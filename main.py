import tkinter as tk
from tkinter import ttk, filedialog

from functions import directory_purifier, directory_files_renamed_sequentially_by_last_edit


class DirectoryPurifierGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Directory Purifier")

        # Split UI into three horizontal sections
        self.top_frame = tk.Frame(self.window)
        self.middle_frame = tk.Frame(self.window)
        self.bottom_frame = tk.Frame(self.window)

        self.top_frame.pack(side="top", fill="x")
        self.middle_frame.pack(fill="both", expand=True)
        self.bottom_frame.pack(side="bottom", fill="x")

        # Top section: big select directory button with directory selected text
        self.directory_name = tk.StringVar(value="")
        self.directory_label = tk.Label(self.top_frame, text="Select directory:")
        self.directory_label.pack(side="left")
        self.directory_button = tk.Button(self.top_frame, text="Browse", command=self.browse_directory)
        self.directory_button.pack(side="left")

        # Bottom section: logs of what happened
        self.logs_text = tk.Text(self.bottom_frame)
        self.logs_text.pack(fill="both", expand=True)

        # Middle section: 2 tabs
        self.tab_control = ttk.Notebook(self.middle_frame)

        self.sort_directory_tab = ttk.Frame(self.tab_control)
        self.directory_purifier_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.sort_directory_tab, text="Sort Directory Names")
        self.tab_control.add(self.directory_purifier_tab, text="Directory Purifier")
        self.tab_control.pack(fill="both", expand=True)

        # Tab 1: Sort directory names
        self.ascending = tk.BooleanVar(value=True)
        self.dry_run_sort = tk.BooleanVar(value=True)

        self.ascending_checkbutton = tk.Checkbutton(self.sort_directory_tab, text="Sort ascending", variable=self.ascending)
        self.ascending_checkbutton.pack()

        self.dry_run_sort_checkbutton = tk.Checkbutton(self.sort_directory_tab, text="Dry run (don't modify files)", variable=self.dry_run_sort)
        self.dry_run_sort_checkbutton.pack()

        self.start_sort_button = tk.Button(self.sort_directory_tab, text="Start", command=self.start_sorting)
        self.start_sort_button.pack()

        # Tab 2: Directory purifier
        self.chars_to_remove = tk.StringVar(value="")
        self.chars_label = tk.Label(self.directory_purifier_tab, text="Characters to remove from file names:")
        self.chars_label.pack()
        self.chars_entry = tk.Entry(self.directory_purifier_tab, textvariable=self.chars_to_remove)
        self.chars_entry.pack()

        self.dry_run_purify = tk.BooleanVar(value=True)
        self.dry_run_purify_checkbutton = tk.Checkbutton(self.directory_purifier_tab, text="Dry run (don't modify files)", variable=self.dry_run_purify)
        self.dry_run_purify_checkbutton.pack()

        self.start_purify_button = tk.Button(self.directory_purifier_tab, text="Start", command=self.start_purifying)
        self.start_purify_button.pack()

    def browse_directory(self):
        self.directory_name.set(filedialog.askdirectory())

    def start_purifying(self):
        output = directory_purifier( self.directory_name.get(),
                                    self.chars_to_remove.get(), 
                                    self.dry_run_purify.get())
        self.show_logs(output)

    def start_sorting(self):
        output = directory_files_renamed_sequentially_by_last_edit(self.directory_name.get(), self.ascending.get(), self.dry_run_sort.get())
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

