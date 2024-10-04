# MultiBlox (C) 2024 draxfm
# This code was written by draxfm

# This code/software is subject to the GNU General Public License v3.0 (GNU GPLv3) License.
# Changing this code and/or distributing modified versions of this code/software is not permitted!
# For further details on the licensing and usage of subcomponents, please refer to the "LICENSE" file contained in this Repository.


import tkinter
import time
import ctypes
import sys
import os
import subprocess
import tkinter.messagebox
import threading
import requests
import json

from tkinter import *
from tkinter import ttk
from pystray import MenuItem as item, Icon
from PIL import Image

version = "v1.0.4"
status = 0

terminate_thread = False
thread = None
CONFIG_FILE = "./assets/config.json"

def check_integrity():
        required_files = {"./assets/icon.ico"}

        for file in required_files:
            if not os.path.isfile(file):
                tkinter.messagebox.showerror(title="MultiBlox Internal Error", message=f"{file} could not be found! If this issue persists contact the developer.")
                sys.exit()

def get_latest_release():
    try:
        url = f"https://api.github.com/repos/DraxFM/MultiBlox/releases/latest"
        response = requests.get(url)
        response.raise_for_status()
        latest_release = response.json()
        latest_ver = latest_release["tag_name"]
        if version != latest_ver:
            tkinter.messagebox.showinfo(title="Outdated MultiBlox Version", message="You are using an outdated version of MultiBlox! Press OK to open the latest release on GitHub.")
            runShell("start https://github.com/DraxFM/MultiBlox/releases/latest")
            sys.exit()
    except requests.exceptions.RequestException as e:
        print(f"Error checking for latest version: {e}")
        tkinter.messagebox.showerror(title="MultiBlox Internal Error", message=f"Please contact the developer! Exception: {e}")
        sys.exit()

def contact_http(page):
    if page == "ghProfile":
        runShell("start https://www.github.com/DraxFM")
    elif page == "ghRepo":
        runShell("start https://github.com/DraxFM/MultiBlox")
    elif page == "dcInvite":
        runShell("start https://discord.gg/sEXECdC3Et")
    elif page == "dcProfile":
        runShell("start https://discord.com/users/654343206275907585")

def runShell(cmd):
    subprocess.call(cmd, shell=True)

def check_duplicateProc():
    duplicate = False
    count = 0
    result = subprocess.run("tasklist | findstr MultiBlox.exe", capture_output=True, text=True, shell=True)
    if result.returncode == 0:
        lines = result.stdout.strip().split("\n")
        if lines:
            for line in lines:
                if "MultiBlox.exe" in line:
                    count += 1
    if count >= 3:
        explorerPIDs = []
        shellCMD = """wmic process where name="MultiBlox.exe" get ProcessId,ParentProcessId,Name"""
        shellCMD2 = """wmic process where name="explorer.exe" get ProcessId,ParentProcessId,Name"""

        result2 = subprocess.run(shellCMD2, capture_output=True, text=True, shell=True)
        result1 = subprocess.run(shellCMD, capture_output=True, text=True, shell=True)

        explorerProcs = result2.stdout.strip().splitlines()
        for process in explorerProcs[1:]:
            parts = process.split()
            if len(parts) == 3:
                pid = parts[2]
                explorerPIDs.append(pid)

        MBProcs = result1.stdout.strip().splitlines()

        global mainProc
        mainProc = None

        for process in MBProcs[1:]:
            parts = process.split()
            if len(parts) == 3:
                pid = parts[2]
                ppid = parts[1]
                print(ppid)
                if ppid in explorerPIDs:
                    mainProc = pid
                    break

        if mainProc == None:
            tkinter.messagebox.showwarning(title="MultiBlox Internal Error", message="An unknown internal error occured. If this keeps happening please contact the developer!")
            duplicate = False
            return duplicate

        for procs in MBProcs[1:]:
            parts = process.split()
            if len(parts) == 3:
                ppid = parts[1]
                if ppid == mainProc or ppid in explorerProcs:
                    duplicate = False
                else:
                    duplicate = True
    return duplicate

def hide_window():
    root.withdraw()

    menu = (item('Show', show_window), item('Exit', quit_window))
    icon = Icon("multiblox", Image.open("./assets/icon.ico"), title="MultiBlox by draxfm", menu=menu)
    
    threading.Thread(target=icon.run, daemon=True).start()

def show_window(icon):
    icon.stop()
    root.after(0, root.deiconify)

def quit_window(icon):
    icon.stop()
    root.quit()
    os._exit(0)

def win_handler():
    if min_to_systray.get() == True:
        hide_window()
    else:
        os._exit(0)

def save_settings(conf):
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(conf, config_file)

