from pathlib import Path
import platform, os, shutil, re, sys, textwrap, threading, subprocess as sub
import getpass as gpass

from colorama import Fore, Back, Style, init
from urllib.parse import urljoin, urlparse
import requests
import pyperclip
import keyboard
import tkinter as tk
import ctypes
import time
import zipfile
from tkinter import ttk
from tkinter import filedialog


import datetime

init(autoreset=True)

def set_title(title):
    if platform.system() == "Windows":
        os.system(f"title {title}")
    else:
        # For Linux / macOS terminals that support ANSI escape codes
        print(f"\33]0;{title}\a", end="", flush=True)

P_dir = Path(__file__).resolve()
set_title(P_dir)

class Extensions:
    def __init__(self, name="Extension"):
        self.name = name
    class PassiveExtension:
        def __init__(self, code: str = ""):
            self.lines = code.splitlines()
            for each in self.lines:
                try:
                    exec(each)
                except Exception as e:
                    print(f"Error while executing passive extension: {e}")

class ShellUtility:
    def __init__(self):
        self.name = "AvalonShell"

    def boxPrint(self, text: str, width: int = 40):
        # Top border
        print("#" * width)

        # Wrap and print each line inside the box
        for line in text.splitlines():
            wrapped = textwrap.wrap(line, width=width - 4)
            if not wrapped:
                print(f"# {' ' * (width - 4)} #")  # empty line handling
            else:
                for wline in wrapped:
                    print(f"# {wline.ljust(width - 4)} #")

        # Bottom border
        print("#" * width)
    def endLine(self, text:str, msg:str, TextAndMSGspliter="-", spacing:int=1, spacechar:str=" "):
        msg = textwrap.fill(msg, )
        return f"{text}{f"{spacechar}" * spacing}{TextAndMSGspliter}{f"{spacechar}" * spacing}{msg}"

