#!/usr/bin/python3
import ctypes
import math
import shutil
import sys
from collections import namedtuple
from copy import deepcopy
from pathlib import Path
from typing import Callable, Iterable, Tuple
from PyQt5 import QtWidgets, QtCore, QtGui

try:
    from ..backend import UserDirs, RootDirs, RootFiles, Tuples, logger
    from ..backend.cryptography import Keyring
    from ..menus.note import EncryptionMenu, ModeMenu, PaletteMenu, SaveDialog, StyleMenu, ToolMenu
    from ..menus.bars import (
        EncryptionLabel,
        FolderLabel,
        HotbarSpacer,
        PopupFrame,
        SizeGrip,
        SizeGripVertical,
        TitleCloseButton,
        TitleLabel,
        TitleStatusButton,
        ToolbarSpacer,
        ToolButton,
    )
except (ValueError, ImportError):
    from backend import UserDirs, RootDirs, RootFiles, Tuples, logger
    from backend.cryptography import Keyring
    from menus.note import EncryptionMenu, ModeMenu, PaletteMenu, SaveDialog, StyleMenu, ToolMenu
    from menus.bars import (
        EncryptionLabel,
        FolderLabel,
        HotbarSpacer,
        PopupFrame,
        SizeGrip,
        SizeGripVertical,
        TitleCloseButton,
        TitleLabel,
        TitleStatusButton,
        ToolbarSpacer,
        ToolButton,
    )

log = logger.new(__name__)


