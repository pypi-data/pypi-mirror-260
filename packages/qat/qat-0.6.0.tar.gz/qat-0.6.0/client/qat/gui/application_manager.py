# -*- coding: utf-8 -*-
# (c) Copyright 2023, Qat’s Authors

"""
Provides the ApplicationManager class
"""

from pathlib import Path
import os

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

from qat.gui import gui_utils
from qat.gui.spy_window import SpyWindow
from qat import app_launcher
import qat

# pylint: disable=attribute-defined-outside-init

class ApplicationManager():
    """
    Show a GUI to manage applications
    """
    def __init__(self, root: tk.Tk) -> None:
        self._config_file = qat.get_config_file()
        self._image_path = Path(os.path.dirname(
            __file__)).resolve().absolute() / 'images'
        self._root = root
        self.is_editing = False
        self.is_adding = False
        self.applications = {}
        self.generate_start_window()


    def generate_start_window(self):
        """
        Create components the ApplicationManager window
        """
        self._start_window = tk.Toplevel(self._root)
        self._start_window.title('Qat Application Manager')
        self._start_window.resizable(False, False)
        self._start_window.protocol("WM_DELETE_WINDOW", self._root.destroy)

        self._generate_toolbar()
        self._generate_editing_area()


    def _generate_editing_area(self):
        image_dir = self._image_path
        # Add text field frame
        self.text_fields = tk.Frame(self._start_window, padx = 5, pady = 3)
        self.text_fields.grid(row=1, column=0, sticky='w')

        # Browse button
        self.browse_button = tk.Button(
            self.text_fields, text="Browse...", command=self.browse_application, state=tk.DISABLED)
        self.browse_button.grid(column=2, row=0)

        # Text
        self.path_label = tk.Label(self.text_fields, text="Path:")
        self.path_label.grid(row=0, column=0, sticky='w')
        self.args_label = tk.Label(self.text_fields, text="Arguments:")
        self.args_label.grid(row=2, column=0, sticky='w')

        # scrollbars
        self.path_scrollbar = ttk.Scrollbar(
            self.text_fields, orient='horizontal')
        self.path_scrollbar.grid(row=1, column=1, sticky='ew')
        self.args_scrollbar = ttk.Scrollbar(
            self.text_fields, orient='horizontal')
        self.args_scrollbar.grid(row=3, column=1, sticky='ew')

        # Text fields
        self.text_widget_path = tk.Entry(
            self.text_fields, width=100, state=tk.NORMAL,
            xscrollcommand=self.path_scrollbar.set, disabledforeground="gray30")
        if self.combobox.get() in self.applications:
            self.text_widget_path.insert(
                tk.END, self.applications[self.combobox.get()]['path'])
        self.text_widget_path["state"] = tk.DISABLED
        self.text_widget_path.grid(row=0, column=1, sticky='ew')
        self.path_scrollbar.configure(command=self.text_widget_path.xview)

        self.text_widget_args = tk.Entry(
            self.text_fields, width=100, state=tk.NORMAL,
            xscrollcommand=self.args_scrollbar.set, disabledforeground="gray30")
        if self.combobox.get() in self.applications:
            self.text_widget_args.insert(
                tk.END, self.applications[self.combobox.get()]['args'])
        self.text_widget_args["state"] = tk.DISABLED
        self.text_widget_args.grid(row=2, column=1, sticky='ew')
        self.args_scrollbar.configure(command=self.text_widget_args.xview)

        self.spy_window = SpyWindow(self._root, self._start_window)
        self.spy_window.generate_spy_window(image_dir)


    def _generate_toolbar(self):
        image_dir = self._image_path
        # Add toolbar
        toolbar = tk.Frame(self._start_window, padx=5, pady=3)
        toolbar.grid(row=0, column=0, sticky='w')

        # Combobox creation
        self.combobox = ttk.Combobox(toolbar, state="readonly", width=50)
        self.applications = qat.list_applications()
        if len(self.applications) > 0:
            self.combobox['values'] = list(i for i in self.applications)
            self.combobox.current(0)

        self.combobox.grid(row=0, column=0, padx=(0, 5), sticky='nsw')

        self.combobox.bind("<<ComboboxSelected>>", self._update_text_fields)

        # Start button
        self.start_icon = tk.PhotoImage(file=image_dir / "start_icon.png")
        self.start_button = tk.Button(
            toolbar, text="Start", image=self.start_icon, command=self.start_application)
        self.start_button.grid(column=1, row=0, sticky='w')

        # Add button
        self.add_icon = tk.PhotoImage(file=image_dir / "add_icon.png")
        self.add_button = tk.Button(
            toolbar, text="Add", image=self.add_icon, command=self.add_application)
        self.add_button.grid(column=3, row=0, sticky='w')

        # Edit button
        self.edit_icon = tk.PhotoImage(file=image_dir / "edit_icon.png")
        self.edit_button = tk.Button(
            toolbar, text="Edit", image=self.edit_icon, command=self.edit_application)
        self.edit_button.grid(column=2, row=0, sticky='w')

        # Save button
        self.save_icon = tk.PhotoImage(file=image_dir / "save_icon.png")
        self.save_button = tk.Button(
            toolbar,
            text="Save",
            image=self.save_icon,
            command=self.register_application,
            state=tk.DISABLED)
        self.save_button.grid(column=4, row=0, sticky='w')

        # Delete button
        self.delete_icon = tk.PhotoImage(file=image_dir / "delete_icon.png")
        self.delete_button = tk.Button(
            toolbar, text="Delete", image=self.delete_icon, command=self.open_delete_dialog)
        self.delete_button.grid(column=5, row=0)

        # Create a tooltip for each buttons of the toolbar
        gui_utils.create_button_tooltip(toolbar, 1.0)

    def _update_text_fields(self, _):
        if self.is_adding:
            selection = self.combobox.get()
            self.add_application()
            self.combobox.set(selection)

        self.combobox.select_clear()

        self.text_widget_path['state'] = tk.NORMAL
        self.text_widget_path.delete(0, tk.END)
        self.text_widget_path.insert(
            tk.END, self.applications[self.combobox.get()]['path'])
        self.text_widget_args['state'] = tk.NORMAL
        self.text_widget_args.delete(0, tk.END)
        self.text_widget_args.insert(
            tk.END, self.applications[self.combobox.get()]['args'])

        self.text_widget_path['state'] = tk.DISABLED
        self.text_widget_args['state'] = tk.DISABLED

    def start_application(self):
        """
        Launch the selected application
        """
        self._start_window.withdraw()

        app_name = self.combobox.get()
        try:
            qat.start_application(app_name, self.applications[app_name]['args'])
            qat.unlock_application()
        except Exception as error: # pylint: disable=broad-exception-caught
            messagebox.showerror(
                "Error",
                f"Could not launch application: {str(error)}",
                parent=self._start_window)
            self._start_window.deiconify()
            return

        self.spy_window.populate_tree([])
        self.spy_window.show()


    def edit_application(self):
        """
        Edit selected application (path and args)
        """
        if not self.is_editing:
            self.is_editing = True
            self.start_button['state'] = tk.DISABLED
            self.add_button['state'] = tk.DISABLED
            self.delete_button['state'] = tk.DISABLED
            self.combobox['state'] = tk.DISABLED
            self.save_button['state'] = tk.NORMAL
            self.browse_button['state'] = tk.NORMAL
            self.text_widget_path['state'] = tk.NORMAL
            self.text_widget_args['state'] = tk.NORMAL
        else:
            self.is_editing = False
            self.start_button['state'] = tk.NORMAL
            self.add_button['state'] = tk.NORMAL
            self.delete_button['state'] = tk.NORMAL
            self.combobox['state'] = 'readonly'
            self.save_button['state'] = tk.DISABLED
            self.browse_button['state'] = tk.DISABLED

            # discard changes
            self.text_widget_path.delete(0, tk.END)
            self.text_widget_path.insert(
                tk.END, self.applications[self.combobox.get()]['path'])
            self.text_widget_args.delete(0, tk.END)
            self.text_widget_args.insert(
                tk.END, self.applications[self.combobox.get()]['args'])

            self.text_widget_path['state'] = tk.DISABLED
            self.text_widget_args['state'] = tk.DISABLED
        self.edit_button.config(
            relief="sunken" if self.is_editing else "raised")


    def add_application(self):
        """
        Define a new application
        """
        self.is_adding = not self.is_adding
        self.add_button.config(relief="sunken" if self.is_adding else "raised")
        if self.is_adding:
            self.start_button['state'] = tk.DISABLED
            self.edit_button['state'] = tk.DISABLED
            self.delete_button['state'] = tk.DISABLED
            self.save_button['state'] = tk.NORMAL
            self.browse_button['state'] = tk.NORMAL

            self.combobox['state'] = tk.NORMAL
            self.combobox.set('')

            self.text_widget_path['state'] = tk.NORMAL
            self.text_widget_path.delete(0, tk.END)

            self.text_widget_args['state'] = tk.NORMAL
            self.text_widget_args.delete(0, tk.END)
        else:
            self.start_button['state'] = tk.NORMAL
            self.edit_button['state'] = tk.NORMAL
            self.delete_button['state'] = tk.NORMAL
            self.save_button['state'] = tk.DISABLED
            self.browse_button['state'] = tk.DISABLED

            self.combobox['state'] = 'readonly'
            self.combobox.current(0)

            self.text_widget_path.delete(0, tk.END)
            self.text_widget_args.delete(0, tk.END)
            self.text_widget_path.insert(
                tk.END, self.applications[self.combobox.get()]['path'])
            self.text_widget_args.insert(
                tk.END, self.applications[self.combobox.get()]['args'])
            self.text_widget_path['state'] = tk.DISABLED
            self.text_widget_args['state'] = tk.DISABLED


    def register_application(self):
        """
        Register a new application to the configuration file
        """

        if len(self.combobox.get()) == 0 or len(self.text_widget_path.get().strip()) == 0:
            return

        qat.register_application(
            self.combobox.get(),
            self.text_widget_path.get().strip(),
            self.text_widget_args.get().strip(),
            None)

        self.combobox['state'] = 'readonly'
        self.text_widget_path['state'] = tk.DISABLED
        self.text_widget_args['state'] = tk.DISABLED
        self.applications = qat.list_applications()
        self.combobox['values'] = list(i for i in self.applications)

        self.start_button['state'] = tk.NORMAL
        self.edit_button['state'] = tk.NORMAL
        self.add_button['state'] = tk.NORMAL
        self.delete_button['state'] = tk.NORMAL
        self.save_button['state'] = tk.DISABLED
        self.browse_button['state'] = tk.DISABLED
        self.is_editing = False
        self.edit_button.config(relief="raised")


    def browse_application(self):
        """
        Use a File selector dialog to select an application
        """
        extension = '*'
        if app_launcher.is_windows():
            extension = '*.exe'
        filename = filedialog.askopenfilename(
            initialdir="C:/",
            title="Select a File",
            filetypes=[("Applications", extension)],
            parent=self._start_window
        )

        if filename:
            self.text_widget_path.delete(0, tk.END)
            self.text_widget_path.insert(tk.END, filename)


    def open_delete_dialog(self):
        """
        Display a confirmation dialog when deleting an application
        """
        answer = messagebox.askokcancel(
            "Remove application",
            "Are you sure you want to delete '" +
            self.combobox.get() + "' from the application list?",
            parent=self._start_window)
        if answer:
            self.delete_application()


    def delete_application(self):
        """
        Remove an application for the configuration file
        """
        qat.unregister_application(self.combobox.get(), None)

        self.combobox['state'] = 'readonly'
        self.text_widget_path['state'] = tk.NORMAL
        self.text_widget_args['state'] = tk.NORMAL
        self.text_widget_path.delete(0, tk.END)
        self.text_widget_args.delete(0, tk.END)

        self.applications = qat.list_applications()
        self.combobox['values'] = list(i for i in self.applications)

        self.combobox.current(0)
        self.text_widget_path.insert(
            tk.END, self.applications[self.combobox.get()]['path'])
        self.text_widget_args.insert(
            tk.END, self.applications[self.combobox.get()]['args'])

        self.text_widget_path['state'] = tk.DISABLED
        self.text_widget_args['state'] = tk.DISABLED
