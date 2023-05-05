import tkinter as tk
from tkinter import filedialog

from functions import directory_purifier


class DirectoryPurifierGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Directory Purifier")

        # Directory picker
        self.directory_name = tk.StringVar(value="")
        self.directory_label = tk.Label(self.window, text="Select directory:")
        self.directory_label.pack(side="left")
        self.directory_button = tk.Button(self.window, text="Browse", command=self.browse_directory)
        self.directory_button.pack(side="left")

        # Text input for chars to remove
        self.chars_to_remove = tk.StringVar(value="")
        self.chars_label = tk.Label(self.window, text="Characters to remove from file names:")
        self.chars_label.pack()
        self.chars_entry = tk.Entry(self.window, textvariable=self.chars_to_remove)
        self.chars_entry.pack()

        # Check button for dry run
        self.dry_run = tk.BooleanVar(value=True)
        self.dry_run_checkbutton = tk.Checkbutton(self.window, text="Dry run (don't modify files)", variable=self.dry_run)
        self.dry_run_checkbutton.pack()

        # Start button
        self.start_button = tk.Button(self.window, text="Start", command=self.start_purifying)
        self.start_button.pack()

        # Logs text widget
        self.logs_text = tk.Text(self.window)
        self.logs_text.pack(fill="both", expand=True)

    def browse_directory(self):
        self.directory_name.set(filedialog.askdirectory())

    def start_purifying(self):
        output = directory_purifier(self.directory_name.get(), self.chars_to_remove.get(), self.dry_run.get())
        self.show_logs(output)

    def show_logs(self, output):
        # Clear the logs text widget
        self.logs_text.delete(1.0, "end")

        # Iterate through the list of tuples and display the old and new file names
        for old_name, new_name in output:
            self.logs_text.insert("end", f"{old_name} -> {new_name}\n")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = DirectoryPurifierGUI()
    gui.run()

