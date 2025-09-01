<p align="center">
  <img src="https://github.com/RandomX42069/AS-AvalonShell/blob/main/SLogo.png" alt="AS-AvalonShell Logo" width="600"/>
  <br/>
  <em>AvalonShell - Hybrid Shell</em>
</p>

## What is AvalonShell?

AvalonShell is a **hybrid shell** (Unix-simplified + Windows + custom commands) with powerful features:

1. **Multi-path Support:**  
   Use `slots` to store paths. Switch between slots 1–10 with the built-in `slot` command.  
   Create unlimited custom slots with `newslot`, switch with `cslot`, and update or change directory with `scd`.

2. **Shell Linking:**  
   Use `slink` to execute commands and arguments in other shells like `cmd.exe` on **Windows** or `gnome-terminal` on **Linux/macOS**.

3. **Clipboard Paste:**  
   Use the `paste` command to directly paste clipboard content into AvalonShell.

4. **Run File:**  
   Two built-in commands:  
   - `runfile` – run a file containing AvalonShell instructions.  
   - `runsel` – open a file dialog to select a file containing instructions (QOL improvement over `runfile`).

5. **Admin Privileges:**  
   Use `admin` to relaunch AvalonShell with elevated privileges.

6. **SysAdmin-Friendly Symbols:**  
   Supports Bash-like symbols: `||`, `&&`, `&`, `;` for familiar scripting and automation.

---

## How to Set Up AvalonShell

### Software Requirements
[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://www.python.org/)  
[![PyInstaller](https://img.shields.io/badge/PyInstaller-Module-blue?logo=python)](https://pyinstaller.org/en/stable/) (**optional** for building executables)

### Build Executable with PyInstaller
```powershell
python -m PyInstaller AvalonShell.py
# Optional: include an icon for a cooler look
python -m PyInstaller -i icon.ico AvalonShell.py
