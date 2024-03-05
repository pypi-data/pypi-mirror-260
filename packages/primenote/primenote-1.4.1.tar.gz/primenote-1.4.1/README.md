<!--LOGO BANNER-->

# PrimeNote
PrimeNote is an intuitive sticky note-taking application for Linux and Windows. It allows the user to effectively edit, store and organize an infinite number of notes. PrimeNote supports various operation modes, such as `plain text`, `rich text`, `image`, `vim` or `console` (terminal emulator). It is well structured and fully featured, including;

- **Always on top** notes, without cluttering the taksbar
- **Druide Antidote** grammar tools built-in support (versions 9, 10 and 11)
- **Smart formatting**, using enhanced 'plain' text where the input is standardized, yet allows basic text decorations
- **Cross-platform compatibility**, with official support for Linux and Windows 7-10
- **Neat organization**, with all data stored by folder structure using human-friendly formats
- **Fernet encryption**, to protect sensitive data
- **Quick search** built-in keyboard-driven tool to browse among note titles and content
- **Special paste** feature to quickly copy text from PDF documents
- **Images support**, with basic viewing features
- **Fully customizable** appearance, menus, hotkeys and mouse events
- **Virtual machine support**, edit a shared note repository in real time
- **Command-line interface** access to all notes (see `pnote -h`)

Its open source software is licensed under GPLv3.

<br/>

# Getting Started — Installation
## Microsoft Windows
- For Windows 7 and above, download and execute the latest **[NSIS installer](https://gitlab.com/william.belanger/storage/-/raw/primenote/primenote-1.4.1.exe?inline=false)**

## Arch Linux
- Install `primenote-git` from the AUR
- Install `gvim` and `qtermwidget` community packages (optional)

## Debian
**PyPi package**
```
# Update system packages
sudo apt-get update
sudo apt-get upgrade

# Install PrimeNote using the 'pipx' tool
sudo apt-get install pipx
pipx install --include-deps primenote
pipx ensurepath

# Re-login so that 'primenote' becomes globally available
```

**Vim and Console modes support**
- Install QTermWidget with PyQt bindings `QTERMWIDGET_BUILD_PYTHON_BINDING=ON`
- Install `vim-gtk` (with client-server mode enabled)

<br/>

# Advanced Features
## Customizable window styles and palettes
- All notes are decorated using CSS files located at the program root;
  - `ui/global.css`: defines the overall geometry and style for all notes
  - `ui/styles/*`: overrides and extend `global.css` attributes
  - `ui/palettes/*`: handles widgets and icons color schemes
- Users can extend those with custom palettes and styles, override or ignore them
- PrimeNote adds its own CSS selector `NoteDecorations` for enhanced customization

## Console mode
- In this mode, the text box is replaced with a native terminal emulator
- When a [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) is found, the file content is automatically executed in the terminal
- More QTermWidget color schemes can be added into `ui/terminal`
- For more details, see [QTermWidget GitHub Project page](https://github.com/lxqt/qtermwidget)

## Vim mode
- Provides a fully featured Vim instance in every note
- System-independent `vimrc` file and theme files
- Two-way communication between Vim servers and PrimeNote command-line interface
- Default settings allow for a seamless design between the text editing modes

## Virtual machine support
PrimeNote can be used simultaneously across two operating systems (OS). Thus, one can share a note folder with another user, a backup server or a virtual machine.<br/>

PrimeNote fully supports symbolic links (symlinks) on Linux, and partially on Windows. Hence, all notes can be stored in a remote location simply by replacing the notes repository folder with a symlink. Likewise, a symlink can be added into the repository. On Windows, however, please note that shortcuts do not equal symlinks, which require administrator privileges. Thankfully, PrimeNote provide a utility to ease the addition of symlinks into the note repository.

**Virtual machine**
- Create a symlink to the host notes repository
- Place it into a folder shared with the client machine
- On the client side, open a PrimeNote instance and right click on the tray icon
- Select `Open in a file manager`
- Replace the opened folder by the symlink, or add the symlink into it

**Limitations**
- `Rename` and `move` operations on symlinks will behave unexpectedly if used across two OS
- Nested symlinks are not yet supported on Windows

<br/>

# Issues and bugs report
PrimeNote has been developed for X11 and Windows 7-10. Wayland is not currently supported. If you encounter any bugs, please report them in the [issues](https://gitlab.com/william.belanger/primenote/-/issues) section, including the last session log. Logs can be located at `~/.config/primenote/logs` on Linux and `C:\Users\<user>\primenote\logs` on Windows.

<br/>

# Contribution
We would welcome assistance from graphic artists to create a logo, banner, and corresponding application icon.
<br/>Python developers are encouraged to contribute unit tests.
<br/>Your [donations](https://www.paypal.com/donate?hosted_button_id=7UTK3HPH6Q5DG) are greatly appreciated and help cover hosting costs.