class NoteWindow(QtWidgets.QWidget):
    shown = QtCore.pyqtSignal(Path)
    hidden = QtCore.pyqtSignal(Path)

    def __init__(self, core, path: Path):
        super().__init__()
        self.core = core
        self.setWindowTitle(path.stem)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setContentsMargins(1, 0, 1, 1)
        self.setAcceptDrops(True)

        self.content = ""
        self.key = core.masterKey if core.sdb["general"]["encrypt all"] else None
        self.movable = False
        self.keyFilter = KeyFilter(self)
        self.syncTimer = QtCore.QTimer(interval=1000)
        self.syncTimer.timeout.connect(self._sync)
        self.syncTimer.start()

    def changeEvent(self, event):
        """Monitors window activation"""
        if event.type() == QtCore.QEvent.ActivationChange:
            try:
                self._refreshToolbar()
                self.setup.status()
                if not self.rolled and self.hasClearText():
                    self.setup.msgbar()
            except (KeyError, FileNotFoundError):
                pass

    def closeEvent(self, event):
        """Closes cleanly and delete the note object"""
        log.info(f"Closing '{self.id}'")
        if "save" in dir(self):
            self.save()

        if self.path.is_nested():
            self.removeBlank()
            if self.id in self.core.ndb["loaded"]:
                self.core.ndb["loaded"].remove(self.id)

        self.core.loaded.pop(self.path, None)
        if not self.inModeTransition and self.id in self.core.ndb["favorites"]:
            self.core.ndb["favorites"].remove(self.id)
        super().closeEvent(event)

    def dragEnterEvent(self, event):
        """Allows the implementation of a customized dropEvent handler"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        super().dragEnterEvent(event)

    def dropEvent(self, event):
        """Transferts dropped URLs to the global DropFilter thread"""
        for url in event.mimeData().urls():
            url = url.toString(QtCore.QUrl.PreferLocalFile)
            QtCore.QMetaObject.invokeMethod(
                self.core.dropFilter,
                "filter",
                QtCore.Qt.QueuedConnection,
                QtCore.Q_ARG(object, self.path),  # Path of sender
                QtCore.Q_ARG(str, url),  # URL to filter
            )
        super().dropEvent(event)

    def focusInEvent(self, event):
        self.shown.emit(self.path)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        """Saves geometry on focus out event"""
        if self.id in self.core.pdb:
            self.saveGeometry()
        super().focusOutEvent(event)

    def hideEvent(self, event):
        self.hidden.emit(self.path)
        super().hideEvent(event)

    def keyPressEvent(self, event):
        """Hotkeys handler"""
        self.keyFilter.update(event)
        nonTextMode = self.mode not in ("plain", "html")  # KeyEvents are handled into Q_TextEdit()
        if self.keyFilter.match() and nonTextMode:
            self.keyFilter.execute()
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """Hotkeys handler"""
        self.keyFilter.update(event)

    def mouseMoveEvent(self, event):
        """Enables window mouse dragging"""
        if self.movable:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(event.globalPos() - self.dragPosition)

    def mousePressEvent(self, event):
        """Enables window mouse dragging"""
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            self.movable = True

    def mouseReleaseEvent(self, event):
        """Prevents mouse dragging on sub-widgets"""
        self.movable = False

    @property
    def onScreen(self) -> bool:
        """Verifies if the window fits inside of screen boundaries"""
        center = self.frameGeometry().center()
        for screen in self.core.screens():
            if screen.contains(center):
                return True
        return False

    def paintEvent(self, event):
        """Draws a one pixel black border around window"""
        border = QtGui.QColor(self.css["border-color"])
        background = self.palette().color(QtGui.QPalette.Background)
        background = QtGui.QColor(background)
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(border))
        painter.drawRect(0, 0, self.width(), self.height())
        painter.setBrush(QtGui.QBrush(background))
        painter.drawRect(1, 1, self.width() - 2, self.height() - 2)

    def resizeEvent(self, event):
        for label in self.msgbarFrame.findChildren(QtWidgets.QLabel):
            label.autoWrap()
            if self.mode == "image":
                label.update()
        super().resizeEvent(event)

    def showEvent(self, event):
        """Shows a note, hides it from system taskbar and updates its style and geometry"""

        def _skipTaskbar():
            if sys.platform.startswith("linux"):
                self.xprop.start()
                self.xprop.waitForFinished()

        log.info(f"{self.id} : Show event")
        if not self.path.is_file():
            return

        self.setWindowState(QtCore.Qt.WindowNoState)  # Restore notes hidden in an inactive desktop
        if self.core.sdb["general"]["skip taskbar"]:
            _skipTaskbar()

        if self.core.sdb["general"]["reposition"]:
            if not self.onScreen:
                self.snap()

        self.activateWindow()
        super().showEvent(event)

    def _sync(self):
        """Unloads externally deleted files"""
        if not self.path.is_file():
            log.warning(f"{self.id} : Deleted by an external process")
            self.close()
            self.core.setup.records.lint()


class Note(NoteWindow):
    def __init__(self, core, path: Path):
        super().__init__(core, path)
        self.path = path
        self.setup = NoteSetup(self, path)
        self.decorate()
        self.restoreGeometry()
        QtCore.QTimer.singleShot(0, self._zoom)

    def hasClearText(self) -> bool:
        """Returns true if text is decrypted or clear text"""
        return self.keyring.hasKey()

    def decorate(self):
        """Applies profile's stylesheet and NoteDecorations{} selector attributes"""
        self.setup.css()
        self.setup.icons()
        self.setup.actions()
        self.setup.toolbar()
        self.setup.status()
        if not self.rolled and self.hasClearText():
            self.setup.msgbar()

    def duplicate(self):
        """Clones the current note"""
        folders = self.path.parent.relative_to(UserDirs.NOTES)
        new = self.core.nameIndex(UserDirs.NOTES / folders / self.path.name)
        shutil.copy(self.path, new)

        # Update the profile and load the clone
        x, y = self.pos().x(), self.pos().y()
        w, h = self.width(), self.height()
        nid = str(new.relative_to(UserDirs.NOTES))
        self.core.pdb[nid] = deepcopy(self.core.pdb[self.id])
        self.core.pdb[nid]["position"] = x + 20, y + 20
        self.core.pdb[nid]["width"] = w
        self.core.pdb[nid]["height"] = h
        self.core.notes.add(new)
        if self.key:
            self.core.loaded[new].keyring.setKey(self.key)

    def load(self):
        pass

    def menuTool(self):
        """Opens the tool contextual menu"""
        if self.css["context-menu"] == "true":
            self.toolMenu.popup(QtGui.QCursor.pos())

    def moveCursorToTop(self):
        """Moves the cursor at the beginning of the document"""
        cursor = self.body.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        self.body.setTextCursor(cursor)

    def moveDialog(self):
        """Opens subfolder browser dialog"""
        self.core.moveDialog(self.path)

    def opacityDecrease(self):
        """Decreases window opacity"""
        self._opacity(-0.1)

    def opacityIncrease(self):
        """Increases window opacity"""
        self._opacity(0.1)

    def pin(self):
        """Toggles the pin attribute of the note profile"""
        current = self.core.pdb[self.id]["pin"]
        self.core.pdb[self.id]["pin"] = not current
        self.setup.status()

    def position(self, index: int, total: int) -> Tuple[int, int]:
        """Calculates the right position for a new note"""
        w, h = self.width(), self.height()
        pos = self.frameGeometry()
        rect = self.core.screen()
        gap = 20

        screen_h = rect.height() - h - (h / 3)  # Available screen rect less clearance
        col_count = max(int(screen_h / gap) + 1, 1)  # Number of notes in each columns
        col_current = int(index / col_count)  # Column # of the current note

        # Drift correction for new columns
        col_drift = gap * col_count
        x_offset = (w - col_drift) * col_current
        y_offset = -col_drift * col_current

        # Set the anchor at the screen center for few notes, at left for many
        if int(total / col_count) > 0:
            pos.moveTopLeft(rect.topLeft())
        else:
            pos.moveCenter(rect.center())
            pos.moveTop(rect.top())

        # Apply drift and offset corrections
        drift = gap * index
        x = int(pos.x() + drift + x_offset)
        y = int(pos.y() + drift + y_offset)
        return x, y

    def removeBlank(self):
        """Deletes empty notes"""
        if self.inModeTransition or not self.core.sdb["clean"]["blanks"]:
            return
        try:
            if not self.body.toPlainText():
                self.path.unlink()
                log.info(f"{self.id} : Removed empty note")
                self.core.setup.records.lint()
        except (FileNotFoundError, PermissionError):
            log.exception(f"Could not remove '{self.path}'")
        except AttributeError:
            pass

    def reset(self):
        """Resets window geometry"""
        self.resetSize()
        position = Grid.pos(self, "middle", "center")
        self.move(*position)

    def resetSize(self):
        """Sets size to profile default"""
        width = self.core.sdb["profile default"]["width"]
        height = self.core.sdb["profile default"]["height"]
        self.resize(width, height)

    def resizeToContent(self):
        """Resizes Note to best fit text width and height"""
        if not self.hasClearText():
            return

        def lineCount(text: str) -> int:
            body = QtWidgets.QPlainTextEdit()
            body.setPlainText(text)
            return body.document().blockCount()

        def resizeWindow(text: str):
            width = self.core.screen().width()
            height = self.core.screen().height()
            ultrawide = bool(width / height > 21 / 9)
            screenMaxWidth = width / 5 if ultrawide else width / 3
            screenMaxHeight = height / 3 if ultrawide else height / 1.5

            # Estimate the ideal width
            titleLength = min(30, len(self.titleLabel.text()))
            titleWidth = self.titleLabel.fontMetrics().maxWidth() * titleLength
            titleWidth += self.statusButton.width()
            titleWidth += self.closeButton.width()
            lineMax = max([line for line in text.splitlines()], key=len)
            lineWidth = self.body.fontMetrics().maxWidth() * len(lineMax)

            width = max(titleWidth, lineWidth)
            width = int(min(width, screenMaxWidth))

            # Get the line count at the new width, convert to pixel height
            height = self.body.fontMetrics().height() * lineCount(text)
            height = height * 1.2 if self.mode == "vim" else height
            if width > 1000:
                height += width / 30

            # Add widgets margins and bars height
            for widget in (self.titleLabel, self.msgbarStack, self.toolbarFrame, self.hotbarFrame):
                if widget.isVisible():
                    height += widget.height()

            for widget in (
                self,
                self.body,
                self.titleLabel,
                self.msgbarStack,
                self.toolbarFrame,
                self.hotbarFrame,
            ):
                if widget.isVisible():
                    margins = widget.contentsMargins()
                    width += margins.left() + margins.right()
                    height += margins.top() + margins.bottom()

            # Clamp the note to a reasonable size
            width = int(min(width, screenMaxWidth))
            height = int(min(height, screenMaxHeight))
            self.core.pdb[self.id]["width"] = width
            self.core.pdb[self.id]["height"] = height
            self.resize(width, height)

        def resize():
            self.unroll()
            unsizableMode = self.mode not in ("image", "html", "plain", "vim")
            if self.path.is_empty() or unsizableMode:
                self.resetSize()

            elif self.mode == "image":
                self.resizeFit()

            elif self.mode in ("plain", "html"):
                text = self.body.toPlainText()
                if text:
                    resizeWindow(text)
                    self.moveCursorToTop()

            elif self.mode == "vim":
                text = self.path.read_text()
                resizeWindow(text)

        resize()
        QtCore.QTimer.singleShot(0, resize)

    def restoreGeometry(self):
        """Restores the size, position, wrap mode and opacity from profile"""
        pos = self.core.pdb[self.id]["position"]
        width = self.core.pdb[self.id]["width"]
        height = self.core.pdb[self.id]["height"]
        opacity = self.core.pdb[self.id]["opacity"]
        wrap = self.core.pdb[self.id]["wrap"]

        self.move(*pos)
        self.resize(width, height)
        self.setWindowOpacity(opacity)
        if self.mode in ("plain", "html"):
            wrap = self.body.WidgetWidth if wrap else self.body.NoWrap
            self.body.setLineWrapMode(wrap)
        log.debug(f"{self.id} : Restored geometry w={width} h={height} x={pos[0]} y={pos[1]}")

    def roll(self):
        """Minimizes window to the titlebar height"""
        if not self.rolled:
            self.saveGeometry()
            self.toolbarFrame.hide()
            self.msgbarStack.hide()
            self.hotbarFrame.hide()
            self.body.hide()
            try:
                self.lockScreen.hide()
            except AttributeError:
                pass
            self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMaximized)
            QtCore.QTimer.singleShot(0, self._minimize)  # resize(width, 0) on next loop

    @property
    def rolled(self) -> bool:
        """Indicates rolled state"""
        hotbar = self.hotbarFrame.isVisible()
        titlebar = self.titleLabel.isVisible()
        return bool(titlebar and not hotbar)

    def save(self):
        pass

    def saveDialog(self):
        """Opens a save as browser dialog -> .txt or .png"""
        dialog = SaveDialog(self.core, self.path)
        if dialog.exec_() == dialog.Accepted:
            dest = dialog.selectedFiles()[0]
            if dest:
                try:
                    shutil.copy(self.path, dest)
                    log.info(f"{self.id} : Copied note to '{dest}'")
                    self.core.sdb["runtime"]["save as dir"] = str(Path(dest).parent)
                except PermissionError:
                    log.exception(f"Could not copy file to {dest}")

    def saveGeometry(self):
        """Saves the size, position, wrap mode and opacity to profile"""
        x, y = self.x(), self.y()
        w, h = self.width(), self.height()
        opacity = round(self.windowOpacity(), 2)
        self.core.pdb[self.id]["position"] = [x, y]
        self.core.pdb[self.id]["opacity"] = opacity

        if not self.rolled:
            self.core.pdb[self.id]["width"] = w
            self.core.pdb[self.id]["height"] = h

        if self.mode in ("plain", "html"):
            self.core.pdb[self.id]["wrap"] = bool(self.body.lineWrapMode())
        log.debug(f"{self.id} : Saved geometry w={w} h={h} x={x} y={y}")

    def setTitle(self, title: str):
        """Sets note title"""
        try:
            self.titleLabel.setText(title)
        except AttributeError:
            pass

    def showOuterFrames(self):
        """Shows hotbar and adjusts canvas size"""
        self.hotbarFrame.show()
        width = self.core.pdb[self.id]["width"]
        height = self.core.pdb[self.id]["height"]
        self.resize(width, height)

    def snap(self):
        """Moves a note to the closest grid point on screen"""
        self.move(*Grid.closest(self))
        self.saveGeometry()

    def unroll(self):
        """Restores full window size"""

        def _fixPosition():
            """Bugfix for snap() method, when a note is hidden while in rolled state"""
            if self.pos().isNull():
                pos = self.core.pdb[self.id]["position"]
                self.move(*pos)

        if self.rolled:
            if self.hasClearText():
                self.toolbarFrame.show()
                self.msgbarStack.show()
                self.body.show()
                _fixPosition()
            else:
                self.lockScreen.show()
        self.showOuterFrames()

    def zoomIn(self, increment=True):
        """Increases note size"""
        if increment:
            self.core.pdb[self.id]["zoom"] += 1
        self.body.zoomIn()

    def zoomOut(self, increment=True):
        """Decreases note size"""
        if increment:
            self.core.pdb[self.id]["zoom"] -= 1
        self.body.zoomOut()

    def _initNoteWindow(self, path):
        """Inits menus and setups window properties"""
        self.core.pdb[self.id]["mode"] = self.mode
        self.modeMenu = ModeMenu(self)
        self.paletteMenu = PaletteMenu(self)
        self.styleMenu = StyleMenu(self)
        self.toolMenu = ToolMenu(self)
        if self.mode in ("plain", "html"):
            self.encryptionMenu = EncryptionMenu(self)
        self._setupXprop()

    def _menuEncryption(self):
        """Opens the encryption contextual menu"""
        self.encryptionMenu.popup(QtGui.QCursor.pos())

    def _menuMode(self):
        """Opens the mode contextual menu"""
        self.modeMenu.popup(QtGui.QCursor.pos())

    def _menuMove(self):
        """Opens the move contextual menu"""
        self.moveMenu.popup(QtGui.QCursor.pos())

    def _menuPalette(self):
        """Opens the palette contextual menu"""
        self.paletteMenu.popup(QtGui.QCursor.pos())

    def _menuStyle(self):
        """Opens the style contextual menu"""
        self.styleMenu.popup(QtGui.QCursor.pos())

    def _minimize(self):
        """Resize note window to the titlebar height"""
        self.resize(self.width(), 0)

    def _opacity(self, inc: float):
        """Adjusts window opacity"""
        opacity = round(self.windowOpacity() + inc, 2)
        opacity = opacity if opacity > 0.1 else 0.1
        self.setWindowOpacity(opacity)

    def _refreshToolbar(self):
        """Updates toolbar icons color"""
        color = self.css["toolbar-icon-active"] if self.isActiveWindow() else self.css["toolbar-icon"]
        color = QtGui.QColor(color)
        for _, button in self.tools.items():
            icon = self.core.colorize(button.icon(), color)
            button.setIcon(icon)

    def _setupXprop(self):
        """Hides the note from the system taskbar"""
        skip = self.core.sdb["general"]["skip taskbar"]
        if skip and sys.platform.startswith("win"):
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.Tool)

        elif sys.platform.startswith("linux"):
            # X11: Manually set the _NET_WM_STATE_SKIP_TASKBAR flag on each window
            # Avoid various WM issues related with WA_X11NetWmWindowType*
            # Use of external process 'xprop' since no skip flag exist in Qt yet
            ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
            ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object, ctypes.c_char_p]
            wid = ctypes.pythonapi.PyCapsule_GetPointer(self.winId().ascapsule(), None)
            cmd = f"-id {wid} -f _NET_WM_STATE 32a -set _NET_WM_STATE _NET_WM_STATE_SKIP_TASKBAR"
            self.xprop = QtCore.QProcess()
            self.xprop.setProgram("xprop")
            self.xprop.setArguments(cmd.split())

    def _swap(self):
        """Swaps note status among idle, favorite and pinned"""
        if self.id in self.core.ndb["favorites"]:
            self.core.ndb["favorites"].remove(self.id)
            self.pin()
        elif self.core.pdb[self.id]["pin"]:
            self.pin()
        else:
            self.core.ndb["favorites"].append(self.id)
        self.setup.status()

    def _zoom(self):
        """Restores saved zoom level"""
        if self.mode == "image":
            return
        zoom = self.core.pdb[self.id]["zoom"]
        for i in range(abs(zoom)):
            if zoom > 0:
                self.zoomIn(increment=False)
            elif zoom < 0:
                self.zoomOut(increment=False)