def load_settings():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            return json.load(config_file)
    return {}

def on_checkbox_toggle(obj, objVar):
    conf[obj] = objVar.get()
    save_settings(conf)

def getRobloxInstance():
    robloxFound = False
    try:
        result = subprocess.run(["tasklist"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            if lines:
                for line in lines:
                    if "RobloxPlayerBeta.exe" in line:
                        robloxFound = True
        return robloxFound
    except Exception as e:
        print(f"Error occured: {e}")
        tkinter.messagebox.showerror(title="MultiBlox Internal Error", message=f"Please contact the developer! Exception: {e}")
        sys.exit()
        
def forceKillRoblox():
    try:
        runShell("taskkill /F /IM RobloxPlayerBeta.exe")
    except Exception as e:
        print(f"Error occured: {e}")
        tkinter.messagebox.showerror(title="MultiBlox Internal Error", message=f"Please contact the developer! Exception: {e}")
        sys.exit()
        
def findBootstrapper(mode):
    if mode == "roblox":
        try:
            base_dir = os.path.join(os.getenv('LOCALAPPDATA'), "Roblox", "Versions")
            roblox_executable = "RobloxPlayerBeta.exe"
            
            for root, dirs, files in os.walk(base_dir):
                if roblox_executable in files:
                    return os.path.join(root, roblox_executable)
            
            return None
        except Exception as e:
            print("Error occured: {e}")
            tkinter.messagebox.showerror(title="MultiBlox Internal Error", message=f"Please contact the developer! Exception: {e}")
            sys.exit()
    elif mode == "bloxstrap":
        try:
            base_dir = os.path.join(os.getenv('LOCALAPPDATA'), "Bloxstrap")
            roblox_executable = "Bloxstrap.exe"
            
            for root, dirs, files in os.walk(base_dir):
                if roblox_executable in files:
                    return os.path.join(root, roblox_executable)
            
            return None
        except Exception as e:
            print("Error occured: {e}")
            tkinter.messagebox.showerror(title="MultiBlox Internal Error", message=f"Please contact the developer! Exception: {e}")
            sys.exit()

def startRobloxInstance():
    try:
        if use_bloxstrap_var.get() == 1:
            bootstrapper = findBootstrapper("bloxstrap")
        elif use_bloxstrap_var.get() == 0:
            bootstrapper = findBootstrapper("roblox")
            
        runShell(f"start {bootstrapper}")
        print("starting roblox instance")
        
    except Exception as e:
        print(f"Error occured: {e}")
        tkinter.messagebox.showerror(title="MultiBlox Internal Error", message=f"Please contact the developer! Exception: {e}")
        sys.exit()

def mutex_thread():
    handle = ctypes.windll.kernel32.CreateMutexW(None, True, "ROBLOX_singletonMutex")

    global terminate_thread
    while not terminate_thread:
        time.sleep(0.1)
        pass

    ctypes.windll.kernel32.ReleaseMutex(handle)
    ctypes.windll.kernel32.CloseHandle(handle)
    if ctypes.windll.kernel32.GetLastError() == 0:
        print("mutex released and handle closed")
    else:
        print(f"error: {ctypes.windll.kernel32.GetLastError()}")
    terminate_thread = False
    global thread
    thread = None

def main_func():
    if use_bloxstrap_var.get() == 1:
        bootstrapper = findBootstrapper("bloxstrap")
        mode = "bloxstrap"
    elif use_bloxstrap_var.get() == 0:
        bootstrapper = findBootstrapper("roblox")
        mode = "roblox"
    if bootstrapper:
        print(f"bootstrapper found: {bootstrapper}")
    else:
        tkinter.messagebox.showerror(title="MultiBlox Error", message=f"MultiBlox was not able to find an existing Roblox Client. If the issue persists please contact the developer. (METHOD: {mode})")
        sys.exit()
    global status
    print(status)
    if status == 1:
        global terminate_thread
        terminate_thread = True
        if getRobloxInstance() == True:
            forceKillRoblox()
        #mutex = ctypes.windll.kernel32.OpenMutexW(0x1F0001, True, "ROBLOX_singletonMutex")
        #ctypes.windll.kernel32.ReleaseMutex(mutex)
        #ctypes.windll.kernel32.CloseHandle(mutex)
        #if ctypes.windll.kernel32.GetLastError() == 0:
        #    print("mutex acquired")
        #else:
        #    print(f"error: {ctypes.windll.kernel32.GetLastError()}")
        status = 0
        main_l1_var.set("Status: Offline")
    elif status == 0:
        global thread
        if thread == None:
            thread = threading.Thread(target=mutex_thread)
            thread.start()
        status = 1
        main_l1_var.set("Status: Online")

check_integrity()
get_latest_release()

if check_duplicateProc() == True:
    tkinter.messagebox.showwarning(title="MultiBlox Duplicate Error", message="Another instance of MultiBlox is already running, check your system tray if you can't find it. If this issue persists please contact the developer!")
    sys.exit()    

root = Tk()
root.title("MultiBlox " + version + " by draxfm")
root.geometry("355x280")
root.iconbitmap("./assets/icon.ico")
root.protocol("WM_DELETE_WINDOW", win_handler)
root.resizable(False, False)

conf = load_settings()

root.attributes("-topmost", True)
root.attributes("-topmost", False)

tabControl = ttk.Notebook(root)

main = ttk.Frame(tabControl)
settings = ttk.Frame(tabControl)
contact = ttk.Frame(tabControl)
tabControl.add(main, text="Main")
tabControl.add(settings, text="Settings")
tabControl.add(contact, text="Contact")
tabControl.pack(expand=1, fill="both")

# -- DYNAMIC VARIABLES --
main_l1_var = StringVar()
use_bloxstrap_var = BooleanVar(value=conf.get("settings_cb1", False))
min_to_systray = BooleanVar(value=conf.get("settings_cb2", True))

# -- MAIN TAB WIDGETS --
title_label = ttk.Label(main, text="MultiBlox Control Panel", font=("Arial", 20))
title_label.grid(row=0, column=0, columnspan=2, pady=(30, 15))

title_label2 = ttk.Label(main, text="made by draxfm | github.com/DraxFM", font=("Arial", 10))
title_label2.grid(row=1, column=0, columnspan=2, pady=(30, 15))

main_l1 = ttk.Label(main, textvariable=main_l1_var, font=("Arial", 14))
main_l1.grid(row=2, column=0, columnspan=2, pady=20)

main_b1 = ttk.Button(main, takefocus=False, text="Toggle MultiBlox", command=main_func, width=20)
main_b1.grid(row=3, column=0, columnspan=2, pady=30, ipady=5)

main_b2 = ttk.Button(main, takefocus=False, text="Start Roblox Instance", command=startRobloxInstance, width=20)
main_b2.grid(row=4, column=0, columnspan=2, pady=30, ipady=5)

main_b2 = ttk.Button(main, takefocus=False, text="Kill Roblox Instances", command=forceKillRoblox, width=20)
main_b2.grid(row=5, column=0, columnspan=2, pady=30, ipady=5)

# -- SETTINGS TAB WIDGETS --
settings_cb1 = ttk.Checkbutton(settings, takefocus=False, text="Use Bloxstrap", variable=use_bloxstrap_var, style="TCheckbutton", command=lambda:on_checkbox_toggle("settings_cb1", use_bloxstrap_var))
settings_cb1.grid(row=0, column=0, padx=10, pady=3, sticky='w')

settings_cb2 = ttk.Checkbutton(settings, takefocus=False, text="Minimize MultiBlox to system tray", variable=min_to_systray, style="TCheckbutton", command=lambda:on_checkbox_toggle("settings_cb2", min_to_systray))
settings_cb2.grid(row=1, column=0, padx=10, pady=3, sticky="w")

# -- CONTACT TAB WIDGETS --
contact_l = ttk.Label(contact, text="Please contact me when experiencing persistent\nor fatal errors.\nYou can also reach out to me for feedback!", font=("Arial", 12))
contact_l.grid(row=0, column=0, padx=3, pady=3)

contact_empty1 = ttk.Label(contact, text="\n")
contact_empty1.grid(row=1, column=0, padx=3, pady=3)

contact_b1 = ttk.Button(contact, takefocus=False, text="Open Github Profile", command=lambda:contact_http("ghProfile"), width=20)
contact_b1.grid(row=2, column=0, padx=30, pady=3, sticky="w", ipady=10)

contact_b2 = ttk.Button(contact, takefocus=False, text="Open Github Repo", command=lambda:contact_http("ghRepo"), width=20)
contact_b2.grid(row=2, column=0, padx=30, pady=3, sticky="e", ipady=10)

contact_b3 = ttk.Button(contact, takefocus=False, text="Open Discord Profile", command=lambda:contact_http("dcProfile"), width=20)
contact_b3.grid(row=3, column=0, padx=30, pady=3, sticky="w", ipady=10)

contact_b4 = ttk.Button(contact, takefocus=False, text="Get Discord Invite", command=lambda:contact_http("dcInvite"), width=20)
contact_b4.grid(row=3, column=0, padx=30, pady=3, sticky="e", ipady=10)


# -- WIDGET ADJUSTMENTS --
main_l1_var.set("Status: Offline")

for widget in main.winfo_children():
    widget.grid_configure(padx=30, pady=5)

root.mainloop()
