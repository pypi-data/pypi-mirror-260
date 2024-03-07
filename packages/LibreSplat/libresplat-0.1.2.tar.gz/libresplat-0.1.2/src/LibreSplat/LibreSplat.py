# LibreSplat
# Created by Sigge [REDACTED]
import tkinter as tk
from tkinter import ttk
import os
import random
import tracemalloc
import sys
import pickle
import io
import requests
import traceback
import subprocess
from base64 import b64encode
witty_comments = [
    "Looks like our code decided to take an unscheduled coffee break!",
    "Well, that wasn't in the script!",
    "Whoops! Looks like someone forgot to feed the code gremlins.",
    "Looks like our software just took a detour through the crash course.",
    "Houston, we have a problem... and it's not rocket science, it's code!",
    "Looks like the software decided to go on a spontaneous vacation. Next stop: Debug Island!",
    "Error 404: Logic not found. Please consult the nearest software wizard.",
    "Looks like our code took a wrong turn at 'if' and ended up in 'else'where!",
    "Well, that's one way to make an unexpected exit.",
    "Looks like the software decided to play hide and seek. Spoiler alert: it's hiding in the crash report!"
]
def run(function, reportserver, root=None,*args):
    snapshot = None
    traceback_str = None
    try:
        tracemalloc.start(200)
        function(*args)
        tracemalloc.stop()
    except Exception as e:
        snapshot = tracemalloc.take_snapshot()
        traceback_list = traceback.format_exception(type(e), e, e.__traceback__)
    
        # Convert the list to a single string
        traceback_str = ''.join(traceback_list)
    
    else:
        return
    rootwin = None
    if root is None:
        rootwin = tk.Tk()
    else:
        rootwin = tk.Toplevel(root)
    fileloc = os.environ["TEMP"] + "\\LibreSplat-CrashReport." + str(random.randint(1,9999)) + ".txt"
    with open(fileloc,"w") as f:
        f.write("=============LibreSplat crash report=============\n\n")
        f.write("// " + random.choice(witty_comments) + "\n\n\n")
        f.write("Python version is " + sys.version + "\n")
        f.write(traceback_str)
    rootwin.title("LibreSplat error reporter")
    label = tk.Label(rootwin, text="The program has crashed.\nWould you like to report or view the report?", relief="sunken", padx=5, pady=5, wraplength=200, justify="left", anchor="nw")
    label.config(font=("Arial", 12), bg="white", bd=1, highlightthickness=1, highlightbackground="black")
    def owde(file_path): # OWDE stands for Open With Default Editor
        try:
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', file_path))
            elif os.name == 'nt':
                os.startfile(file_path)
            elif os.name == 'posix':
                subprocess.call(('xdg-open', file_path))
        except Exception as e:
            print("Error: ", e)
    def send():
        nonlocal label
        nonlocal button1
        nonlocal button2
        nonlocal button3
        label.destroy()
        button1.destroy()
        button2.destroy()
        button3.destroy()
        label = tk.Label(rootwin, text="Please wait..\nUploading error log to server...", relief="sunken", padx=5, pady=5, wraplength=200, justify="left", anchor="nw")
        label.config(font=("Arial", 12), bg="white", bd=1, highlightthickness=1, highlightbackground="black")
        label.pack(padx=10, pady=10)
        progressbar = ttk.Progressbar(rootwin, orient="horizontal", length=300, mode="indeterminate")
        progressbar.pack(pady=10)
        progressbar.start()
        if root is None:
            rootwin.update() # might error
        bytes_io = io.BytesIO()
        pickle.dump(snapshot, bytes_io) # serialize the snapshot to be used later in the memory analyzer
        bytes_io.seek(0)
        data = {'log':b64encode(open(fileloc,"rb").read()).decode(),'snapshot':b64encode(bytes_io.read()).decode()}
        response = requests.post(reportserver, json=data)
        bytes_io.close()
        rootwin.destroy()
    label.pack(padx=10, pady=10)
    button1 = tk.Button(root, text="Send report",command=send)
    button1.pack(side=tk.LEFT)

    button2 = tk.Button(root, text="Do not send report",command=rootwin.destroy)
    button2.pack(side=tk.LEFT)
    button3 = tk.Button(root, text="View report",command=lambda:owde(fileloc))
    button3.pack(side=tk.LEFT)
    if root is None:
        rootwin.mainloop()
if __name__ == "__main__":
    # Example
    run(lambda: 1 / 0,"http://example.com/upload",None,None)