class NoteSetup:
    """Setups instances and variables for Note class"""

    def __init__(self, note, path):
        self.note = note
        self.core = note.core
        self.uid(path)
        self.top()
        self.pdb()
        self.css()
        self.icons()
        self.actions()
        note.keyring = Keyring(note)
        self.bottom()
        self.grid()
        self.signals()
        note.inModeTransition = False
        note.setTitle(path.stem)

    def actions(self):
        """Fetches notes actions for the current mode"""
        c, n = self.core, self.note
        n.actions = self.actionsFromMode(c, n.mode, note=n)

    @staticmethod
    def actionsFromMode(core, mode: str = "all", note: Note = None) -> dict:
        """Returns available actions for one or all modes"""

        class NoteMock:
            def __init__(self):
                self.notes = self
                self.body = self

            def __getattr__(self, *args) -> Callable:
                return lambda: None

        def bicolor(key):
            return Tuples.NoteIcons(note.icons.menu.get(key), note.icons.toolbar.get(key))

        c = core
        n = note if note else NoteMock()
        icons = bicolor if note else lambda key: core.icons.get(key)
        Action = Tuples.Action

        actions = {
            "activate": Action("Activate", icons("activate"), n.activateWindow),
            "delete": Action("Delete", icons("delete"), c.notes.delete),
            "duplicate": Action("Duplicate", icons("duplicate"), n.duplicate),
            "hide": Action("Hide", icons("hide"), n.hide),
            "mode": Action("Mode", icons("mode"), n._menuMode),
            "move": Action("Move", icons("move"), n.moveDialog),
            "new": Action("New note", icons("new"), c.notes.new),
            "opacity+": Action("Increase opacity", icons("opacity_increase"), n.opacityIncrease),
            "opacity-": Action("Decrease opacity", icons("opacity_decrease"), n.opacityDecrease),
            "open": Action("Open in file manager", icons("folder_open"), c.fileManager),
            "pin": Action("Pin", icons("pin"), n.pin),
            "raise": Action("Raise", icons("raise"), n.raise_),
            "refresh": Action("Refresh", icons("refresh"), n.decorate),
            "rename": Action("Rename", icons("rename"), c.notes.rename),
            "reset": Action("Reset geometry", icons("reset"), n.reset),
            "resize": Action("Resize to content", icons("fit"), n.resizeToContent),
            "roll": Action("Roll", icons("roll"), n.roll),
            "save as": Action("Save as", icons("save_as"), n.saveDialog),
            "separator": Action("Separator", icons("separator"), lambda: None),
            "snap": Action("Snap to grid", icons("snap"), n.snap),
            "style": Action("Style", icons("style"), n._menuStyle),
            "swap": Action("Swap status", icons("swap"), n._swap),
            "palette": Action("Palette", icons("palette"), n._menuPalette),
            "unload": Action("Unload", icons("hide"), n.close),
            "unroll": Action("Unroll", icons("unroll"), n.unroll),
            "zoom in": Action("Zoom in", icons("zoom_in"), n.zoomIn),
            "zoom out": Action("Zoom out", icons("zoom_out"), n.zoomOut),
        }

        if mode in ("plain", "html", "all"):
            lockIcon = "unlock" if n.readOnly else "lock"
            actions.update(
                {
                    "antidote": Action("Antidote", icons("spelling"), n.body.antidote),
                    "capitalize": Action("Capitalize", icons("capitalize"), n.body.capitalize),
                    "copy": Action("Copy", icons("copy"), n.body.copyPlain),
                    "cut": Action("Cut", icons("cut"), n.body.cutPlain),
                    "encryption": Action("Encryption", icons("key_encrypt"), n._menuEncryption),
                    "line delete": Action("Delete line", icons("line_delete"), n.body.lineDelete),
                    "line down": Action("Move line downward", icons("line_down"), n.body.lineDown),
                    "line duplicate": Action("Duplicate line", icons("add"), n.body.lineDuplicate),
                    "line end": Action("Go to end of line", icons("line_end"), n.body.lineEnd),
                    "line start": Action("Go to start of line", icons("line_start"), n.body.lineStart),
                    "line up": Action("Move line upward", icons("line_up"), n.body.lineUp),
                    "lock": Action("Lock content (read-only)", icons("lock"), n.lock),
                    "lock|unlock": Action("Toggle read-only", icons(lockIcon), n.toggleLock),
                    "lowercase": Action("Lowercase", icons("lowercase"), n.body.lowercase),
                    "paste": Action("Paste", icons("paste"), n.body.paste),
                    "redo": Action("Redo", icons("redo"), n.body.redo),
                    "save": Action("Save", icons("save"), n.save),
                    "search": Action("Find and replace", icons("search"), n.search),
                    "select": Action("Select block", icons("copy"), n.body.lineSelect),
                    "select all": Action("Select all", icons("select_all"), n.body.selectAll),
                    "shuffle": Action("Shuffle", icons("shuffle"), n.body.lineShuffle),
                    "sort": Action("Sort", icons("sort"), n.body.lineSort),
                    "special paste": Action("Special paste", icons("paste_special"), n.body.pasteSpecial),
                    "swapcase": Action("Swapcase", icons("swapcase"), n.body.swapcase),
                    "titlecase": Action("Titlecase", icons("titlecase"), n.body.titlecase),
                    "undo": Action("Undo", icons("undo"), n.body.undo),
                    "unlock": Action("Unlock content (read-write)", icons("unlock"), n.unlock),
                    "uppercase": Action("Uppercase", icons("uppercase"), n.body.uppercase),
                    "wrap": Action("Word wrap", icons("wrap"), n.body.wrap),
                }
            )

        if mode in ("html", "all"):
            actions.update(
                {
                    "bold": Action("Bold", icons("bold"), n.body.bold),
                    "clear format": Action("Clear formatting", icons("clear_format"), n.body.clearFormat),
                    "copy rich": Action("Copy rich text", icons("copy"), n.body.copy),
                    "cut rich": Action("Cut rich text", icons("cut"), n.body.cut),
                    "highlight": Action("Highlight", icons("highlight"), n.body.highlight),
                    "italic": Action("Italic", icons("italic"), n.body.italic),
                    "strike": Action("Strikethrough", icons("strike"), n.body.strike),
                    "underline": Action("Underline", icons("underline"), n.body.underline),
                }
            )

        if mode in ("image", "all"):
            lockIcon = "lock" if n.keepAspectRatio else "unlock"
            actions.update(
                {
                    "aspect ratio": Action("Keep aspect ratio", icons(lockIcon), n.toggleAspectRatio),
                    "fit": Action("Resize to fit screen", icons("fit"), n.resizeFit),
                    "original": Action("Original size", icons("size_original"), n.resizeOriginal),
                    "scale": Action("Restore aspect ratio", icons("aspect_ratio"), n.restoreAspectRatio),
                }
            )

        if mode in ("console", "all"):
            actions.update(
                {
                    "reload": Action("Reload", icons("reset"), n.reload),
                }
            )

        return actions

    def bottom(self):
        """Organizes bottom bar layout"""
        c, n = self.core, self.note

        # Message bar & Popup
        n.msgbarLayout = QtWidgets.QHBoxLayout()
        n.msgbarLayout.setContentsMargins(0, 0, 0, 0)
        n.msgbarLayout.setSpacing(0)
        spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        n.encryptionLabel = EncryptionLabel(n)
        n.folderLabel = FolderLabel(n)
        n.msgbarLayout.addWidget(n.encryptionLabel)
        n.msgbarLayout.addWidget(n.folderLabel)
        n.msgbarLayout.addItem(spacer)

        n.popupFrame = PopupFrame(n)
        n.msgbarFrame = QtWidgets.QFrame()
        n.msgbarStack = QtWidgets.QStackedWidget()
        n.msgbarStack.addWidget(n.msgbarFrame)
        n.msgbarStack.addWidget(n.popupFrame)
        policy = QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum
        n.msgbarStack.setSizePolicy(*policy)

        # Toolbar
        n.leftSpacer = ToolbarSpacer()
        n.rightSpacer = ToolbarSpacer()
        n.toolbarFrame = QtWidgets.QFrame()
        n.toolbarLayout = QtWidgets.QHBoxLayout()
        n.toolbarLayout.setContentsMargins(0, 0, 0, 0)
        n.toolbarLayout.setSpacing(0)

        n.toolbarLayout.addWidget(n.leftSpacer)
        n.tools = {}
        for action in c.sdb["toolbar menus"][n.mode]:
            if action == "separator":
                separator = QtWidgets.QLabel(":")
                separator.setObjectName("toolbar-separator")
                n.toolbarLayout.addWidget(separator)
            else:
                try:
                    n.tools[action] = ToolButton(n, action)
                    n.toolbarLayout.addWidget(n.tools[action])
                except KeyError:
                    log.exception(f"Invalid note menu option '{action}'")
        n.toolbarLayout.addWidget(n.rightSpacer)

        # Hotbar
        sizeGrips = SizeGrip(n, "left"), SizeGripVertical(n), SizeGrip(n, "right")
        n.sizeGrips = Tuples.SizeGrips(*sizeGrips)
        n.hotbarFrame = QtWidgets.QFrame()
        n.hotbarLayout = QtWidgets.QHBoxLayout()
        n.hotbarLayout.setContentsMargins(0, 0, 0, 0)
        n.hotbarLayout.setSpacing(0)

        n.hotbarLayout.addWidget(n.sizeGrips.left)
        n.hotbarLayout.addWidget(HotbarSpacer())
        n.hotbarLayout.addWidget(n.sizeGrips.center)
        n.hotbarLayout.addWidget(HotbarSpacer())
        n.hotbarLayout.addWidget(n.sizeGrips.right)

        # Layout
        n.toolbarFrame.setLayout(n.toolbarLayout)
        n.toolbarFrame.setObjectName("toolbar-frame")
        n.msgbarFrame.setLayout(n.msgbarLayout)
        n.msgbarFrame.setObjectName("msgbar-frame")
        n.hotbarFrame.setLayout(n.hotbarLayout)
        n.hotbarFrame.setObjectName("hotbar-frame")

    def css(self):
        """Updates combined stylesheets and NoteDecorations{} CSS selectors"""
        c, n = self.core, self.note
        c.setup.css()  # Reloads global.css

        profile = c.pdb[n.id]
        userStyle = UserDirs.STYLES / profile["style"]
        rootStyle = RootDirs.STYLES / profile["style"]
        userPalette = UserDirs.PALETTES / profile["palette"]
        rootPalette = RootDirs.PALETTES / profile["palette"]

        Stylesheet = namedtuple("Stylesheet", ("user", "root", "fallback"))
        style = Stylesheet(userStyle, rootStyle, RootFiles.DEFAULT_STYLE)
        palette = Stylesheet(userPalette, rootPalette, RootFiles.DEFAULT_PALETTE)

        paths = []
        for css in (style, palette):
            if css.user.is_file():
                paths.append(css.user)
            elif css.root.is_file():
                paths.append(css.root)
            else:
                paths.append(css.fallback)
        n.css = c.getNoteDecorationsCSS(*paths)

        # Combines and apply profile stylesheets
        css = ""
        for s in paths:
            with open(s, encoding="utf-8") as f:
                css += f.read()
        n.setStyleSheet(css)

        sheets = ", ".join([str(s) for s in paths])
        log.debug(f"{n.id} : Loaded profile CSS '{sheets}'")

    def grid(self):
        """Organizes all widgets sublayouts into the grid layout"""
        n = self.note
        n.gridLayout = QtWidgets.QGridLayout(n)
        n.gridLayout.setSpacing(0)
        n.gridLayout.setContentsMargins(0, 0, 0, 0)
        n.gridLayout.addWidget(n.statusButton, 0, 0, 1, 1)
        n.gridLayout.addWidget(n.titleLabel, 0, 1, 1, 1)
        n.gridLayout.addWidget(n.closeButton, 0, 2, 1, 1)
        n.gridLayout.addWidget(n.msgbarStack, 2, 0, 1, 3)
        n.gridLayout.addWidget(n.toolbarFrame, 3, 0, 1, 3)
        n.gridLayout.addWidget(n.hotbarFrame, 4, 0, 1, 3)

    def icons(self):
        """Applies a custom foreground color on toolbar icons"""
        c, n = self.core, self.note
        toolbarColor = QtGui.QColor(n.css["toolbar-icon-active"])
        menuColor = QtGui.QColor(n.css["menu-icon"])
        n.icons = Tuples.NoteIcons({}, {})
        for i in c.icons:
            n.icons.toolbar[i] = c.colorize(c.icons[i], toolbarColor)
            n.icons.menu[i] = c.colorize(c.icons[i], menuColor)

    def msgbar(self):
        """Sets visibility of the message bar stack widget"""
        c, n = self.core, self.note

        def _bars() -> list:
            """Returns a list of available message bars"""
            bars = ["folder"] if n.path.is_nested() else []
            if n.mode == "image":
                bars.append("pixels")
            elif n.mode != "console":
                bars.append("words")
                if n.keyring.hasEncryption():
                    bars.append("encryption")
            return bars

        def _updateLabels():
            """Updates relevant message labels"""
            labels = n.msgbarFrame.findChildren(QtWidgets.QLabel)
            for label in labels:
                label.update()

        enabled = bool(n.css["msgbar-visible"] == "true")
        for bar in _bars():
            if enabled and c.sdb["message bar"][bar]:
                _updateLabels()
                n.msgbarStack.show()
                break
        else:
            n.msgbarStack.hide()

    def pdb(self):
        """Verifies that the profile exist, else create a new one"""
        c, n = self.core, self.note
        profiles = c.pdb
        if n.id not in profiles:
            index = len(c.loaded) + 1
            new = deepcopy(c.sdb["profile default"])
            n.resize(new["width"], new["height"])
            profiles[n.id] = new
            profiles[n.id]["position"] = n.position(index, index)

    def signals(self):
        """Connects contextual menu signals"""
        n = self.note
        for widget in (n.titleLabel, n.toolbarFrame, n.hotbarFrame):
            widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            widget.customContextMenuRequested.connect(n.menuTool)

    def status(self):
        """Sets and colorizes the appropriate status icon pixmap"""
        c, n = self.core, self.note
        if c.pdb[n.id]["pin"]:
            icon = n.icons.toolbar["pin_title"]
        elif n.id in c.ndb["favorites"]:
            icon = n.icons.toolbar["toggle"]
        else:
            icon = n.icons.toolbar["tray"]

        color = n.css["status-icon-active"] if n.isActiveWindow() else n.css["status-icon"]
        icon = c.colorize(icon, QtGui.QColor(color))
        n.statusButton.setIcon(icon)
        n.setWindowIcon(icon)

    def toolbar(self):
        """Setups toolbar layout and buttons"""
        c, n = self.core, self.note

        # Toolbar alignment
        left = bool(n.css["toolbar-align"] in ("center", "right"))
        right = bool(n.css["toolbar-align"] in ("center", "left"))
        n.leftSpacer.setVisible(left)
        n.rightSpacer.setVisible(right)

        # Toolbar icons
        for action in c.sdb["toolbar menus"][n.mode]:
            try:
                icon = n.tools[action]
                icon.setIcon(n.actions[action].icon.toolbar)
            except KeyError:
                pass

        # Visibility
        visible = n.css["toolbar-visible"] == "true"
        layout = n.toolbarLayout
        for w in (layout.itemAt(i) for i in range(layout.count())):
            w.widget().setVisible(visible)

    def top(self):
        """Organizes top layout"""
        n = self.note
        n.statusButton = TitleStatusButton(n)
        n.titleLabel = TitleLabel(n)
        n.closeButton = TitleCloseButton(n)

    def uid(self, path: Path):
        """Parses and sets identifiers from note path"""
        n = self.note
        n.id = str(path.relative_to(UserDirs.NOTES))
        n.path = path
        n.name = path.stem
        n.setTitle(path.stem)


