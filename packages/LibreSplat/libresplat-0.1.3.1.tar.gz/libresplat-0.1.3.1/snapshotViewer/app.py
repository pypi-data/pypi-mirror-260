# the snapshot viewer must be safe as it uses pickles!
import pickle
import tracemalloc
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter.filedialog import askopenfile
class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Restrict unpickling to specific safe modules
        safe_modules = {'tracemalloc': tracemalloc}
        if module in safe_modules:
            return safe_modules[module].__dict__.get(name)
        messagebox.showerror("Unsafe pickle","This pickle is unsafe, so we\nblocked you from accessing it")
        raise pickle.UnpicklingError("Global '%s.%s' is forbidden" % (module, name))

def safe_loads(s):
    return SafeUnpickler(io.BytesIO(s)).load()
root = Tk()
button1 = Button(root, text="Select Pickle",command=lambda:update_ui(SafeUnpickler(askopenfile(mode ='r+b', filetypes =[('Snapshot files', '*.pickle')])).load()))
button1.grid(row=0, column=0)
sizevar = StringVar()
label = Label( root, textvariable=sizevar, relief=RAISED )
sizevar.set("Total Memory Usage: N/A")
bsizevar = StringVar()
bloklabel = Label( root, textvariable=bsizevar, relief=RAISED )
bsizevar.set("Total Blocks Used: N/A")
def update_ui(snapshot):
    stats = snapshot.statistics("lineno")
    sizevar.set(f"Total Memory Usage: {stats[0].size // 1024}kb")
    bsizevar.set(f"Total Blocks Used: {stats[0].count}")
label.grid(row=1, column=0)
bloklabel.grid(row=2, column=0)
root.mainloop()
