import tkinter as tk
import subprocess

class Terminal(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.text = tk.Text(self, height=20, width=80, bg="black", fg="white")
        self.text.pack(fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self, bg="red", fg="white", insertbackground="white")
        self.entry.pack(fill=tk.X)

        # Bind the Enter key press event to the run_command function
        self.entry.bind("<Return>", self.run_command)

        self.history = []
        self.history_index = 0

        self.prompt = '> '
        self.text.insert(tk.END, self.prompt)

    def run_command(self, event):
        command = self.entry.get()
        self.history.append(command)
        self.history_index = len(self.history)

        self.text.insert(tk.END, "\n" + self.prompt + command + "\n")

        try:
            if command.startswith("cd "):
                path = command[3:]
                subprocess.run(command, shell=True, cwd=path)
            else:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                self.text.insert(tk.END, output + "\n")
        except subprocess.CalledProcessError as e:
            self.text.insert(tk.END, "Error: " + str(e) + "\n")

        self.text.insert(tk.END, self.prompt)
        self.entry.delete(0, tk.END)

    def handle_up_key(self, event):
        if self.history_index > 0:
            self.history_index -= 1
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.history[self.history_index])

    def handle_down_key(self, event):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.history[self.history_index])
        elif self.history_index == len(self.history) - 1:
            self.history_index += 1
            self.entry.delete(0, tk.END)

if __name__ == "__main__":
    import os

    root = tk.Tk()
    root.title("Terminal")
    root.geometry("1920x1080")
    root.configure(bg="black")
    terminal = Terminal(root)
    terminal.pack(fill=tk.BOTH, expand=True)

    root.bind("<Up>", terminal.handle_up_key)
    root.bind("<Down>", terminal.handle_down_key)

    root.mainloop()