class Grid:
    def pos(note, vertical: str, horizontal: str) -> Tuple[int, int]:
        """Translates a grid point from strings to (x, y) coordinates"""
        noteGeometry = note.frameGeometry()
        screenGeometry = QtWidgets.QDesktopWidget().availableGeometry()
        Anchor = namedtuple("Anchor", ("anchor", "coordinate"))
        positions = {
            "left": Anchor(noteGeometry.moveLeft, screenGeometry.left),
            "center": Anchor(noteGeometry.moveCenter, screenGeometry.center),
            "right": Anchor(noteGeometry.moveRight, screenGeometry.right),
            "top": Anchor(noteGeometry.moveTop, screenGeometry.top),
            "middle": Anchor(noteGeometry.moveCenter, screenGeometry.center),
            "bottom": Anchor(noteGeometry.moveBottom, screenGeometry.bottom),
        }
        order = (horizontal, vertical) if horizontal == "center" else (vertical, horizontal)
        for pos in order:
            direction = positions[pos]
            direction.anchor(direction.coordinate())
        x = noteGeometry.x()
        y = noteGeometry.y()
        return (x, y)

    @classmethod
    def closest(cls, note) -> Tuple[int, int]:
        """Returns the (x, y) coordinates of the closest grid point"""
        best = cls._snapToGrid(note)
        return cls.pos(note, *best)

    def _snapToGrid(note) -> Tuple[str, str]:
        """Returns the nearest grid point on the screen"""

        def _average(a: QtCore.QPoint, b: QtCore.QPoint) -> QtCore.QPoint:
            dx = int((a.x() + b.x()) / 2)
            dy = int((a.y() + b.y()) / 2)
            return QtCore.QPoint(dx, dy)

        def _distance(point: QtCore.QPoint) -> int:
            noteGeometry = note.frameGeometry().center()
            dx = abs(point.x() - noteGeometry.x())
            dy = abs(point.y() - noteGeometry.y())
            distance = math.sqrt(dx**2 + dy**2)
            return int(distance)

        screen = QtWidgets.QDesktopWidget().availableGeometry()
        topCenter = _average(screen.topLeft(), screen.topRight())
        bottomCenter = _average(screen.bottomLeft(), screen.bottomRight())
        middleLeft = _average(screen.topLeft(), screen.bottomLeft())
        middleRight = _average(screen.topRight(), screen.bottomRight())
        middleCenter = _average(middleLeft, middleRight)
        points = {
            _distance(screen.topLeft()): ("top", "left"),
            _distance(screen.topRight()): ("top", "right"),
            _distance(screen.bottomLeft()): ("bottom", "left"),
            _distance(screen.bottomRight()): ("bottom", "right"),
            _distance(topCenter): ("top", "center"),
            _distance(bottomCenter): ("bottom", "center"),
            _distance(middleLeft): ("middle", "left"),
            _distance(middleRight): ("middle", "right"),
            _distance(middleCenter): ("middle", "center"),
        }
        best = min(points)
        return points[best]


