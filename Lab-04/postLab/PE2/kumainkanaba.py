import tkinter as tk
import tkinter.messagebox as mb
import tkinter.filedialog as fd

# Create root window but keep it hidden
root = tk.Tk()
root.withdraw()

# --- Message boxes ---
mb.showinfo("Info", "This is an info message")
mb.showwarning("Warning", "This may not work...")
mb.showerror("Error", "Oops!")

answer1 = mb.askyesno("Yes/No", "Kumain ka na?")
print("askyesno:", answer1)   # True / False

answer2 = mb.askokcancel("OK/Cancel", "Totoo ba yan?")
print("askokcancel:", answer2)  # True / False

answer3 = mb.askquestion("Question", "Wehhh?")
print("askquestion:", answer3)  # 'yes' / 'no'

answer4 = mb.askretrycancel("Retry/Cancel", "Isa pa?")
print("askretrycancel:", answer4)  # True / False

answer5 = mb.askyesnocancel("Yes/No/Cancel", "Ok?")
print("askyesnocancel:", answer5)  # True / False / None

# --- File dialog ---
file_path = fd.askopenfilename(
    title="Select a text file",
    filetypes=[("Text files", ".txt"), ("All files", ".*")]
)

if file_path:
    mb.showinfo("Selected File", f"You chose:\n{file_path}")
    print("Selected file:", file_path)
else:
    mb.showinfo("No File", "No file selected.")
    print("No file selected.")