class Shell:


    def __init__(self, slot_dir=None):
        # Initialize slot directories
        self.name = "AvalonShell"
        self.home = os.path.abspath("home")
        self.main = slot_dir or os.path.abspath(".")
        self.secondary = self.main
        self.third = self.main
        self.fourth = self.main
        self.fifth = self.main
        self.sixth = self.main
        self.seventh = self.main
        self.eighth = self.main
        self.nineth = self.main
        self.tenth = self.main
        self.slots = {}
        self.cuslot = ""
        self.crr_dir = self.home  # current directory for the prompt
        self.version = "0.1.0"
        self.variables = {
            "MAIN": self.main,
            "SECOND": self.secondary,
            "THIRD": self.third,
            "FOURTH": self.fourth,
            "FIFTH": self.fifth,
            "SIXTH": self.sixth,
            "SEVENTH": self.seventh,
            "EIGHTH": self.eighth,
            "NINETH": self.nineth,
            "TENTH": self.tenth,
            "USER": os.environ.get("USERNAME", "Unknown"),
            "HOME": self.home,
            "SLOT_TARGET": 1,
            "CLIPBOARD": self.paste(),
            "RECYCLE.BIN": os.path.abspath(r"C:/$Recycle.Bin") if os.path.exists(r"C:/$Recycle.Bin") else os.path.abspath(r"D:/$Recycle.Bin"),
            "SHELL": "AvalonShell",
        }
        self.webs = {
            "python": "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe",
            "qemu": "https://qemu.weilnetz.de/w64/qemu-w64-setup-20250819.exe",
        }
        
        self.ferr = Fore.LIGHTRED_EX
        self.fargs = Fore.LIGHTYELLOW_EX
        self.fsuccess = Fore.LIGHTGREEN_EX
        self.fcmd = Fore.LIGHTBLUE_EX
        self.fser = Fore.LIGHTMAGENTA_EX

        self.util = ShellUtility()
        self.root = tk.Tk()
        self.root.withdraw()
        self.touHouFacts = [
            f"fun fact: if you ever played {Fore.MAGENTA}touhou{Fore.RESET} {self.ferr}hardest difficulty{Fore.RESET}, you'll never see the background again"
        ]
        self.totalCMDs = ""
        self.extension = Extensions()


    os.makedirs("home", exist_ok=True)


    def loadExt(self):
        startPasExt = self.extension.PassiveExtension


    def returnerCMD(self):
        full = self.totalCMDs.strip()
        partis = full.split()
        cmd = partis[0]
        args = partis[1:]

        returned = ""
        try:
            # detect redirection operator in args
            operator = None
            idx = len(args)
            if ">>" in args:
                operator = ">>"
                idx = args.index(">>")
            elif ">" in args:
                operator = ">"
                idx = args.index(">")
            elif "&&" in args:
                operator = "&&"
                idx = args.index("&&")
            elif "&" in args:
                operator = "&"
                idx = args.index("&")
            elif ";" in args:
                operator = ";"
                idx = args.index(";")


            # commands
            if cmd in ("cd", "scd"):
                returned = args[0] if idx > 0 else ""

            elif cmd == "cat":
                if idx > 0:
                    file_path = os.path.join(self.crr_dir, args[0])
                    with open(file_path, "r", encoding="utf-8") as f:
                        returned = f.read()

            elif cmd == "chmod":
                if idx >= 2:
                    file_path = os.path.join(self.crr_dir, args[0])
                    mode = args[1]
                    returned = f"Changed mode of {file_path} to {mode}"

            elif cmd == "chown":
                if idx >= 3:
                    file_path = os.path.join(self.crr_dir, args[0])
                    user, group = args[1], args[2]
                    returned = f"Changed owner of {file_path} to {user}:{group}"

            elif cmd in ("c", "cls", "clear"):
                returned = ""  # clearscreen placeholder

            elif cmd == "cp":
                if idx >= 2:
                    file = os.path.join(self.crr_dir, args[0])
                    dest = args[1]
                    returned = f"Copy {file} -> {dest}"

            elif cmd == "df":
                import psutil
                disk = "/"  # portable default
                if not os.path.exists(disk):
                    return f"{self.ferr}Disk {disk} does not exist{Fore.RESET}"
                usage = psutil.disk_usage(disk)
                returned = (f"{self.fcmd}Disk {disk}{Fore.RESET}\n"
                            f"Total: {usage.total} bytes, Used: {usage.used}, "
                            f"Free: {usage.free}, Usage: {usage.percent}%")

            elif cmd == "download":
                if idx >= 2:
                    url, file = args[0], args[1]
                    returned = f"Download {url} -> {file}"

            elif cmd == "install":
                if idx >= 1:
                    returned = f"Install {args[0]}"

            elif cmd == "du":
                returned = f"Directory: {self.crr_dir} Use: {os.path.getsize(self.crr_dir)}"

            elif cmd == "echo":
                if operator:
                    returned = " ".join(args[:idx]) if idx > 0 else ""
                else:
                    returned = " ".join(args) if args else ""

            elif cmd == "exit":
                returned = "exit"


            elif cmd == "grep":
                if len(args) >= 2:
                    returned = f"{args[0]} {os.path.join(self.crr_dir, args[1])}"
                else:
                    returned = "Missing Tokens"


            elif cmd == "kill":
                if len(args) >= 1:
                    returned = f"{args[0]}"
                else:
                    returned = f"Missing Tokens"

            
            elif cmd in ("less", "view"):
                if len(args) >= 1:
                    returned = f"{os.path.join(self.crr_dir, args[1])}"
                else:
                    returned = f"Missing Tokens"

            
            elif cmd in ("listdir", "ls", "dir"):
                if len(args) >= 1:
                    returned = f"{"\n".join(os.listdir(self.crr_dir))}"
                else:
                    returned = f"Missing Tokens"


            elif cmd == "mkdir":
                if len(args) >= 1:
                    lift = 0
                    for arg in args:
                        if arg in ("-p", "-P"):
                            lift += 1
                    for each in args[lift:]:
                        path = os.path.join(self.crr_dir, each)
                        returned += f"{path}\n"
                else:
                    returned = f"Missing Tokens"
            
            elif cmd in ("mv", "move", "mov"):
                if len(args) >= 2:
                    file = args[0]
                    directory = args[1]
                    returned += f"{file} -> {directory}"
                else:
                    returned = f"Missing Tokens"

            elif cmd == "nano":
                if len(args) >= 1:
                    returned = f"nano {args[0]}"
                else:
                    returned = f"Missing Tokens"

            elif cmd == "newvar":
                if len(args) >= 2:
                    returned = f"{args[0]}: {args[1]}"
                else:
                    returned = f"Missing Tokens"

            
            elif cmd == "oshost":
                if len(args) >= 1:
                    if len(args) >= 2: # if are there any extra args if the host
                        returned = f"{args[0]}: {" ".join(args[1:])}"
                    else:
                        returned = f"{args[0]}"
            

            elif cmd == "paste":
                returned = "Paste"


            elif cmd == "printvar":
                returned = self.variables

            
            elif cmd == "ps":
                try:
                    system = platform.system()
                    if system == "Windows":
                        result = sub.run(["tasklist"], text=True, capture_output=True)
                        returned += result
                    else:
                        # Unix/Linux/Mac
                        result = sub.run(["ps", "aux"], text=True, capture_output=True)
                        returned += result
                except Exception as e:
                    returned += e


            elif cmd == "pwd":
                returned += os.getcwd()


            elif cmd == "pbf":
                if len(args) >= 1:
                    returned += f"{args[0]}"
                else:
                    returned += "Missing Tokens"

            
            elif cmd in ("rename", "ren"):
                if len(args) >= 2:
                    returned += f"{args[0]} - {args[1]}"
                else:
                    returned += f"Missing tokens"


            elif cmd == "rm":
                if len(args) >= 1:
                    returned += f"{args[0]}"
                else:
                    returned += "Missing Tokens"


            elif cmd == "rmdir":
                if len(args) >= 1:
                    returned += f"{args[0]}"
                else:
                    returned += "Missing Tokens"

            
            elif cmd in ("r", "run"):
                if len(args) >= 1:
                    returned += f"{" ".join(args[0:])}"
                else:
                    returned += "Missing Tokens"


            elif cmd == "runfile":
                if len(args) >= 1:
                    returned += f"{args[0]}"
                else:
                    returned += "Missing Tokens"

            
            elif cmd == "runsel":
                returned = "the file you selected"

            
            elif cmd == "setvar":
                if len(args) >= 2:
                    returned += f"{args[0]}: {args[1]}"
                else:
                    returned += "Missing Tokens"

            
            elif cmd == "slink":
                if len(args) >= 2:
                    returned += f"{args[0]}: {" ".join(args[1:])}"
                else:
                    returned += "Missing Tokens"


            elif cmd in ("slot", "cslot"):
                if len(args) >= 2:
                    returned += f"S: {args[0]}"
                else:
                    returned += "Missing Tokens"
            

            elif cmd == "shows":
                returned += f"S: {self.variables["SLOT_TARGET"]}"
            

            elif cmd == "newslot":
                if len(args) >= 1:
                    returned += f"NS: {args[0]}"
                else:
                    returned += "Missing Tokens"

            
            elif cmd == "printslot":
                returned += f"{self.variables["SLOT_TARGET"]}"
                for each, value in self.slots.items():
                    returned += f"{each}: {value}"


            elif cmd == "admin":
                returned += "admin"


            elif cmd == "w":
                if len(args) >= 2:
                    returned += f"{args[0]}: {" ".join(args[1:])}"
                else:
                    returned += "Missing Tokens"


            elif cmd in ("title", "name"):
                if len(args) >= 1:
                    returned += f"ASPN: {args[0]}"
                else:
                    returned += "Missing Tokens"

            
            elif cmd in ("touch", "tou", "touhou"):
                if len(args) >= 1:
                    returned += f"{" ".join(args[0:])}"
                else:
                    returned += "Missing Tokens"


            elif cmd == "loop":
                if len(args) >= 3:
                    returned += f"{args[0]} - {args[1]} - {" ".join(args[2:])}"
                else:
                    returned += "Missing Tokens"


            elif cmd in ("spec", "specs"):
                platformOS = platform.system()
                if platformOS == "Windows":
                    win = platform.uname()
                    returned += f"""                      
                             ....:..                   
              .....::---==+++*****+.        System      :       {win.system}          
 ...::---===++**=.=***************+.        Version     :       {win.version}             
.=**************+.=***************+.        Machine     :       {win.machine}                  
.=**************+.=***************+.        Processor   :       {win.processor}
.=**************+.=***************+.        Node        :       {win.node}          
.=**************+.=***************+.        User        :       {gpass.getuser()}           
.=**************+.=***************+.        Python      :       {sys.version.split()[0]}           
.=**************+.=***************+. 
.:--------------:.:---------------:.                   
.-==============-.:===============-.                   
.=**************+.=***************+.                   
.=**************+.=***************+.                   
.=**************+.=***************+.                   
.=**************+.=***************+.                   
.=**************+.=***************+.                   
.=**************+.=***************+.                   
 ...:::--===++**=.=***************+.                   
               ....::---==+++*****+.                   
                             ....:..                         
"""

                else:
                    
                    linux = platform.uname()
                    returned += f"""
                     ████████               System      :       {linux.system}            
                   ████████████             Version     :       {linux.version}               
                  ███████████▓▓███          Machine     :       {linux.machine}
                 █████████████████          Processor   :       {linux.processor}         
                ███████████████████         Node        :       {linux.node}            
                ██▓▒▒████▓░░▒▓█████         User        :       {gpass.getuser()}          
                ██▒█▓░██▓░██▓░▓████         Python      :       {sys.version.split()[0]}            
                ██▒██░▓▓▒░███ ▓████                     
                ███▒▒░░░░░░░░▒█████                     
                ██▒░░░░░░░░░▒▒██████                    
                █▓▒▒░░░▒▒▒░▒▒███▓▓██                   
                ██▒▒▓▒▒▒▒▒▒░░░░██████                   
               ███░░░▒▒▒░░░    ░███████                 
              ███░  ░░░░░       ▒███████                
              ███░             ░░░████████               
            ████▓▒░░  ░░░  ░░▒▒▒▒▒░█████████             
            ███▓░░             ░░░▒░█████████            
           ███▓░                  ░░░█████████           
          ████░                     ░█████████           
         ████░       ░               ░█████████          
         █████░       ░               ░█████████          
         ████▒       ░░               ░██████████         
         █▒▓█▓       ░░               ░█████████          
        ▒░░░░▓█░      ░            ░░░░███████▓▒          
     ▓▒░░░░░░▒██░░               ░░░░▒██████▒░░░         
    ▒░░░░░░░░░░░░░███▓░            ░░▒▒░▒▒▓▓▓▒▒░░░░         
  ▓▒░░░░░░░░░░░░░░████░            ░▒▒░░░░░░░░░░░░░░       
  ▒░░░░░░░░░░░░░░░▓█▓░           ░▒█▒░░░░░░░░░░░░░░░░     
 █▒░░░░░░░░░░░░░░░░▒░          ░▓██▓▒░░░░░░░░░░░░░░░░     
 ▒░░░░░░░░░░░░░░░░░░▒█▒░░▒▒▒▓██████▓▒░░░░░░░░░░░░▒▓       
██▒▒▒▒▒▒░░░░░░░░░░░▒▒██████████████▓▒▒░░░░░░░▒▓████       
 ██████▓▓▓▓▒▒▒▒▒▒▒▒▒▓██████████████▓▒▒▒▒▒▒▒▓██████        
   ██████████▓▓▓▓▓▓█████████████████▓▓▓▓▓▓██████          
      █████████████           █████████████                  
"""

            elif cmd == "asp":
                returned += f"Python {sys.version}"
            

            elif cmd == "zip":
                if len(args) >= 2:
                    if len(args) >= 2:
                        returned += f"{args[0]}"
                    else:
                        returned += f"{args[0]} - {" ".join(args[1:])}"
                else:
                    returned += "Missing Tokens"

            
            elif cmd == "unzip":
                if len(args) >= 1:
                    returned += f"{" ".join(args[0:])}"
                else:
                    returned += "Missing Tokens"
            

            elif cmd == "#":
                returned = f"{" ".join(args[0:])}"
            else:
                returned = f"Unknown command: {cmd}"

        except Exception as e:
            returned = f"Error: {e}"

        return returned
    



    def redirector(self, mode="w", redirect_file=None):
        # Current command string
        full = self.totalCMDs.strip()
        if not full:
            return  # nothing to do

        # Split into parts
        partis = full.split()
        cmd = partis[0]
        args = partis[1:]

        # Build the file path
        fullpath = os.path.join(self.crr_dir, redirect_file)

        # Prepare what to write
        willWrite = ""
        if ">" in args or ">>" in args:
            try:
                willWrite += self.returnerCMD()
            except Exception as e:
                willWrite += f"Error: {e}"
        else:
            willWrite = ""

        # Write to file
        try:
            with open(fullpath, mode, encoding="utf-8") as f:
                f.write(willWrite + "\n")  # optional newline
        except Exception as e:
            print(f"{Fore.RED}Redirect error: {e}{Fore.RESET}") 



    def symbolical_Executor(self):
        # Step 1: Split top-level commands by ';' (lowest precedence, always execute)
        semi_segments = [seg.strip() for seg in self.totalCMDs.split(";")]

        for semi_seg in semi_segments:
            # Step 2: Split by '&' for parallel execution
            parallel_segments = [seg.strip() for seg in semi_seg.split("&")]

            threads = []

            def run_segment(segment):
                # Step 3: Handle '||' (lower precedence) with '&&' (higher precedence inside)
                or_segments = [seg.strip() for seg in segment.split("||")]

                for or_seg in or_segments:
                    # Split each '||' segment by '&&' (highest precedence)
                    and_commands = [cmd.strip() for cmd in or_seg.split("&&")]

                    success = True
                    for cmd in and_commands:
                        success = self.parse(cmd)  # your parser returns True/False
                        if not success:
                            break  # stop '&&' chain on first failure

                    if success:
                        break  # stop '||' chain on first success

            # Step 4: Start all parallel threads
            for seg in parallel_segments:
                t = threading.Thread(target=run_segment, args=(seg,))
                t.start()
                threads.append(t)

            # Step 5: Wait for all parallel threads to finish
            for t in threads:
                t.join()




    def showsc(self):
        stdslot = "MAIN"
        match self.variables["SLOT_TARGET"]:
            case 1:
                stdslot = "MAIN"
            case 2:
                stdslot = "SECONDARY"
            case 3:
                stdslot = "THIRD"
            case 4:
                stdslot = "FOURTH"
            case 5:
                stdslot = "FIFTH"
            case 6:
                stdslot = "SIXTH"
            case 7:
                stdslot = "SEVENTH"
            case 8:
                stdslot = "EIGHTH"
            case 9:
                stdslot = "NINETH"
            case 10:
                stdslot = "TENTH"
        crrslot = textwrap.fill(f"{Fore.MAGENTA}{stdslot}{Fore.RESET}", width=80)
        csslot  = textwrap.fill(f"{Fore.MAGENTA}{self.cslot}{Fore.RESET}", width=80)
        print(f"Current standard slots: {crrslot} \nCurrent custom slot: {csslot}")
        return f"Current standard slots: {crrslot} \nCurrent custom slot: {csslot}"


    def human_size(self, size):
        """Convert bytes into human-readable units automatically."""
        for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
            if size < 1024 or unit == "PB":  # stop at PB
                return f"{size:.1f} {unit}"
            size /= 1024


    def zip(self, archive_name, *files):
        """Create a ZIP archive with the given files."""
        archive_path = os.path.join(self.crr_dir, archive_name)
        try:
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for each in files:
                    file_path = os.path.join(self.crr_dir, each)
                    if os.path.exists(file_path):
                        zipf.write(file_path, arcname=os.path.basename(file_path))
                    else:
                        print(f"Warning: {each} not found, skipping.")
            print(f"{Fore.LIGHTGREEN_EX}Created ZIP archive:{Fore.RESET} {self.fargs}{archive_path}{Fore.RESET}")
            return archive_path
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Error creating ZIP archive: {e}{Fore.RESET}")


    def unzip(self, archiveName, outputDir=None, targetFiles=None):
        archPath = os.path.join(self.crr_dir, archiveName)

        # Validate archive
        if not os.path.exists(archPath):
            print(f"{Fore.RED}Error:{Fore.RESET} Archive doesn't exist: {archPath}")
            return

        # Default outputDir → same name as archive (without .zip)
        if outputDir is None:
            baseName = os.path.splitext(archiveName)[0]
            outputDir = os.path.join(self.crr_dir, baseName)

        # Ensure outputDir exists
        if not os.path.exists(outputDir):
            print(f"{Fore.MAGENTA}Exception:{Fore.RESET} Output directory does not exist: {outputDir}")
            print(f"Creating directory for extraction…")
            os.makedirs(outputDir, exist_ok=True)

        try:
            with zipfile.ZipFile(archPath, 'r') as zip_ref:
                if targetFiles:  # Extract only selected files
                    for file in targetFiles:
                        if file in zip_ref.namelist():
                            zip_ref.extract(file, outputDir)
                            print(f"Extracted: {file}")
                        else:
                            print(f"{Fore.YELLOW}Warning:{Fore.RESET} File not found in archive: {file}")
                else:  # Extract all
                    zip_ref.extractall(outputDir)
                    print(f"Extracted all files to: {outputDir}")
                return outputDir
        except Exception as e:
            print(f"{Fore.RED}Error during extraction:{Fore.RESET} {e}")


    def pbf(self, fileName: str, length: int = 512, pureBinary: bool = False):
        """Print binary contents of a file."""
        if length > 1028:
            print(f"{Fore.LIGHTRED_EX}File length cannot exceed 1028!{Fore.RESET}")
            return None

        full = os.path.join(self.crr_dir, fileName)

        if not os.path.exists(full):
            print(f"{Fore.LIGHTRED_EX}File doesn't exist: {full}{Fore.RESET}")
            return f"File doesn't exist: {full}"
        if not os.path.isfile(full):
            print(f"{Fore.LIGHTRED_EX}The target isn't a file: {full}{Fore.RESET}")
            return f"The target isn't a file: {full}"

        with open(full, "rb") as f:
            binary = f.read()

        if pureBinary:
            # Show hex bytes
            hexed = " ".join(f"{b:02X}" for b in binary[:length])
            print(hexed)
            return hexed
        else:
            # Show raw bytes (decoded safely)
            print(binary[:length])
            return binary[:length]


    def edit(self, file: str):
        system = platform.system()
        fullPath = os.path.join(self.crr_dir, file)
        if system == "Windows":
            sub.Popen(["notepad.exe", fullPath])
        elif system == "Linux":
            sub.Popen(["nano", fullPath])  # or gedit, xdg-open
        elif system == "Darwin":
            sub.Popen(["open", "-e", fullPath])
        else:
            print("Unsupported system for edit command")
        
    def AdminShell(self):
        if ctypes.windll.shell32.IsUserAnAdmin():
            print(f"{self.fser}AvalonReports: {Fore.RESET}{self.fcmd}Running{Fore.RESET} {self.ferr}Avalon{Fore.LIGHTWHITE_EX}Shell with {Fore.RESET}{Fore.LIGHTCYAN_EX}Admin privileges.{Fore.RESET}")
            print(f"{self.fser}AvalonReports: {Fore.RESET}{self.ferr}Avalon{Fore.LIGHTWHITE_EX}Shell is now running as an Admin{Fore.RESET}")
            print(f"{self.fser}AvalonReports: {Fore.RESET}{self.ferr}CAUTION:{Fore.LIGHTWHITE_EX} Deleting OS's files can result in a full reinstall{Fore.RESET}")
        else:
            print(f"{self.fser}AvalonReports: {Fore.RESET}{self.ferr}Host User is not an Admin!")
            time.sleep(1.0)
            print(f"{self.fser}AvalonReports: {Fore.RESET}Relaunching {self.ferr}Avalon{Fore.LIGHTWHITE_EX}Shell with {Fore.RESET}{Fore.LIGHTCYAN_EX}Admin Privileges...{Fore.RESET}")
            
            ret = ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            if ret <= 32:
                print(f"{Fore.LIGHTRED_EX}Admin relaunch cancelled{Fore.RESET}")
            else:
                print(f"{self.fser}AvalonReports: {Fore.RESET}{self.ferr}Avalon{Fore.LIGHTWHITE_EX}Shell is now running with {Fore.RESET}{Fore.LIGHTCYAN_EX}Admin Privileges{Fore.RESET}")
                print(f"{self.fser}AvalonReports: {Fore.RESET}{self.ferr}CAUTION:{Fore.LIGHTWHITE_EX} Deleting OS's files can result in a {Fore.RESET}{Fore.LIGHTCYAN_EX}full reinstall{Fore.RESET}")

                sys.exit() # stop non-admin privileges process

    def python313(self, file: str = None):
        """Run a Python file or open a Python REPL in a new terminal window."""

        # If no file provided -> open REPL
        if not file:
            system = platform.system()
            try:
                if system == "Windows":
                    sub.Popen(
                        ["start", "cmd", "/k", sys.executable],
                        shell=True
                    )
                elif system == "Linux":
                    sub.Popen(
                        ["gnome-terminal", "--", sys.executable]
                    )
                elif system == "Darwin":  # macOS
                    sub.Popen(
                        ["osascript", "-e", f'tell app "Terminal" to do script "{sys.executable}"']
                    )
                else:
                    print(f"{self.ferr}Unsupported OS for REPL launch{Fore.RESET}")
            except Exception as e:
                print(f"{self.ferr}Error opening REPL: {e}{Fore.RESET}")
            return

        # Otherwise, run a file normally
        fullPath = os.path.join(self.crr_dir, file)

        if not os.path.exists(fullPath):
            print(f"{self.ferr}File does not exist: {fullPath}{Fore.RESET}")
            return
        if not os.path.isfile(fullPath):
            print(f"{self.ferr}Not a file: {fullPath}{Fore.RESET}")
            return
        if not file.endswith(".py"):
            print(f"{self.ferr}Target file isn't a python file: {file}{Fore.RESET}")
            return

        try:
            sub.run([sys.executable, fullPath], check=True)
        except sub.CalledProcessError as e:
            print(f"{self.ferr}Script exited with error code {e.returncode}{Fore.RESET}")
        except Exception as e:
            print(f"{self.ferr}Error while running script: {e}{Fore.RESET}")


    def paste(self):
        try:
            text = pyperclip.paste()
            if text:
                print(text)
            else:
                print("(Clipboard is empty)")
            self.variables["CLIPBOARD"] = text
            return text
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Error accessing clipboard: {e}")
            return ""
    
    def rmdir(self, dire: str):
        full_path = os.path.join(self.crr_dir, dire)
        if not os.path.exists(full_path):
            print(f"{self.ferr}Directory does not exist: {full_path}{Fore.RESET}")
            return
        if not os.path.isdir(full_path):
            print(f"{self.ferr}Not a directory: {full_path}{Fore.RESET}")
            return
        try:
            os.rmdir(full_path)
            print(f"{self.fsuccess}Removed directory: {full_path}{Fore.RESET}")
        except OSError:
            print(f"{self.ferr}Directory is not empty or cannot be removed: {full_path}{Fore.RESET}")
    
    
    def cp(self, sources, target_dir=None):
        """
        Copy one or more files from the current directory to a target directory.
        - sources: str or list of filenames
        - target_dir: optional target directory (default: current directory)
        """
        if isinstance(sources, str):
            sources = [sources]  # make it a list for uniform processing
        
        target_dir = os.path.join(self.crr_dir, target_dir)  # default to current directory
        
        if not os.path.exists(target_dir):
            print(f"{self.ferr}Target directory does not exist: {target_dir}{Fore.RESET}")
            return
        if not os.path.isdir(target_dir):
            print(f"{self.ferr}Target is not a directory: {target_dir}{Fore.RESET}")
            return

        for src in sources:
            src_path = os.path.join(self.crr_dir, src)
            if not os.path.exists(src_path):
                print(f"{self.ferr}Source file does not exist: {src_path}{Fore.RESET}")
                continue
            if not os.path.isfile(src_path):
                print(f"{self.ferr}Source is not a file: {src_path}{Fore.RESET}")
                continue
            
            target_path = os.path.join(target_dir, os.path.basename(src))
            if os.path.exists(target_path):
                print(f"{self.ferr}Target file already exists: {target_path}{Fore.RESET}")
                continue

            try:
                shutil.copy2(src_path, target_path)
                print(f"{self.fsuccess}Copied {src_path} -> {target_path}{Fore.RESET}")
            except Exception as e:
                print(f"{self.ferr}Error copying {src_path}: {e}{Fore.RESET}")


    def writeto(self, filename, text:str):
        path = os.path.join(self.crr_dir, filename)
        if not os.path.exists(path):
            print(f"{self.ferr}Error: file doesn't exist: {filename}{Fore.RESET}")
        elif not os.path.isfile(path):
            print(f"{self.ferr}Error: Target isn't a file: {filename}{Fore.RESET}")
        
        
        try:
            with open(path, "w") as f:
                f.write(str(" ".join(text))) 
        except UnicodeError:
            print("File contain non printable characters")


    def mv(self, file: str, dest: str):
        src_path = os.path.join(self.crr_dir, file)
        if not os.path.exists(src_path):
            print(f"{self.ferr}File does not exist: {file}{Fore.RESET}")
            return
        if not os.path.isfile(src_path):
            print(f"{self.ferr}Source is not a file: {file}{Fore.RESET}")
            return

        dest_path = os.path.join(self.crr_dir, dest)
        # If dest is a directory, move file into it
        if os.path.isdir(dest_path):
            dest_path = os.path.join(dest_path, os.path.basename(file))
        else:
            # If dest's parent directory does not exist, warn
            parent_dir = os.path.dirname(dest_path)
            if not os.path.exists(parent_dir):
                print(f"{self.ferr}Destination directory does not exist: {parent_dir}{Fore.RESET}")
                return

        try:
            shutil.move(src_path, dest_path)
            print(f"{self.fsuccess}Moved {src_path} -> {dest_path}{Fore.RESET}")
        except FileExistsError:
            print(f"{self.ferr}File already exists at destination: {dest_path}{Fore.RESET}")
        except Exception as e:
            print(f"{self.ferr}Error moving file: {e}{Fore.RESET}")

    
    
    def chown(self, fileName: str, user: str, group: str = None):
        """
        Change file owner (and optionally group) on Unix or Windows.
        - fileName: file in self.crr_dir
        - user: new owner
        - group: new group (only relevant on Unix)
        """
        full_path = os.path.join(self.crr_dir, fileName)
        if not os.path.exists(full_path):
            print(f"{self.ferr}File does not exist: {full_path}{Fore.RESET}")
            return

        system = platform.system()
        try:
            if system in ("Linux", "Darwin"):  # Unix-like
                import pwd, grp
                uid = pwd.getpwnam(user).pw_uid
                gid = os.stat(full_path).st_gid  # default: keep current group
                if group:
                    gid = grp.getgrnam(group).gr_gid
                os.chown(full_path, uid, gid)
                print(f"{self.fsuccess}Ownership of {fileName} changed to {user}:{group or ''}{Fore.RESET}")
            elif system == "Windows":
                # Use icacls to set ownership
                cmd = ["icacls", full_path, "/setowner", user]
                sub.run(cmd, shell=True)
                print(f"{self.fsuccess}Ownership of {fileName} set to {user} (Windows){Fore.RESET}")
            else:
                print(f"{self.ferr}Unsupported OS: {system}{Fore.RESET}")
        except PermissionError:
            print(f"{self.ferr}Permission denied. You may need admin/root privileges.{Fore.RESET}")
        except Exception as e:
            print(f"{self.ferr}Error changing ownership: {e}{Fore.RESET}")

    # Change directory
    def CD(self, path):
        path = os.path.expanduser(path)

        # If absolute path given, keep it. Else, check inside current dir
        if path.startswith(".-"):
            check = os.listdir(self.crr_dir)
            fullcheck = os.path.join(self.crr_dir, check[0])
            if not len(check) == 1:
                print(f"{self.ferr}The current directory doesn't have exactly 1 item{Fore.RESET}")
                return None
            elif not os.path.isdir(fullcheck):
                print(f"{self.ferr}The only item inside the current directory is not a directory{Fore.RESET}")
                return None
            print(f"{Fore.GREEN}Entering the only dir in the current directory: {fullcheck}{Fore.RESET}")

            abspath = os.path.join(self.crr_dir, check[0])
            self.crr_dir = abspath

            slot = self.variables.get("SLOT_TARGET", 1)
            try:
                slot = int(slot)
            except ValueError:
                print(self.ferr + f"Invalid SLOT_TARGET value: {slot}. Must be 1, 2, ..., 10.")
                return None

            if slot == 1:
                self.main = abspath
                self.variables.update({"MAIN": abspath})
            elif slot == 2:
                self.secondary = abspath
                self.variables.update({"SECOND": abspath})
            elif slot == 3:
                self.third = abspath
                self.variables.update({"THIRD": abspath})
            elif slot == 4:
                self.fourth = abspath
                self.variables.update({"FOURTH": abspath})
            elif slot == 5:
                self.fifth = abspath
                self.variables.update({"FIFTH": abspath})
            elif slot == 6:
                self.sixth = abspath
                self.variables.update({"SIXTH": abspath})
            elif slot == 7:
                self.seventh = abspath
                self.variables.update({"SEVENTH": abspath})
            elif slot == 8:
                self.eighth = abspath
                self.variables.update({"EIGHTH": abspath})
            elif slot == 9:
                self.nineth = abspath
                self.variables.update({"NINETH": abspath})
            elif slot == 10:
                self.tenth = abspath
                self.variables.update({"TENTH": abspath})
            else:
                print(self.ferr + f"Unknown slot: {slot}")
                return None
            
            return abspath

        if path.startswith(".$"):
            repeat = path.count("$")
            for _ in range(repeat):
                spalt = Path(self.crr_dir)
                if spalt.parent == spalt:  # Already at root
                    print(self.ferr + "Directory depth is global")
                    break
                self.crr_dir = str(spalt.parent)

        elif path == ".":
            if os.name == "nt":  # Windows
                self.crr_dir = str(Path("D:/") if Path("D:/").exists() else Path("C:/"))
            else:  # Linux/Mac
                self.crr_dir = str(Path.home())
        else:
            if os.path.isabs(path) or (len(path) == 2 and path[1] == ":"):
                abs_path = os.path.normpath(path)
            else:
                abs_path = os.path.normpath(os.path.join(self.crr_dir, path))

            if not os.path.isdir(abs_path):
                print(self.ferr + f"Path does not exist: {abs_path}")
                return None

            # Update current dir immediately
            self.crr_dir = abs_path

            slot = self.variables.get("SLOT_TARGET", 1)
            try:
                slot = int(slot)
            except ValueError:
                print(self.ferr + f"Invalid SLOT_TARGET value: {slot}. Must be 1, 2, ..., 10.")
                return None

            if slot == 1:
                self.main = abs_path
                self.variables.update({"MAIN": abs_path})
            elif slot == 2:
                self.secondary = abs_path
                self.variables.update({"SECOND": abs_path})
            elif slot == 3:
                self.third = abs_path
                self.variables.update({"THIRD": abs_path})
            elif slot == 4:
                self.fourth = abs_path
                self.variables.update({"FOURTH": abs_path})
            elif slot == 5:
                self.fifth = abs_path
                self.variables.update({"FIFTH": abs_path})
            elif slot == 6:
                self.sixth = abs_path
                self.variables.update({"SIXTH": abs_path})
            elif slot == 7:
                self.seventh = abs_path
                self.variables.update({"SEVENTH": abs_path})
            elif slot == 8:
                self.eighth = abs_path
                self.variables.update({"EIGHTH": abs_path})
            elif slot == 9:
                self.nineth = abs_path
                self.variables.update({"NINETH": abs_path})
            elif slot == 10:
                self.tenth = abs_path
                self.variables.update({"TENTH": abs_path})
            else:
                print(self.ferr + f"Unknown slot: {slot}")
                return None

            return abs_path

    # Make directories
    def mkdir(self, Parent=False, *args):
        if not args:
            print(self.ferr + "mkdir requires at least one directory argument")
            return

        if Parent:
            for dirN in args:
                try:
                    parts = Path(self.crr_dir, dirN).parts
                    path = ""
                    for part in parts:
                        path = os.path.join(path, part)
                        if not os.path.exists(path):
                            os.mkdir(path)
                            print(f"Created: {path}")
                except Exception as e:
                    print(self.ferr + f"Error creating {dirN}: {e}")
        else:
            for dir_name in args:
                fdir = os.path.join(self.crr_dir, dir_name)
                try:
                    os.mkdir(fdir)  # normal single-level mkdir
                    print(f"Created: {fdir}")
                except FileExistsError:
                    print(self.ferr + f"Directory already exists: {fdir}")
                except Exception as e:
                    print(self.ferr + f"Error creating {fdir}: {e}")


    # Remove files/directories
    def rm(self, *args):
        if not args:
            print(self.ferr + "rm requires at least one file or directory argument")
            return
        for target in args:
            ftarget = os.path.join(self.crr_dir, target)
            try:
                if os.path.isfile(ftarget):
                    os.remove(ftarget)
                    print(f"Removed file: {ftarget}")
                elif os.path.isdir(ftarget):
                    shutil.rmtree(ftarget)
                    print(f"Removed directory: {ftarget}")
                else:
                    print(f"Path does not exist: {ftarget}")
            except Exception as e:
                print(self.ferr + f"Error removing {ftarget}: {e}")

    def echo(self, args, col_attr=Fore.WHITE):
        # Convert input to a single string
        if isinstance(args, list):
            args = " ".join(str(a) for a in args)  # join list elements
        else:
            args = str(args)  # ensure string type

        if not args:
            print(self.ferr + "echo requires at least one character")
            return

        # Replace $VARIABLES with shell values
        def ecReplace(match):
            var = match.group(1)
            return self.variables.get(var, "")

        result = re.sub(r"\$([A-Za-z_][A-Za-z0-9_]*)", ecReplace, args)

        print(f"{col_attr}{result}{Style.RESET_ALL}")

    def Program(self, program_name, inputs="", live=True):
        # Use crr_dir as base if path is relative
        full_path = program_name if os.path.isabs(program_name) else os.path.join(self.crr_dir, program_name)

        if not os.path.exists(full_path):
            print(self.ferr + f"Program not found: {full_path}")
            return

        try:
            if live:
                proc = sub.Popen(full_path, text=True, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.STDOUT)
                if inputs:
                    proc.stdin.write(str(inputs))
                    proc.stdin.close()
                for line in proc.stdout:
                    print(line, end="")
                proc.wait()
            else:
                result = sub.run(
                    full_path,
                    input=str(inputs),
                    text=True,
                    capture_output=True
                )
                print(result.stdout)
                if result.stderr:
                    print(self.ferr + result.stderr, file=sys.stderr)

        except Exception as e:
            print(self.ferr + f"Error running program: {e}")



    def setVar(self, var:str, value):
        var = var.upper()
        self.variables[f"{var}"] = value
        if var == "SLOT_TARGET":
            try:
                value = int(value)
                if value not in (1, 2, 3):
                    print(self.ferr + f"Unknown Slot: {value}. Slots must be 1, 2, ..., 10.")
                    return
            except ValueError:
                print(self.ferr + f"Invalid SLOT_TARGET value: {value}. Must be 1, 2, ..., 10.")
                return
            self.variables["SLOT_TARGET"] = value
            self.crr_dir = [self.main, self.secondary, self.third, self.fourth, self.fifth
            ,self.sixth, self.seventh, self.eighth, self.nineth, self.tenth
            ][value - 1]



    def newVar(self, label, value):
        self.variables[f"{label}"] = value



    def printVar(self):
        for key, value in self.variables.items():
            print(f"{self.fargs}{key}{Fore.RESET} {self.fcmd}{value}{Fore.RESET}")



    def slot(self, slot:int=1):
        try:
            slot = int(slot)
            if slot in (1, 2, 3, 4, 5, 6,
                7, 8, 9, 10
            ):
                self.variables.update({"SLOT_TARGET": slot})
                self.crr_dir = [self.main, self.secondary, self.third, self.fourth, self.fifth,
                    self.sixth, self.seventh, self.eighth, self.nineth, self.tenth
                ][slot - 1]
            else:
                print(self.ferr + f"Invalid SLOT_TARGET value: {slot}. Must be 1, 2, ..., 10.")
        except Exception as e:
            print(self.ferr + f"Error: {e}")



    def printslot(self):
        print(f"{self.fargs}Slot Target:{Fore.RESET} {self.variables["SLOT_TARGET"]}")
        print(f"{self.fargs}Custom Slots:{Fore.RESET} \n")
        for each, value in self.slots.items():
            print(f"{self.fcmd}{each}:{Fore.RESET} {self.fargs}{value}{Fore.RESET}")



    def newslot(self, slotname:str, path:str=os.path.abspath("home")):
        self.slots[f"{slotname}"] = path
        print(f"{slotname} slot have been added {self.fsuccess}successfully!{Fore.RESET}")



    def cslot(self, slotname:str):
        abspath = self.slots[f"{slotname}"]
        self.cuslot = f"{slotname}"
        self.crr_dir = abspath



    def scd(self, path:str):
        # If absolute path given, keep it. Else, check inside current dir
        if "$" in path:
            repeat = path.count("$")
            for _ in range(repeat):
                spalt = Path(self.crr_dir)
                if spalt.parent == spalt:  # Already at root
                    print(self.ferr + "Directory depth is global")
                    break
                self.crr_dir = str(spalt.parent)
        elif path == ".":
            if os.name == "nt":  # Windows
                self.crr_dir = str(Path("D:/") if Path("D:/").exists() else Path("C:/"))
            else:  # Linux/Mac
                self.crr_dir = str(Path.home())
        else:
            path = os.path.expanduser(path)

            if os.path.isabs(path) or (len(path) == 2 and path[1] == ":"):
                abs_path = os.path.normpath(path)
            else:
                abs_path = os.path.normpath(os.path.join(self.crr_dir, path))
            if not os.path.isdir(abs_path):
                    print(self.ferr + f"Path does not exist: {abs_path}")
                    return None
            self.crr_dir = abs_path
            self.slots[self.cuslot] = abs_path
        


    def OSHost(self, hostCMD, *hostARGS, live=True):
        full_cmd = [hostCMD] + list(hostARGS)
        try:
            if live:
                proc = sub.Popen(full_cmd, text=True, stdout=sub.PIPE, stderr=sub.STDOUT)
                for line in proc.stdout:
                    print(line, end="")  # stream live output
                proc.wait()
            else:
                result = sub.run(full_cmd, text=True, capture_output=True)
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(self.ferr + result.stderr)
        except Exception as e:
            print(self.ferr + f"Error running host command: {e}")



    def download_to_home(self, URL, target):
        # Ensure your shell has a home folder path
        home_folder = self.home  # e.g., "C:/AvalonShell/Home"
        os.makedirs(home_folder, exist_ok=True)  # create it if it doesn't exist

        # Full path to save file
        save_path = os.path.join(home_folder, target)

        try:
            response = requests.get(URL)
            response.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(self.fsuccess + f"Downloaded to home: {Fore.LIGHTMAGENTA_EX}{save_path}{Fore.RESET}")
        except Exception as e:
            print(self.ferr + f"Error downloading {URL}: {e}")



    def listdir(self, reverse=False, sort_size=False, only_files=False, only_dirs=False, abspath=False):
        entries = os.listdir(self.crr_dir)
        if not entries:
            print(f"{Fore.LIGHTCYAN_EX}{self.crr_dir}:{Fore.RESET} (empty)")
            return
        
        if reverse:
            entries = entries[::-1]
        if sort_size:
            entries = sorted(entries, key=lambda x: os.path.getsize(os.path.join(self.crr_dir, x)))

        if abspath:
            entries = [os.path.abspath(os.path.join(self.crr_dir, e)) for e in entries]

        if only_files:
            entries = [e for e in entries if os.path.isfile(os.path.join(self.crr_dir, e))]
        if only_dirs:
            entries = [e for e in entries if os.path.isdir(os.path.join(self.crr_dir, e))]

        else:
            entries = sorted(entries)

        print(f"{Fore.LIGHTCYAN_EX}{self.crr_dir}:{Fore.RESET}\n" + f"{Fore.YELLOW}" + "\n".join(entries) + f"{Fore.RESET}")


    
    def listdirdetailed(self, 
        reverse=False,
        sort_size=False,
        only_files=False,
        only_dirs=False,
        abspath=False,
        humanReadableSize=False
    ):
        entries = os.listdir(self.crr_dir)
        if not entries:
            print(f"{Fore.LIGHTCYAN_EX}{self.crr_dir}:{Fore.RESET} (empty)")
            return

        if reverse:
            entries = entries[::-1]
        if sort_size:
            entries = sorted(entries, key=lambda x: os.path.getsize(os.path.join(self.crr_dir, x)))

        if abspath:
            entries = [os.path.abspath(os.path.join(self.crr_dir, e)) for e in entries]

        if only_files:
            entries = [e for e in entries if os.path.isfile(os.path.join(self.crr_dir, e))]
        if only_dirs:
            entries = [e for e in entries if os.path.isdir(os.path.join(self.crr_dir, e))]
        else:
            entries = sorted(entries)

        print(f"{Fore.LIGHTCYAN_EX}{self.crr_dir}:{Fore.RESET}")

        for each in entries:
            full_path = os.path.join(self.crr_dir, each)

            # File size (skip for directories)
            if os.path.isfile(full_path):
                size = os.path.getsize(full_path)
                size = self.human_size(size) if humanReadableSize else f"{size} B"
            else:
                size = "-"

            # Modified time
            mtime = datetime.datetime.fromtimestamp(
                os.path.getmtime(full_path)
            ).strftime("%Y-%m-%d %H:%M:%S")

            # Wrap/shorten long text
            wrapped_name = textwrap.shorten(each, width=35, placeholder="…")

            # Neat columns
            print(
                f"{Fore.LIGHTCYAN_EX}{wrapped_name:<35}{Fore.RESET} | " + f"{Fore.YELLOW}",
                f"Size: {str(size):<10} "
                f"Modified: {mtime} "
            )




    def rename(self, target, newName):
        fullPath = os.path.join(self.crr_dir, target)
        newPath = os.path.join(self.crr_dir, newName)

        if not os.path.exists(fullPath):
            print(f"{self.ferr}Error: '{target}' does not exist.")
            return

        if os.path.exists(newPath):
            print(f"{self.ferr}Error: '{newName}' already exists.")
            return

        os.rename(fullPath, newPath)
        print(f"Renamed '{target}' to '{newName}'")



    def Slink(self, shell_name="cmd", shellcmd="", HostShellArgs=""):
        """
        Launch a new shell in a separate window with optional command and extra arguments.
        """
        try:
            if platform.system() == "Windows":
                full_cmd = f'start "" "{shell_name}"'
                if HostShellArgs:
                    full_cmd += f" {HostShellArgs}"
                if shellcmd:
                    full_cmd += f' /k "{shellcmd}"'
                sub.run(full_cmd, shell=True)
            else:
                term = "gnome-terminal"  # or xterm
                args = [term, "--", shell_name]
                if HostShellArgs:
                    args.extend(HostShellArgs.split())
                if shellcmd:
                    args.extend(["-c", shellcmd])
                sub.run(args)

        except Exception as e:
            print(self.ferr + f"Error launching shell '{shell_name}': {e}")


    
    def nano(self, fileName: str):
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Editing {fileName} — Avalon Nano")
        print("(Type text. Ctrl+O = save, Ctrl+X = exit)\n")

        __src__ = []

        while True:
            event = keyboard.read_event(suppress=True)

            if event.event_type == keyboard.KEY_DOWN:
                if event.name == "ctrl+x":
                    print("\nExiting editor...")
                    break
                elif event.name == "ctrl+o":
                    os.makedirs("home/nano", exist_ok=True)
                    with open(f"home/nano/{fileName}", "w") as f:
                        f.write("\n".join(__src__))
                    print(f"\nSaved to home/nano/{fileName}")
                elif event.name == "enter":
                    __src__.append("")
                    print()  # move to new line
                elif event.name == "backspace":
                    if __src__ and __src__[-1]:
                        __src__[-1] = __src__[-1][:-1]
                        print("\b \b", end="", flush=True)  # erase char
                elif len(event.name) == 1:  # normal character
                    if not __src__:
                        __src__.append("")
                    __src__[-1] += event.name
                    print(event.name, end="", flush=True)
    


    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")



    def pwd(self):
        slot = self.variables.get("SLOT_TARGET", 1)
        print(f"{Fore.LIGHTBLUE_EX}Slot {slot} Directory:{Fore.RESET} {self.fargs}{self.crr_dir}{Fore.RESET}")

    

    def touch(self, *fileName):
        for each in fileName:
            file_path = os.path.join(self.crr_dir, each)
            try:
                with open(file_path, "x") as f:
                    f.write("")  # create an empty file
                print(f"{self.fsuccess}Created file: {file_path}{Fore.RESET}")
            except FileExistsError:
                print(f"{self.ferr}File already exists: {file_path}{Fore.RESET}")
            except Exception as e:
                print(f"{self.ferr}Error creating file: {e}{Fore.RESET}")



    def runsel(self):
        self.root = tk.Tk()
        self.root.withdraw()

        file_path = filedialog.askopenfilename(
            title="Select a file to run",
            filetypes=(("AvalonShell scripts", "*.as"), ("All files", "*.*"))
        )

        if not file_path:
            print(self.ferr + "No file selected.")
            return

        file_name = os.path.abspath(file_path)
        self.runfile(file_name)



    def cat(self, fileName, number_lines=False):
        """
        Print the contents of a file.
        - number_lines: if True, prefix each line with its line number
        """
        fullpath = os.path.join(self.crr_dir, fileName)
        if not os.path.exists(fullpath):
            print(f"{self.ferr}File doesn't exist: {fullpath}{Fore.RESET}")
            return
        if not os.path.isfile(fullpath):
            print(f"{self.ferr}The target isn't a file: {fullpath}{Fore.RESET}")
            return
        try:
            with open(fullpath, "r", encoding="utf-8", errors="replace") as f:
                for idx, line in enumerate(f, start=1):
                    line_to_print = line.rstrip()
                    if number_lines:
                        print(f"{idx:4}: {line_to_print}")
                    else:
                        print(line_to_print)
        except Exception as e:
            print(f"{self.ferr}Error reading file {fullpath}: {e}{Fore.RESET}")



    def less(self, fileName, page_lines=20):
        fullpath = os.path.join(self.crr_dir, fileName)
        if not os.path.exists(fullpath):
            print(f"{self.ferr}File doesn't exist: {fullpath}{Fore.RESET}")
            return
        if not os.path.isfile(fullpath):
            print(f"{self.ferr}The target isn't a file: {fullpath}{Fore.RESET}")
            return

        try:
            with open(fullpath, "r") as f:
                lines = f.readlines()
            
            total_lines = len(lines)
            current = 0

            while current < total_lines:
                # Show one page
                for i in range(current, min(current + page_lines, total_lines)):
                    print(lines[i], end="")
                current += page_lines

                if current >= total_lines:
                    break

                # Wait for user input
                user_input = input(f"{self.fargs}--More-- ({current}/{total_lines}){Fore.RESET} ")
                if user_input.lower() in ("q", "quit", "exit"):
                    break

        except Exception as e:
            print(f"{self.ferr}Error reading file: {e}{Fore.RESET}")



    def grep(self, pattern, fileName, ignore_case=False, show_line_number=False):
        """
        Search for a pattern in a file and print matching lines.
        :param pattern: string or regex pattern to search for
        :param fileName: file to search in (from current directory)
        :param ignore_case: if True, ignore case
        :param show_line_number: if True, print line numbers
        """
        fullpath = os.path.join(self.crr_dir, fileName)
        
        if not os.path.exists(fullpath):
            print(f"{self.ferr}File doesn't exist: {fullpath}{Fore.RESET}")
            return
        if not os.path.isfile(fullpath):
            print(f"{self.ferr}The target isn't a file: {fullpath}{Fore.RESET}")
            return

        try:
            with open(fullpath, "r", encoding="utf-8", errors="ignore") as f:
                for i, line in enumerate(f, 1):
                    line_to_check = line
                    if ignore_case:
                        line_to_check = line.lower()
                        pattern = pattern.lower()
                    
                    if pattern in line_to_check:
                        if show_line_number:
                            print(f"{i}: {line.strip()}")
                        else:
                            print(line.strip())
        except Exception as e:
            print(f"{self.ferr}Error reading file: {e}{Fore.RESET}")



    def chmod(self, fileName: str, mode: str):
        """
        Change file permissions.
        - fileName: the target file (in self.crr_dir)
        - mode: either numeric (e.g., '755') or symbolic (e.g., 'u+x')
        """
        full_path = os.path.join(self.crr_dir, fileName)
        if not os.path.exists(full_path):
            print(f"{self.ferr}File does not exist: {full_path}{Fore.RESET}")
            return

        # Handle numeric mode like '755'
        if mode.isdigit() and len(mode) == 3:
            try:
                numeric_mode = int(mode, 8)  # convert from octal
                os.chmod(full_path, numeric_mode)
                print(f"{self.fsuccess}Permissions of {fileName} set to {mode}{Fore.RESET}")
            except Exception as e:
                print(f"{self.ferr}Error setting permissions: {e}{Fore.RESET}")
        else:
            # Optional: symbolic mode support (u+x, g-w, etc.)
            print(f"{self.ferr}Only numeric modes like 644 or 755 are supported for now.{Fore.RESET}")



    def ps(self):
        try:
            system = platform.system()
            if system == "Windows":
                # Windows equivalent
                result = sub.run(["tasklist"], text=True, capture_output=True)
                print(result.stdout)
            else:
                # Unix/Linux/Mac
                result = sub.run(["ps", "aux"], text=True, capture_output=True)
                print(result.stdout)
        except Exception as e:
            print(f"{self.ferr}Error listing processes: {e}{Fore.RESET}")



    def df(self, disk: str = "C:/"):
        import psutil
        if not os.path.exists(disk):
            print(f"{self.ferr}Disk {disk} does not exist{Fore.RESET}")
            return
        usage = psutil.disk_usage(disk)
        print(f"{self.fcmd}Disk {disk}{Fore.RESET}")
        print(f"Total: {usage.total} bytes, Used: {usage.used}\nFree: {usage.free}\nUsage: {usage.percent}%")



    def title(self, name):
        try:
            set_title(name)
            print(f"{self.fcmd}AvalonShell Proccess{Fore.RESET} {self.fargs}Name{Fore.RESET} has been set to {self.fargs}{name}{Fore.RESET} {self.fsuccess}successfully!{Fore.RESET}")
        except UnicodeDecodeError:
            print(f"{self.ferr}Error: Title contain non printable characters{Fore.RESET}")
        except Exception as e:
            print(f"{self.ferr}Error: {e}")



    def kill(self, pid_or_name):
        """
        Kill a process by PID or process name.
        - pid_or_name: int (PID) or str (process name)
        """
        import psutil

        if isinstance(pid_or_name, str) and pid_or_name.isdigit():
            pid_or_name = int(pid_or_name)

        killed_any = False

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if (isinstance(pid_or_name, int) and proc.info['pid'] == pid_or_name) or \
                (isinstance(pid_or_name, str) and proc.info['name'] == pid_or_name):
                    proc.kill()
                    print(f"{self.fsuccess}Killed process {proc.info['name']} (PID {proc.info['pid']}){Fore.RESET}")
                    killed_any = True
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                print(f"{self.ferr}Failed to kill process {proc.info['pid']}: {e}{Fore.RESET}")

        if not killed_any:
            print(f"{self.ferr}No matching process found for '{pid_or_name}'{Fore.RESET}")



    def du(self):
        print(f"{self.fcmd}Directory:{Fore.RESET} {Fore.MAGENTA}{self.crr_dir}{Fore.RESET} {self.fcmd}Use:{Fore.RESET} {self.fargs}{os.path.getsize(self.crr_dir)}{Fore.RESET}")



    def top(self, refresh: float = 2.0, limit: int = 10):
        """
        Display the top running processes by CPU usage.
        - refresh: seconds between updates
        - limit: number of processes to display
        """
        import psutil
        import time
        try:
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print(f"{self.fsuccess}AvalonShell Top Processes (refresh every {refresh}s){Fore.RESET}\n")
                # Gather processes info
                procs = []
                for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                    try:
                        procs.append(p.info)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                # Sort by CPU usage
                procs.sort(key=lambda x: x['cpu_percent'], reverse=True)
                # Print header
                print(f"{'PID':>6} {'CPU%':>6} {'MEM%':>6} {'NAME'}")
                # Print top processes
                for proc in procs[:limit]:
                    print(f"{proc['pid']:>6} {proc['cpu_percent']:>6.1f} {proc['memory_percent']:>6.1f} {proc['name']}")
                print("\nPress Ctrl+C to exit")
                time.sleep(refresh)
        except KeyboardInterrupt:
            print("\nExiting top...")



    def loop(self, loopTimes, cmd, *args):
        if not loopTimes:
            print(self.ferr + f"Error loop times is unknown: {loopTimes}")
            return
        if loopTimes < 0:
            print(self.ferr + f"Error: Loop count must be non-negative: {loopTimes}")
            return
        try:
            for i in range(loopTimes):
                command = cmd + (" " + " ".join(args) if args else "")  # Fixed string joining
                self.parse(command)
        except Exception as e:
            print(self.ferr + f"Error during loop: {e}")



    def install(self, software: str):
        home_folder = self.home
        try:
            # Verify that the requested software exists in your mapping
            if software not in self.webs:
                print(self.ferr + f"Unsupported software: {software}")
                return

            # Define install directory
            install_dir = os.path.join(home_folder, software)
            os.makedirs(install_dir, exist_ok=True)

            # Get download URL
            url = self.webs[software]

            # Extract filename safely from URL
            file_name = os.path.basename(urlparse(url).path)
            if not file_name:  # fallback in case URL has no path
                file_name = f"{software}_installer.exe"

            save_file = os.path.join(install_dir, file_name)

            # Download the installer
            print(self.fsuccess + f"Downloading {software} from {url} ...")
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            with open(save_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(self.fsuccess + f"Saved installer to {save_file}")

            # Run the installer silently
            if software.lower() == "python":
                target_dir = os.path.abspath(install_dir)
                sub.run([
                    save_file,
                    "/quiet",
                    "InstallAllUsers=1",
                    f"TargetDir={target_dir}",
                    "PrependPath=1"
                ], check=True)
                print(self.fsuccess + "Python installed successfully!")

            elif software.lower() == "qemu":
                target_dir = os.path.abspath(os.path.join(home_folder, "qemu"))
                result = sub.run(
                    f'"{save_file}" /S /D={target_dir}',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(self.fsuccess + "QEMU installed successfully!")
                else:
                    print(self.ferr + f"QEMU installer failed with code {result.returncode}")
                    print("STDOUT:", result.stdout)
                    print("STDERR:", result.stderr)
        except Exception as e:
            print(self.ferr + f"Error while installing {software}: {e}")

    def specs(self,):
        if platform.system() == "Windows":
            win = platform.uname()
            print(f"""{Fore.LIGHTBLUE_EX}                         
                             ....:..                   
              .....::---==+++*****+.        {Fore.LIGHTWHITE_EX}System      :       {Fore.LIGHTBLUE_EX}{win.system}{Fore.LIGHTBLUE_EX}            
 ...::---===++**=.=***************+.        {Fore.LIGHTWHITE_EX}Version     :       {Fore.LIGHTBLUE_EX}{win.version}{Fore.LIGHTBLUE_EX}              
.=**************+.=***************+.        {Fore.LIGHTWHITE_EX}Machine     :       {Fore.LIGHTBLUE_EX}{win.machine}{Fore.LIGHTBLUE_EX}                    
.=**************+.=***************+.        {Fore.LIGHTWHITE_EX}Processor   :       {Fore.LIGHTBLUE_EX}{win.processor}{Fore.LIGHTBLUE_EX}
.=**************+.=***************+.        {Fore.LIGHTWHITE_EX}Node        :       {Fore.LIGHTBLUE_EX}{win.node}{Fore.LIGHTBLUE_EX}           
.=**************+.=***************+.        {Fore.LIGHTWHITE_EX}User        :       {Fore.LIGHTBLUE_EX}{gpass.getuser()}{Fore.LIGHTBLUE_EX}           
.=**************+.=***************+.        {Fore.LIGHTWHITE_EX}Python      :       {Fore.LIGHTBLUE_EX}{sys.version.split()[0]}{Fore.LIGHTBLUE_EX}           
.=**************+.=***************+. 
.:--------------:.:---------------:.                   
.-==============-.:===============-.                   
.=**************+.=***************+.                   
.=**************+.=***************+.                   
.=**************+.=***************+.                   
.=**************+.=***************+.                   
.=**************+.=***************+.                   
.=**************+.=***************+.                   
 ...:::--===++**=.=***************+.                   
               ....::---==+++*****+.                   
                             ....:..                         
{Fore.RESET}""")
        else:
            linux = platform.uname()
            print(f"""{Fore.LIGHTWHITE_EX}
                     ████████               {Fore.LIGHTWHITE_EX}System      :       {linux.system}{Fore.LIGHTBLUE_EX}             
                   ████████████             {Fore.LIGHTWHITE_EX}Version     :       {linux.version}{Fore.LIGHTBLUE_EX}               
                  ███████████▓▓███          {Fore.LIGHTWHITE_EX}Machine     :       {linux.machine}{Fore.LIGHTBLUE_EX}              
                 █████████████████          {Fore.LIGHTWHITE_EX}Processor   :       {linux.processor}{Fore.LIGHTBLUE_EX}             
                ███████████████████         {Fore.LIGHTWHITE_EX}Node        :       {linux.node}{Fore.LIGHTBLUE_EX}             
                ██▓▒▒████▓░░▒▓█████         {Fore.LIGHTWHITE_EX}User        :       {gpass.getuser()}{Fore.LIGHTBLUE_EX}            
                ██▒█▓░██▓░██▓░▓████         {Fore.LIGHTWHITE_EX}Python      :       {sys.version.split()[0]}{Fore.LIGHTBLUE_EX}            
                ██▒██░▓▓▒░███ ▓████                     
                ███▒▒░░░░░░░░▒█████                     
                ██▒░░░░░░░░░▒▒██████                    
                █▓▒▒░░░▒▒▒░▒▒███▓▓██                   
                ██▒▒▓▒▒▒▒▒▒░░░░██████                   
               ███░░░▒▒▒░░░    ░███████                 
              ███░  ░░░░░       ▒███████                
              ███░             ░░░████████               
            ████▓▒░░  ░░░  ░░▒▒▒▒▒░█████████             
            ███▓░░             ░░░▒░█████████            
           ███▓░                  ░░░█████████           
          ████░                     ░█████████           
         ████░       ░               ░█████████          
         █████░       ░               ░█████████          
         ████▒       ░░               ░██████████         
         █▒▓█▓       ░░               ░█████████          
        ▒░░░░▓█░      ░            ░░░░███████▓▒          
     ▓▒░░░░░░▒██░░               ░░░░▒██████▒░░░         
    ▒░░░░░░░░░░░░░███▓░            ░░▒▒░▒▒▓▓▓▒▒░░░░         
  ▓▒░░░░░░░░░░░░░░████░            ░▒▒░░░░░░░░░░░░░░       
  ▒░░░░░░░░░░░░░░░▓█▓░           ░▒█▒░░░░░░░░░░░░░░░░     
 █▒░░░░░░░░░░░░░░░░▒░          ░▓██▓▒░░░░░░░░░░░░░░░░     
 ▒░░░░░░░░░░░░░░░░░░▒█▒░░▒▒▒▓██████▓▒░░░░░░░░░░░░▒▓       
██▒▒▒▒▒▒░░░░░░░░░░░▒▒██████████████▓▒▒░░░░░░░▒▓████       
 ██████▓▓▓▓▒▒▒▒▒▒▒▒▒▓██████████████▓▒▒▒▒▒▒▒▓██████        
   ██████████▓▓▓▓▓▓█████████████████▓▓▓▓▓▓██████          
      █████████████           █████████████                  
{Fore.RESET}""")     

    def help(self):
        """
        Display all available commands in AvalonShell with their descriptions.
        """
        cmd = self.util.endLine

        commands = [
            cmd(f"{self.fcmd}cat{Fore.RESET} {self.fargs}<fileName> [number_lines]{Fore.RESET}", "Print file content, optionally with line numbers", "|"),
            cmd(
                f"{self.fcmd}cd{Fore.RESET} {self.fargs}<Path>{Fore.RESET}","Change the current directory to the specified path, or use `.$` to go up one or more directories. `.` to set directory depth to global. `.-` to go to the only dir in the current directory","|"),
            cmd(
                f"{self.fcmd}scd{Fore.RESET} {self.fargs}<Path>{Fore.RESET}","Change the current directory of a custom slot to the specified path, or use `$` to go up one or more directories. the last same as cd","|"),
            cmd(f"{self.fcmd}chmod{Fore.RESET} {self.fargs}<fileName> <Mode>{Fore.RESET}", "Change file permissions (numeric mode like 755)", "|"),
            cmd(f"{self.fcmd}chown{Fore.RESET} {self.fargs}<fileName> <User> [Group]{Fore.RESET}", "Change file ownership", "|"),
            cmd(f"{self.fcmd}clear/cls/c{Fore.RESET}", "Clear the terminal screen", "|"),
            cmd(f"{self.fcmd}cp{Fore.RESET} {self.fargs}<SourceFile> <Destination>{Fore.RESET}", "Copy a file to a destination directory", "|"),
            cmd(f"{self.fcmd}df{Fore.RESET} {self.fargs}[Disk]{Fore.RESET}", "Display disk usage information", "|"),
            cmd(f"{self.fcmd}download{Fore.RESET} {self.fargs}<URL or Key> [Filename]{Fore.RESET}", "Download a file to the home directory", "|"),
            cmd(f"{self.fcmd}install{Fore.RESET} {self.fargs}<AvalonShell supported software>{Fore.RESET}", "A built-in command that download a software supported by Avalon Shell to the home directory", "|"),
            cmd(f"{self.fcmd}du{Fore.RESET}", "Display the size of the current directory", "|"),
            cmd(f"{self.fcmd}echo{Fore.RESET} {self.fargs}<Text or $VARIABLE>{Fore.RESET}", "Print text or variable value", "|"),
            cmd(f"{self.fcmd}exit{Fore.RESET}", "Exit AvalonShell", "|"),
            cmd(f"{self.fcmd}grep{Fore.RESET} {self.fargs}<Pattern> <fileName> [-i] [-n]{Fore.RESET}", "Search for a pattern in a file, optionally ignoring case or showing line numbers", "|"),
            cmd(f"{self.fcmd}kill{Fore.RESET} {self.fargs}<PID or ProcessName>{Fore.RESET}", "Terminate a process by PID or name", "|"),
            cmd(f"{self.fcmd}less/view{Fore.RESET} {self.fargs}<fileName>{Fore.RESET}", "View file content page by page", "|"),
            cmd(f"{self.fcmd}listdir/ls/dir{Fore.RESET} {self.fargs}<Extra Args: -f(file only), -d(dir only), -l(detailed), -r(reversed), -b(sort by bytes) -p(full path) -h(human readable size, only work with -l).(These are optional)>{Fore.RESET}", "List all items in the current directory", "|"),
            cmd(f"{self.fcmd}mkdir{Fore.RESET} {self.fargs}<*MultipleDirectoryName>{Fore.RESET}", "Create a directory in the current directory", "|"),
            cmd(f"{self.fcmd}mv/move/mov{Fore.RESET} {self.fargs}<SourceFile> <Destination>{Fore.RESET}", "Move a file to a destination", "|"),
            cmd(f"{self.fcmd}nano{Fore.RESET} {self.fargs}<fileName>{Fore.RESET}", "Edit a file using Avalon Nano editor", "|"),
            cmd(f"{self.fcmd}newvar{Fore.RESET} {self.fargs}<VarName> [Value]{Fore.RESET}", "Create a new variable with a value", "|"),
            cmd(f"{self.fcmd}oshost{Fore.RESET} {self.fargs}<HostCMD> [HostARGS]{Fore.RESET}", "Run a host system command", "|"),
            cmd(f"{self.fcmd}paste{Fore.RESET}", "Paste and display clipboard content", "|"),
            cmd(f"{self.fcmd}printvar{Fore.RESET}", "Print all shell variables", "|"),
            cmd(f"{self.fcmd}ps{Fore.RESET}", "List running processes", "|"),
            cmd(f"{self.fcmd}pwd{Fore.RESET}", "Print the current working directory and slot", "|"),
            cmd(f"{self.fcmd}pbf{Fore.RESET} {self.fargs}<file> <length> <PureBinary:True|False or 1|0>{Fore.RESET}",
                "Print a binary file in hex or pure binary, max length: 1024 letters",
                "|"
            ),
            cmd(f"{self.fcmd}rename/ren{Fore.RESET} {self.fargs}<FileName> <NewName>{Fore.RESET}", "Rename a file", "|"),
            cmd(f"{self.fcmd}rm{Fore.RESET} {self.fargs}<File or Directory>{Fore.RESET}", "Remove a file or directory", "|"),
            cmd(f"{self.fcmd}rmdir{Fore.RESET} {self.fargs}<Directory>{Fore.RESET}", "Remove an empty directory", "|"),
            cmd(f"{self.fcmd}run/r{Fore.RESET} {self.fargs}<ProgramName> [Inputs]{Fore.RESET}", "Run a program with optional inputs", "|"),
            cmd(f"{self.fcmd}runfile{Fore.RESET} {self.fargs}<File>{Fore.RESET}", "Execute commands from a script file", "|"),
            cmd(f"{self.fcmd}runsel{Fore.RESET}", "Select and run a script file via file dialog", "|"),
            cmd(f"{self.fcmd}setvar{Fore.RESET} {self.fargs}<VarName> [Value]{Fore.RESET}", "Set a variable to a value", "|"),
            cmd(f"{self.fcmd}slink{Fore.RESET} {self.fargs}<ShellName> [ShellCMD] [HostShellArgs]{Fore.RESET}", "Launch a new shell with optional commands", "|"),
            cmd(f"{self.fcmd}slot{Fore.RESET} {self.fargs}<Slot>{Fore.RESET}", "Switch to a specified slot (1-10)", "|"),
            cmd(f"{self.fcmd}cslot{Fore.RESET} {self.fargs}<Slot>{Fore.RESET}",
                "Switch to a custom slot",
                "|"
            ),
            cmd(f"{self.fcmd}shows{Fore.RESET}",
                "Show the current standard and custom slot",
                "|"
            ),
            cmd(f"{self.fcmd}newslot{Fore.RESET} {self.fargs}<Slot>{Fore.RESET}",
                "Create a custom slot",
                "|"
            ),
            cmd(f"{self.fcmd}printslot{Fore.RESET}",
                "Show all custom slots",
                "|"
            ),
            cmd(f"{self.fcmd}admin{Fore.RESET}",
                "Run AvalonShell with admin privileges",
                "|"
            ),
            cmd(f"{self.fcmd}w{Fore.RESET} {self.fargs}<FileName> <*Contents>{Fore.RESET} ",
                "Write to a file",
                "|"
            ),
            cmd(f"{self.fcmd}title/name{Fore.RESET} {self.fargs}<Name>{Fore.RESET}", "Set the terminal title", "|"),
            cmd(f"{self.fcmd}top{Fore.RESET} {self.fargs}[Refresh] [Limit]{Fore.RESET}", "Display top processes by CPU usage", "|"),
            cmd(f"{self.fcmd}touch/tou/touhou{Fore.RESET} {self.fargs}<FileName>{Fore.RESET}", "Create an empty file (touhou shows a fun fact)", "|"),
            cmd(f"{self.fcmd}loop{Fore.RESET} {self.fargs}<times> <cmd> <args>{Fore.RESET}", "Loop a command with specified times", "|"),
            cmd(f"{self.fcmd}specs/spec{Fore.RESET}", "Show your host system and machine specs", "|"),
            
            
            cmd(f"{self.fcmd}asp{Fore.RESET} {self.fargs}<FileName(Optional: if you don't specify a file then it will open python repl in a new window)>{Fore.RESET}",
                "AvalonShell's Python Interpreter",
                "|"
            ),

            cmd(f"{self.fcmd}zip{Fore.RESET} {self.fargs}<ArchiveName> <*Multiplefiles>{Fore.RESET}",
                "AvalonShell's Built-in zip function",
                "|"
            ),

            cmd(f"{self.fcmd}unzip{Fore.RESET} {self.fargs}<ArchiveName> <outputDir(Automatically created a new one when no dir were specified)> <specificFiles>{Fore.RESET}",
                "AvalonShell's Built-in unzip function",
                "|"
            ),


            "Extra CMDs:",
            cmd(f"{self.fcmd}/(at the end){Fore.RESET}",
                "Go to the next line and keeping the old line not executed",
                "|"
            ),
            cmd(f"{self.fcmd}#(at the start){Fore.RESET}",
                "print a comment",
                "|"
            ),

            "Symbols:",

            cmd(f"{self.fcmd}||{Fore.RESET}",
                "run the cmd on the right if the cmd on the left failed",
                "|"
            ),
            cmd(f"{self.fcmd}&&{Fore.RESET}",
                "execute another cmd on the right",
                "|"
            ),
            cmd(f"{self.fcmd}&{Fore.RESET}",
                "multi-tasking on the bg",
                "|"
            ),
            cmd(f"{self.fcmd};{Fore.RESET}",
                "always executed",
                "|"
            ),
            cmd(f"{self.fcmd}>{Fore.RESET}",
                "overwrite the output of a cmd to a file",
                "|"
            ),
            cmd(f"{self.fcmd}>>{Fore.RESET}",
                "append the output of a cmd to a file",
                "|"
            ),

            "Random things:",
            cmd(f"{self.fcmd}help{Fore.RESET}",
                "self explainetory",
                "|"
            ),
        ]

        # Box style header
        self.util.boxPrint("Avalon Shell - Help Menu", width=60)

        # Print all commands
        print("\n".join(commands))

    def parse(self, user_input: str):
        splitedLines = user_input.splitlines()
        for each in splitedLines:
            parts = each.split()
            if not parts:  # Skip empty lines
                continue
                
            cmd = parts[0].lower()
            args = parts[1:]

            # Replace variables in args that start with $
            def replace_var(arg):
                if arg.startswith('$'):
                    match = re.match(r'\$([A-Za-z_][A-Za-z0-9_]*)', arg)
                    if match:
                        var = match.group(1)
                        return self.variables.get(var, "")
                return arg

            # Apply variable substitution to each argument
            args = [replace_var(arg) for arg in args]

            try:


                if cmd == "help":
                    self.help()
                    return True


                elif cmd == "edit":
                    if len(args) == 1:
                        filename = args[0]
                        self.edit(filename)
                    else:
                        self.edit("Untitled")
                    return True


                elif cmd == "shows":
                    self.showsc()
                    return True


                elif cmd == "pbf":
                    if len(args) == 0:
                        print("Usage: pbf <FileName> <length> <pureBinary: true|false or 1|0(optional)>")
                        return False
                    else:
                        file = args[0]
                        length = 512
                        pure = False

                        if len(args) >= 2:
                            length = int(args[1])
                        if len(args) >= 3 and args[2] in (1,0, "true", "false"):
                            if args[2] in (1, "true", "True"):
                                pure = True
                            else:
                                pure = False
                        
                        self.pbf(file, length, pure)
                        return True


                elif cmd == "zip":
                    if len(args) > 1:
                        zipName = args[0]
                        files = args[1:]
                        self.zip(zipName, *files)
                        return True
                    else:
                        print("Usage: zip <zipName> <multipleFiles>")
                        return False

                
                elif cmd == "unzip":
                    if len(args) >= 1:
                        archiveName = args[0]
                        outputDir = None
                        targetFiles = None

                        if len(args) >= 2:
                            outputDir = args[1]
                        if len(args) > 2:
                            targetFiles = args[2:]

                        self.unzip(archiveName, outputDir, targetFiles)
                        return True
                    else:
                        print("Usage: unzip <archiveName> [outputDir] [files...]")
                        return False



                elif cmd == "asp":
                    if len(args) == 1:
                        file = args[0]
                        self.python313(file)
                    else:
                        self.python313()
                    return True


                elif cmd == "admin":
                    self.AdminShell()
                    return True

                elif cmd in ("specs", "spec"):
                    self.specs()
                    return True


                elif cmd == "w":
                    if len(args) < 2:
                        print("Usage: w <fileName> <Contents>")
                        return False
                    else:
                        file = args[0]
                        content = args[1:]
                        self.writeto(file, content)
                        return True


                elif cmd == "ps":
                    self.ps()
                    return True


                elif cmd == "kill":
                    if not args:
                        print(f"{self.ferr}Usage: kill <PID|ProcessName>{Fore.RESET}")
                        return False
                    else:
                        self.kill(args[0])
                        return True


                elif cmd == "loop":
                    if len(args) < 2:
                        print(f"{self.ferr}Usage: loop <times> <cmd> [args...]{Fore.RESET}")
                        return False
                    else:
                        try:
                            times = int(args[0])
                            if times < 0:
                                print(f"{self.ferr}Error: Loop count must be non-negative{Fore.RESET}")
                                continue
                        except ValueError:
                            print(f"{self.ferr}Times must be an integer{Fore.RESET}")
                            continue
                        cmde = args[1]
                        loop_args = args[2:]
                        self.loop(times, cmde, *loop_args)
                        return True


                elif cmd == "top":
                    refresh = 2.0
                    limit = 10
                    if args:
                        try:
                            refresh = float(args[0])
                        except ValueError:
                            print(f"{self.ferr}Invalid refresh value: {args[0]}{Fore.RESET}")
                            continue
                    if len(args) > 1:
                        try:
                            limit = int(args[1])
                        except ValueError:
                            print(f"{self.ferr}Invalid limit value: {args[1]}{Fore.RESET}")
                            continue
                    self.top(refresh, limit)
                    return True


                elif cmd in ("title", "name"):
                    if not args:
                        print(f"{self.ferr}Usage: title <Name>{Fore.RESET}")
                        return False
                    else:
                        self.title(args[0])
                        return True


                elif cmd == "df":
                    if args:
                        self.df(args[0])
                        return True
                    else:
                        self.df()
                        return True


                elif cmd == "chmod":
                    if len(args) < 2:
                        print(f"{self.ferr}Usage: chmod <fileName> <mode>{Fore.RESET}")
                        return False
                    else:
                        self.chmod(args[0], args[1])
                        return True


                elif cmd in ("less", "view"):
                    if not args:
                        print(f"{self.ferr}Usage: less <fileName>{Fore.RESET}")
                        return False
                    else:
                        self.less(args[0])
                        return True


                elif cmd == "grep":
                    if len(args) < 2:
                        print(f"{self.ferr}Usage: grep <pattern> <fileName> [-i] [-n]{Fore.RESET}")
                        return False
                    else:
                        pattern = args[0]
                        fileName = args[1]
                        ignore_case = "-i" in args
                        show_line_number = "-n" in args
                        self.grep(pattern, fileName, ignore_case, show_line_number)
                        return True


                elif cmd in ("clear", "cls", "c"):
                    self.clear()
                    return True


                elif cmd == "chown":
                    if len(args) < 2:
                        print(f"{self.ferr}Usage: chown <fileName> <user> [group]{Fore.RESET}")
                        return False
                    else:
                        fileName = args[0]
                        user = args[1]
                        group = args[2] if len(args) > 2 else None
                        self.chown(fileName, user, group)
                        return True


                elif cmd in ("cat", "catalog"):
                    if not args:
                        print(f"{self.ferr}Usage: cat/catalog <fileName> [number_lines]{Fore.RESET}")
                        return False
                    else:
                        numberinglines = len(args) > 1 and args[1].lower() in ("1", "true", "yes", "y")
                        self.cat(args[0], numberinglines)
                        return True


                elif cmd == "cd":
                    if args:
                        if args[0] == "winRECYCLE":
                            recycle = self.variables.get("RECYCLE.BIN")
                            if recycle:
                                self.CD(recycle)
                                return True
                            else:
                                print(f"{self.ferr}Recycle Bin path not found{Fore.RESET}")
                                return False
                        else:
                            self.CD(" ".join(args))
                            return True
                    else:
                        print(f"{self.ferr}cd requires a path argument{Fore.RESET}")
                        return False


                elif cmd == "scd":
                    if args:
                        self.scd(" ".join(args))
                        return True
                    else:
                        print(f"{self.ferr}scd requires a path argument{Fore.RESET}")
                        return False


                elif cmd == "newslot":
                    if args:
                        self.newslot(" ".join(args))
                        return False
                    else:
                        print(f"{self.ferr}newslot requires a slot name argument{Fore.RESET}")
                        return False


                elif cmd == "cslot":
                    if len(args) == 0:
                        print(f"Usage: cslot <slotName>")
                        return False
                    else:
                        slotName = args[0]
                        self.cslot(slotName)
                        return True


                elif cmd == "printslot":
                    self.printslot()
                    return True


                elif cmd == "slot":
                    if args:
                        try:
                            slot = int(args[0])
                            self.slot(slot)
                            return True
                        except ValueError:
                            print(f"{self.ferr}slot requires a numeric argument{Fore.RESET}")
                            return False
                    else:
                        print(f"{self.ferr}slot requires a slot argument{Fore.RESET}")
                        return False


                elif cmd == "mkdir":
                    yesParent = False
                    lifting = 0
                    for arg in args:
                        if arg in ("-p", "-P"):
                            yesParent = True
                            lifting += 1

                    if len(args) > 0:
                        dirs = args[lifting:]
                        self.mkdir(yesParent, *dirs)
                        return False
                    else:
                        print("Usage: mkdir <ExtraArgs: -p/-P(optional)> <MultipleDirs>")
                        return False


                elif cmd == "rm":
                    if len(args) > 0:
                        files = args[0:]
                        self.rm(*files)
                        return True
                    else:
                        print("Usage: rm <*MultipleDirOrFiles>")
                        return False


                elif cmd == "echo":
                    self.echo(args)
                    return True


                elif cmd == "cp":
                    if len(args) < 2:
                        print(f"{self.ferr}Usage: cp <srcFile> <Directory>{Fore.RESET}")
                        return False
                    else:
                        src = args[0]            # first argument is source
                        dest = " ".join(args[1:]) # rest of arguments combined as destination
                        self.cp(src, dest)
                        return True


                elif cmd == "pwd":
                    self.pwd()
                    return True

                elif cmd in ("touch", "tou", "touhou"):
                    if not args:
                        print(f"{self.ferr}Usage: touch <MultipleFile>{Fore.RESET}")
                        return False
                    else:
                        files = args[0:]
                        if cmd == "touhou":
                            import random as r
                            print(r.choice(self.touHouFacts))
                        self.touch(*files)


                elif cmd in ("mv", "mov", "move"):
                    if len(args) <= 1:
                        print(f"{self.ferr}Usage: mv/mov/move SrcFile Destination{Fore.RESET}")
                        return False
                    else:
                        self.mv(args[0], args[1])
                        return True


                elif cmd == "setvar":
                    if not args:
                        print(f"{self.ferr}Usage: setvar <var name> [value]{Fore.RESET}")
                        return False
                    else:
                        varName = args[0]
                        values = " ".join(args[1:])
                        self.setVar(varName, values)
                        print(f"Var: {varName} has been set to: {values} successfully!")
                        return True


                elif cmd == "newvar":
                    if not args:
                        print(f"{self.ferr}Usage: newvar <var name> [value]{Fore.RESET}")
                        return False
                    else:
                        varn = args[0]
                        value = " ".join(args[1:])
                        self.newVar(varn, value)
                        print(f"Variable: {varn}. Value: {value} has been added to self.variables!")
                        return True


                elif cmd == "printvar":
                    self.printVar()
                    return True


                elif cmd == "oshost":
                    if not args:
                        print(f"{self.ferr}Usage: oshost <hostCMD> [hostARGS]{Fore.RESET}")
                        return False
                    else:
                        if len(args) >= 1:
                            self.OSHost(args[0], *args[1:])
                        else:
                            self.OSHost(args[0], [""])
                        return True


                elif cmd == "download":
                    if not args:
                        print(f"{self.ferr}Usage: download <url or key> [filename]{Fore.RESET}")
                        return False
                    else:
                        tfile = args[0]
                        url = self.webs.get(tfile, tfile)
                        target = args[1] if len(args) > 1 else os.path.basename(url) or "downloaded_file"
                        
                        # Expand variables in both url and target
                        for var, val in self.variables.items():
                            url = url.replace(f"${var}", str(val))
                            target = target.replace(f"${var}", str(val))
                            
                        save_path = os.path.join(self.home, target)
                        try:
                            os.makedirs(self.home, exist_ok=True)
                            self.download_to_home(url, save_path)
                            return True
                        except requests.exceptions.RequestException as e:
                            print(f"{self.ferr}Download failed: {e}{Fore.RESET}")
                            return False
                        except Exception as e:
                            print(f"{self.ferr}Error saving file: {e}{Fore.RESET}")
                            return False


                elif cmd == "install":
                    if not args:
                        print(f"{self.ferr}Usage: install <AvalonShell Supported software>{Fore.RESET}")
                    else:
                        software = " ".join(args)
                        try:
                            self.install(software)
                            return True
                        except Exception as e:
                            print(f"{self.ferr}Error while installing software: {e}{Fore.RESET}")
                            return False


                elif cmd == "nano":
                    if not args:
                        print(f"{self.ferr}Usage: nano <FileName>{Fore.RESET}")
                        return False
                    else:
                        self.nano(args[0])
                        return True


                elif cmd in ("run", "r"):
                    if not args:
                        print(f"{self.ferr}Usage: run <program_name> [inputs]{Fore.RESET}")
                        return False
                    else:
                        program_input = " ".join(args[1:])
                        self.Program(args[0], program_input)
                        return True


                elif cmd == "runsel":
                    target=self.runsel
                    return True


                elif cmd in ("ls", "listdir", "dir"):
                    reverse = False
                    detailed = False
                    sort_size = False
                    only_cfiles = False
                    only_cdirs  = False
                    fullpath = False
                    human = False

                    for arg in args:
                        if arg == "-r":
                            reverse = True
                        elif arg == "-l":
                            detailed = True
                        elif arg == "-s":
                            sort_size = True
                        elif arg == "-f":
                            only_cfiles = True
                            only_cdirs = False
                        elif arg == "-d":
                            only_cdirs =True
                            only_cfiles = False
                        elif arg == "-p":
                            fullpath = True
                        elif arg == "-h":
                            human = True

                    # If detailed mode is requested
                    if detailed:
                        self.listdirdetailed(reverse=reverse, sort_size=sort_size, only_files=only_cfiles, only_dirs=only_cdirs, abspath=fullpath, humanReadableSize=human)
                        return True
                    else:
                        self.listdir(reverse=reverse, sort_size=sort_size, only_files=only_cfiles, only_dirs=only_cdirs, abspath=fullpath)
                        return True


                elif cmd in ("rename", "ren"):
                    if len(args) < 2:
                        print(f"{self.ferr}Usage: rename <target> <newName>{Fore.RESET}")
                        return False
                    else:
                        self.rename(args[0], " ".join(args[1:]))
                        return True


                elif cmd == "slink":
                    if not args:
                        print(f"{self.ferr}Usage: {Style.BRIGHT}slink{Style.RESET_ALL} <ShellName|ShellFilePath> ...{Fore.RESET}")
                        return False
                    else:
                        otherShell = args[0]
                        shellCMD = " ".join(args[1:])
                        HOSTSHELLcmd = " ".join(args[2:])
                        self.Slink(otherShell, shellCMD, HOSTSHELLcmd)
                        return True
                elif cmd == "exit":
                    print("exiting Avalon Shell...")
                    sys.exit(0)
                    return True              
                elif cmd.startswith("#"):
                    print(f"{self.fsuccess}# {' '.join(args)}{Fore.RESET}")
                    return True
                else:
                    print(f"{self.ferr}Unknown command: {cmd}{Fore.RESET}")
                    return False
            except Exception as e:
                print(f"{self.ferr}Error executing command {cmd}: {e}{Fore.RESET}")
                return False


    def runfile(self, file: str):
        filepath = os.path.join(self.crr_dir, file)

        if not os.path.exists(filepath):
            print(self.ferr + f"File doesn't exist: {file}")
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):  # ignore empty lines and comments
                        continue
                    self.parse(line)
        except Exception as e:
            print(self.ferr + f"Error reading file {file}: {e}")


    def handle_redirect(self, operator):
        parts = self.totalCMDs.split()
        idx = parts.index(operator)
        file = parts[idx + 1]
        mode = "a" if operator == ">>" else "w"
        self.redirector(mode=mode, redirect_file=file)

        remaining = parts[:idx] + parts[idx+2:]
        remaining_cmd = " ".join(remaining)
        self.parse(remaining_cmd)
        self.totalCMDs = ""


    def run(self):
        os.system("cls" if os.name == "nt" else "clear")
        print(Fore.LIGHTYELLOW_EX + f"{self.ferr}Avalon{Fore.RESET}{Fore.LIGHTWHITE_EX}Shell{Fore.RESET} {Fore.LIGHTYELLOW_EX}{self.version}{Fore.RESET}[©2025 RandomX]")
        print(f"""{self.ferr}
                   ##                       {Fore.LIGHTWHITE_EX}Shell       :   {Fore.LIGHTYELLOW_EX}   AvalonShell v{self.version}{self.ferr}
      **           ##                 ###   {Fore.LIGHTWHITE_EX}Shell Slots :   {Fore.LIGHTYELLOW_EX}   10{self.ferr}
     *++*          ##                ####   {Fore.LIGHTWHITE_EX}Shell Path  :   {Fore.LIGHTYELLOW_EX}   {os.path.abspath(__file__)}{self.ferr}
  **+=--=+**      ###             ######    {Fore.LIGHTWHITE_EX}OS Host     :   {Fore.LIGHTYELLOW_EX}   {platform.system()}{self.ferr}
 *++-:..:-=+*     # ##           ####       {Fore.LIGHTWHITE_EX}Host User   :   {Fore.LIGHTYELLOW_EX}   {gpass.getuser()}{self.ferr}
  **+=--=+**      # ##          ####        {Fore.LIGHTWHITE_EX}Author      :   {self.ferr}   Random{Fore.LIGHTWHITE_EX}X{self.ferr}
     *++*         # ###        ####      
      **        ### ###     #######      
                ### ###  ######          
                ### ##########     *     
               ##########        *++*    
             ############       *+=-+**  
         ##########   ####   **+-::.:-=+*
     ############      ###     *+=-:-++* 
########## #####       ####     *++=+**  
          ####          ####      **     
      #######            #####           
      #####                ####          
    #####                   ####         
 #######                     ###         
#####                          #####     
###                             ####{Fore.RESET}\n""")
        try:
            while True:
                try:
                    userInput = input(f"{Fore.LIGHTMAGENTA_EX}{self.crr_dir}> {Fore.RESET}")
                    parts = userInput.split()
                    cmd = parts[0].lower()
                    args = parts[1:]
                    self.totalCMDs += "".join(cmd) + " " + " ".join(args)
                    if self.totalCMDs.endswith("\\"):
                        while self.totalCMDs.endswith("\\"):
                            self.totalCMDs = self.totalCMDs[:-1]  # remove the backslash
                            input2 = input("> ")
                            splat2 = input2.split()
                            if not splat2:
                                continue
                            cmd2 = splat2[0]
                            args2 = " ".join(splat2[1:])
                            self.totalCMDs += "\n" + cmd2 + (" " + args2 if args2 else "")
                        self.parse(self.totalCMDs)
                        self.totalCMDs = ""




                    if ">>" in self.totalCMDs:
                        self.handle_redirect(">>")
                    elif ">" in self.totalCMDs:
                        self.handle_redirect(">")
                    elif "||" in self.totalCMDs or "&&" in self.totalCMDs or ";" in self.totalCMDs or "&" in self.totalCMDs:
                        self.symbolical_Executor()
                        self.totalCMDs = ""


                    else:
                        if cmd == "paste":
                            self.parse(self.paste())
                            self.totalCMDs = ""
                        elif cmd == "runfile":
                            file = args[0]
                            self.runfile(file)
                            self.totalCMDs = ""
                        else:
                            self.parse(self.totalCMDs)
                            self.totalCMDs = ""

                except KeyboardInterrupt:
                    print(f"{self.ferr}KeyBoardInterrupt{Fore.RESET}")
                    continue
                except Exception as e:
                    print(self.ferr + f"Error: {e}")
        except EOFError:
            print("Exiting Avalon Shell...")
            sys.exit(0)

AS = Shell()
AS.run()