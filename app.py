import threading
import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog, messagebox

import pyperclip  # To access clipboard content

from handler import handler


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Handler App")

        # Set window background color to light beige
        self.root.configure(bg="#F5F5DC")

        # Polish instructions label
        # Polish instructions label
        self.instruction_label = tk.Label(root,
                                          text="Aby użyć, należy z Quizleta eksportować fiszki w następujący sposób:\n ... -> eksport -> \nPomiędzy pojęciem a definicją spacja;;;spacja \n Pomiędzy rzędami spacja!!!spacja \n -> kopiuj tekst.",
                                          wraplength=600, justify=tk.LEFT, bg="#F5F5DC")
        # Use pack() to avoid overlap and ensure proper display
        self.instruction_label.pack(padx=10, pady=20, anchor="w")
        self.file_path = ""
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30, bg="#F5F5DC")
        self.text_area.pack(padx=10, pady=10)

        # Create an indeterminate progress bar (infinite moving) with background color matching
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
        self.progress.pack(pady=10)

        self.process_button = tk.Button(root, text="select from files", command=self.select_from_files, bg="#F5F5DC")
        self.process_button.pack(pady=10)

        self.paste_button = tk.Button(root, text="ctrl-V", command=self.paste_csv, bg="#F5F5DC")
        self.paste_button.pack(pady=10)

        # Handler for CSV processing (can be adjusted based on actual handler implementation)
        self.handler_instance = handler(progress_callback=self.update_progress)
    def select_from_files(self):
        # Let the user select a CSV file
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not self.file_path:
            return
        # Start the progress bar animation
        self.progress.start()
        # Run CSV processing in a background thread to keep the UI responsive
        threading.Thread(target=self.run_csv_processing, daemon=True).start()

    def paste_csv(self):
        # Get clipboard content
        clipboard_content = pyperclip.paste()
        if clipboard_content:
            # Paste the content into the text area
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.INSERT, clipboard_content)
            # Start the progress bar animation
            self.progress.start()
            # Process the clipboard content in a background thread
            threading.Thread(target=self.run_csv_processing, args=(clipboard_content,), daemon=True).start()
        else:
            messagebox.showwarning("No Data", "Clipboard is empty or does not contain valid CSV data.")

    def run_csv_processing(self, csv_data=None):
        try:

            # Start the progress bar animation
            self.text_area.delete(1.0, tk.END)
            # If csv_data is provided (from clipboard), handle it directly
            if csv_data:
                # Ensure that csv_data is a string before processing
                if isinstance(csv_data, str):
                    output, total_lines, processed_lines = self.handler_instance.handle_from_data(csv_data)
                else:
                    raise ValueError("Clipboard data is not valid text.")
            else:
                output, total_lines, processed_lines = self.handler_instance.handle(self.file_path)
            # Insert the processed output into the text area
            self.text_area.insert(tk.INSERT, output)
            messagebox.showinfo("Success", "CSV processing completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")
        finally:
            # Stop the progress bar animation
            self.progress.stop()

    def update_progress(self, processed_lines, total_lines):
        # The progress bar is purely moving while CSV is processed
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
