#!/usr/bin/python3
import re
from typing import Tuple
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy

try:
    from ..backend import UserDirs, logger
except (ValueError, ImportError):
    from backend import UserDirs, logger

log = logger.new(__name__)


# # # # # TITLE BAR # # # # #


class MouseFilter(QtCore.QObject):
    def __init__(self, note):
        super().__init__()
        self.note = note
        self.core = note.core
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setToolTipDuration(0)
        self.debounce = 0

    def mouseDoubleClickEvent(self, event):
        """Handler for double click event"""
        self.core.execute(self.group, "doubleclick", self.note.path)

    def mousePressEvent(self, event):
        """Handler for mouse button events"""
        buttons = {
            QtCore.Qt.LeftButton: "left",
            QtCore.Qt.MiddleButton: "middle",
            QtCore.Qt.RightButton: "right",
        }
        button = buttons.get(event.button())
        self.core.execute(self.group, button, self.note.path)
        self.note.mousePressEvent(event)

    def wheelEvent(self, event):
        """Handler for mouse wheel events"""
        threshold = self.core.sdb["general"]["wheel threshold"]
        if self.debounce >= threshold:
            direction = "up" if event.angleDelta().y() > 0 else "down"
            self.core.execute(self.group, direction, self.note.path)
        self.debounce += 1 if self.debounce < threshold else -threshold


class TitleCloseButton(QtWidgets.QPushButton, MouseFilter):
    group = "close"

    def __init__(self, note):
        super().__init__(note)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.setObjectName("topbar-close")
        self.setText("×")


class TitleLabel(QtWidgets.QLabel, MouseFilter):
    group = "title"

    def __init__(self, note):
        super().__init__(note)
        self.core = note.core
        self.setObjectName("topbar-title")
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)

    def paintEvent(self, event):
        """Elides long title, else wraps and sets the minimum width to prevent truncation"""
        threshold = self.core.sdb["general"]["elide threshold"]
        if threshold and len(self.text()) > threshold:
            # Elide long title exceeding threshold
            metrics = self.fontMetrics()
            elided = metrics.elidedText(self.text(), QtCore.Qt.ElideMiddle, self.width())
            painter = QtGui.QPainter(self)
            painter.drawText(self.rect(), self.alignment(), elided)

            # Override wrapped text maximum height
            margins = self.contentsMargins()
            height = metrics.height() + margins.top() + margins.bottom()
            self.setMaximumHeight(height)
        else:
            self.setMaximumHeight(QtWidgets.QWIDGETSIZE_MAX)
            super().paintEvent(event)
            self._adjustMinWidth()

    def _adjustMinWidth(self):
        """Sets minimum width the pixel length of the longuest word"""
        longuestWord = max([line for line in self.text().split()], key=len)
        charWidth = self.fontMetrics().maxWidth()
        minWidth = charWidth * (len(longuestWord) + 1)
        self.setMinimumWidth(minWidth)


class TitleStatusButton(QtWidgets.QPushButton, MouseFilter):
    group = "status"

    def __init__(self, note):
        super().__init__(note)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.setObjectName("topbar-status")


# # # # # MESSAGE BAR # # # # #


class MessageLabel(QtWidgets.QLabel):
    def __init__(self, note):
        super().__init__()
        self.note = note
        self.core = note.core
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        QtCore.QTimer.singleShot(0, self.update)

    def autoWrap(self):
        """Disables word wrap when the message bar horizontal space is sufficient"""
        self.setWordWrap(self.isBarFull)

    @property
    def isBarFull(self) -> bool:
        """Measures the available horizontal space based on the real width of unwrapped
        labels. This include the space used by CSS padding, margins and font metrics"""
        used = 0
        msgbar = self.note.msgbarFrame
        for label in msgbar.findChildren(QtWidgets.QLabel):
            mock = QtWidgets.QLabel(label.text())
            mock.setObjectName(label.objectName())
            mock.adjustSize()
            used += mock.width()
        margins = self.note.contentsMargins()
        available = self.note.width() - margins.left() - margins.right()
        return (available - used) <= 1

    def update(self):
        """Wrapper for private _update() function. Prevents windows resizing by enabling wordwrap
        before setText() call. Toggles message bar visibility as needed"""
        self.setWordWrap(True)
        self._update()
        self.autoWrap()

    def resizeEvent(self, event):
        """Avoids vertical text truncation for long file paths"""
        self.adjustSize()
        super().resizeEvent(event)


class EncryptionLabel(MessageLabel):
    def __init__(self, note):
        super().__init__(note)
        self.setObjectName("msgbar-encryption")
        self.setStyleSheet("padding: 2px 1px 0px 4px;")

    def _update(self):
        """Sets visibility of the encryption indicator"""
        n = self.note
        if n.mode in ("console", "image"):
            self.hide()
            return

        isEncrypted = n.keyring.hasEncryption()
        enabled = bool(isEncrypted and self.core.sdb["message bar"]["encryption"])
        self.setVisible(enabled)
        if enabled:
            active = n.isActiveWindow()
            color = n.css["encryption-icon-active"] if active else n.css["encryption-icon"]
            color = QtGui.QColor(color)
            icon = n.icons.menu["key_encrypt"]
            icon = self.core.colorize(icon, color)
            icon = icon.pixmap(QtCore.QSize(12, 12))
            self.setPixmap(icon)