class KeyFilter:
    def __init__(self, note):
        self.note = note
        self.core = note.core
        self.blocked = (
            "ctrl;c",
            "ctrl;x",
            "ctrl;v",
            "ctrl;z",
            "ctrl;y",
            "ctrl;a",
            "ctrl;k",
            "ctrl;ins",
            "ctrl;home",
            "ctrl;end",
            "shift;ins",
            "shift;del",
        )
        self.last = None

    def execute(self):
        """Executes the action bound to the last pressed hotkey"""
        hk, action = self.last
        hk = hk.replace(",", "+")
        hk = hk.replace(";", "+")
        hk = hk.title()
        log.info(f"{self.note.id} : Hotkey pressed : {hk} : {action.label}")
        self.note.popupFrame.showMessage(action.label, hk)
        try:
            action.call()
        except TypeError:
            action.call(self.note.path)

    def ignored(self) -> bool:
        """Verifies if the match should be ignored (override of Qt's default in QTextEditWidget)"""
        match = self._find(self.blocked)
        return bool(match)

    def match(self) -> Tuples.Action:
        """Verifies if the pressed keys matches an hotkey, returns the relevant Action if any"""
        if not self.core.sdb["general"]["hotkeys"]:
            return None

        hotkeys = self.core.sdb["key events"]
        hk = self._find(hotkeys)
        try:
            action = hotkeys.get(hk)[1]
            action = self.note.actions[action]
            self.last = (hk, action)
            return action
        except TypeError:
            pass
        except (IndexError, KeyError):
            log.error(f"{self.note.id} : Invalid hotkey")

    def update(self, event: QtGui.QKeyEvent):
        """Updates modifiers and key pressed status"""
        mod = event.modifiers()
        self.modifiers = {
            "shift": bool(mod & QtCore.Qt.ShiftModifier),
            "ctrl": bool(mod & QtCore.Qt.ControlModifier),
            "alt": bool(mod & QtCore.Qt.AltModifier),
            "meta": bool(mod & QtCore.Qt.MetaModifier),
        }
        key = QtGui.QKeySequence(event.key())
        self.key = key.toString().lower()

    def _find(self, hotkeys: Iterable) -> str:
        """Looks through all registered hotkeys to return matches"""
        for hk in hotkeys:  # "ctrl,shift;d": ("note", "delete"),
            mods, key = hk.split(";")
            mods = mods.split(",")
            underload = [m for m in mods if not self.modifiers[m]]
            overload = [m for m in self.modifiers if self.modifiers[m] and m not in mods]
            if not underload and not overload and self.key == key:
                return hk
        return None