class FolderLabel(MessageLabel):
    def __init__(self, note):
        super().__init__(note)
        self.setObjectName("msgbar-folder")

    def _update(self):
        """Updates the folder label according to the current note path"""
        path = self.note.path.relative_to(UserDirs.NOTES)
        path = str(path.parent)
        path = "" if path == "." else path
        enabled = bool(path and self.note.core.sdb["message bar"]["folder"])
        self.setText(path)
        self.setVisible(enabled)


class WordsCounter(MessageLabel):
    def __init__(self, note):
        if note.mode in ("plain", "html"):
            note.body.textChanged.connect(self.update)
            note.body.selectionChanged.connect(self.update)
        else:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.update)
            self.timer.setInterval(1000)
            self.timer.start()
        self.body = note.body
        super().__init__(note)
        self.setObjectName("msgbar-words")

    def _count(self, text: str) -> Tuple[int, int]:
        """Counts the amount of words and characters in a string"""
        words = len(re.findall(r"\S+", text))
        chars = len(text)
        return (words, chars)

    def _external(self) -> Tuple[str, str, str]:
        """Fetches content from file"""
        with open(self.note.path, encoding="utf-8") as f:
            return f.read().rstrip(), "", ""

    def _internal(self) -> Tuple[str, str, str]:
        """Fetches content from Q_TextEdit"""
        cursor = self.body.textCursor()
        prefix, suffix = ("[", "]") if cursor.hasSelection() else ("", "")
        text = cursor.selectedText() if cursor.hasSelection() else self.body.toPlainText()
        return text, prefix, suffix

    def _update(self, force=False):
        """Updates the words counter label for the current selection or the whole text"""
        if self.note.mode == "vim":
            if self.text() and not self.note.isVisible():
                return
            text, prefix, suffix = self._external()
        else:
            text, prefix, suffix = self._internal()

        words, chars = self._count(text)
        wordsNum = "s" if words > 1 else ""
        charsNum = "s" if chars > 1 else ""
        self.setText(f"{prefix}{words} word{wordsNum}, {chars} character{charsNum}{suffix}")
        self.setVisible(self.core.sdb["message bar"]["words"])


class PopupFrame(QtWidgets.QFrame):
    def __init__(self, note):
        super().__init__(note)
        self.setObjectName("popup-frame")
        self.leftLabel = QtWidgets.QLabel()
        self.leftLabel.setObjectName("msgbar-popup-left")
        self.rightLabel = QtWidgets.QLabel()
        self.rightLabel.setObjectName("msgbar-popup-right")

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.leftLabel)
        layout.addWidget(self.rightLabel)
        self.setLayout(layout)
        self.hide()

        self.note = note
        self.core = note.core
        self.timer = QtCore.QTimer(note)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._clear)

    def showMessage(self, left: str, right: str):
        """Hides the regular message bar and display the popup message"""
        interval = self.core.sdb["message bar"]["popup interval"]
        cssEnabled = bool(self.note.css["popup-visible"] == "true")
        enabled = not self.note.rolled and self.note.hasClearText() and cssEnabled
        if interval and enabled:
            self.leftLabel.setText(left)
            self.rightLabel.setText(right)
            self.note.msgbarStack.setCurrentIndex(1)
            self.note.msgbarStack.show()
            self.timer.start(interval)

    def _clear(self):
        """Clears popup message and shows the regular message bar"""
        self.leftLabel.clear()
        self.rightLabel.clear()
        self.note.msgbarStack.setCurrentIndex(0)
        if not self.note.rolled:
            self.note.setup.msgbar()


# # # # # TOOL BAR # # # # #


class ToolbarSpacer(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        policy = QSizePolicy.MinimumExpanding, QSizePolicy.Ignored
        self.setSizePolicy(*policy)
        self.setObjectName("toolbar-spacer")
        self.hide()


class ToolButton(QtWidgets.QPushButton):
    def __init__(self, note, action):
        super().__init__()
        self.note = note
        self.action = note.actions[action]
        self.setObjectName("toolbar-icon")
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setToolTip(self.action.label)
        self.clicked.connect(self._clicked)

    def _clicked(self, event):
        """Handler for left click event"""
        log.info(f"{self.note.id} : {self.action.label}")
        try:
            self.action.call()
        except TypeError:
            self.action.call(self.note.path)


# # # # # HOT BAR # # # # #


class HotbarSpacer(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        policy = QSizePolicy.MinimumExpanding, QSizePolicy.Ignored
        self.setSizePolicy(*policy)
        self.setObjectName("hotbar-spacer")


class SizeGrip(QtWidgets.QSizeGrip):
    def __init__(self, note, tag=None):
        super().__init__(note)
        self.note = note
        self.setObjectName(tag)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)


class SizeGripVertical(SizeGrip):
    def __init__(self, note):
        super().__init__(note)
        self.setObjectName("center")

    def mousePressEvent(self, event):
        """Blocks horizontal resizing"""
        self.note.setFixedWidth(self.note.width())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Restores horizontal resizing"""
        self.note.setFixedWidth(QtWidgets.QWIDGETSIZE_MAX)
        super().mouseReleaseEvent(event)
