# -*- coding: utf-8 -*-
# (c) Copyright 2023, Qat’s Authors

"""
Provides the SpyWindow class
"""

import tkinter as tk
from tkinter import ttk
from qat.gui import gui_utils
import qat


class SpyWindow():
    """
    Main window of Qat Spy when connected to an application
    """
    # pylint: disable=attribute-defined-outside-init
    def __init__(self, root: tk.Tk, start_window) -> None:
        self._root = root
        self._start_window = start_window
        self.spy_window = None
        self.is_picking = False
        self._selected_object = None
        self.main_windows_list = []
        self.current_root_objects = []


    def generate_spy_window(self, image_dir):
        """
        Create components of the main window
        """
        self.spy_window = tk.Toplevel(self._root)
        self.spy_window.title('Qat Spy')
        self.spy_window.geometry('1000x600')
        self.spy_window.protocol("WM_DELETE_WINDOW", self.back_to_start)
        self.spy_window.withdraw()

        # Specify Grid
        tk.Grid.columnconfigure(self.spy_window, 0, weight=1)
        tk.Grid.columnconfigure(self.spy_window, 1, weight=1)
        tk.Grid.columnconfigure(self.spy_window, 2, weight=1)
        tk.Grid.columnconfigure(self.spy_window, 3, weight=1)
        tk.Grid.columnconfigure(self.spy_window, 4, weight=1)
        tk.Grid.rowconfigure(self.spy_window, 1, weight=1)

        # define columns
        columns = 'type'

        self.tree = ttk.Treeview(
            self.spy_window, columns=columns, selectmode='browse')

        # default column is accessed using #0
        self.tree.heading('#0', text="Object")
        self.tree.heading('type', text='Type')

        self.tree.bind('<<TreeviewOpen>>', self.item_opened)
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

        self.tree.grid(row=1, column=0, sticky='nsew')

        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.spy_window, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=1, sticky='ns')

        self.properties_tree = ttk.Treeview(
            self.spy_window, columns=("value"), selectmode='browse')
        # define headings
        self.properties_tree.heading('#0', text='Property')
        self.properties_tree.heading('value', text='Value')

        self.properties_tree.grid(row=1, column=2, sticky='nsew')

        # add a scrollbar
        vert_scrollbar = ttk.Scrollbar(
            self.spy_window, orient=tk.VERTICAL, command=self.properties_tree.yview)
        self.properties_tree.configure(yscroll=vert_scrollbar.set)
        vert_scrollbar.grid(row=1, column=3, sticky='ns')

        # Add toolbar
        self.toolbar = tk.Frame(self.spy_window, bd=1, relief=tk.RAISED)
        self.toolbar.grid(row=0, column=0, columnspan=3, sticky='we')

        # add picker button
        self.picker_icon = tk.PhotoImage(file=image_dir / "spy_icon.png")
        self.picker_button = tk.Button(
            self.toolbar, text="Picker", image=self.picker_icon, command=self.pick_item)
        self.picker_button.grid(row=0, column=0, sticky='w')

        # add up button
        self.up_icon = tk.PhotoImage(
            file=image_dir / "up_icon.png", master=self._root)
        self.up_button = tk.Button(
            self.toolbar, text="Up one level", image=self.up_icon, command=self.go_up)
        self.up_button.grid(row=0, column=1, sticky='w')

        # add refresh button
        self.refresh_icon = tk.PhotoImage(file=image_dir / "refresh_icon.png")
        self.refresh_button = tk.Button(
            self.toolbar, text="Refresh", image=self.refresh_icon, command=self.refresh)
        self.refresh_button.grid(row=0, column=2, sticky='w')

        self.pick_label = tk.Label(
            self.toolbar,
            text='While picking, hold CTRL to interact with app or SHIFT to pick background object',
            bd=0)
        self.pick_label.grid(row=0, column=3, sticky='w')

        # Create a tooltip for each buttons of the toolbar
        gui_utils.create_button_tooltip(self.toolbar, 1.0)


    def show(self):
        """
        Display the main window
        """
        self.spy_window.deiconify()
        self.is_picking = False


    def back_to_start(self):
        """
        Close current application and display the Application Manager window
        """
        try:
            qat.close_application()
        except: # pylint: disable=bare-except
            print("Could not close application")

        self.spy_window.withdraw()
        self._start_window.deiconify()


    def go_up(self):
        """
        Select the parent object in the tree
        """
        # If no item is selected choose the first item in tree
        if len(self.tree.selection()) > 0:
            selected_id = self.tree.selection()[0]
        else:
            selected_id = self.tree.get_children('')[0]

        parent = self.tree.parent(selected_id)
        if parent:
            self.tree.focus(parent)
            self.tree.selection_set(parent)
        else:
            selected_object = self.ids[selected_id]
            try:
                parent_object = selected_object.parent
                if parent_object.get_definition() is not None:
                    self.populate_tree(parent_object)
                else:
                    self.populate_tree([])
            except Exception: # pylint: disable=broad-exception-caught
                pass


    def populate_tree(self, root_object_list):
        """
        Populate the object tree from the given root objects
        """
        if not isinstance(root_object_list, list):
            root_object_list = [root_object_list]

        self.current_root_objects = root_object_list
        if len(root_object_list) == 0:
            root_object_list = qat.list_top_windows()

        self.tree.delete(*self.tree.get_children())

        self.ids = {}

        for root_object in root_object_list:
            root_id = self.tree.insert('', tk.END, text=str(
                root_object), values=(root_object.className,), open=False)
            self.ids[root_id] = root_object

            if len(root_object.children) > 0:
                self.tree.insert(root_id, index=0, text="loading",
                                 values=("loading",), open=False)

        self.refresh_properties()


    def refresh_properties(self):
        """
        Refresh all values in the property table
        """
        if len(self.tree.selection()) == 0:
            self.properties_tree.delete(*self.properties_tree.get_children())
            return
        selected_object = self.ids[self.tree.selection()[0]]
        self.populate_properties(selected_object)


    def refresh(self):
        """
        Refresh all elements and preserve selection if possible
        """
        self.populate_tree(self.current_root_objects)


    def populate_properties(self, selected_object):
        """
        Populate the property table for the given object
        """
        # pylint: disable=bare-except
        self.properties_tree.delete(*self.properties_tree.get_children())
        properties = self.sort_properties(selected_object.list_properties())
        for prop in properties:
            try:
                value = prop[1]
                tree_id = self.properties_tree.insert(
                    '', tk.END, text=prop[0], values=(str(value),), open=False)
                if isinstance(value, qat.QtObject):
                    self.add_object(tree_id, value)
                elif isinstance(value, qat.QtCustomObject):
                    self.add_custom_object(tree_id, value)

            except:
                pass


    def add_object(self, tree_id, qt_object: qat.QtObject):
        """
        Add the given object to the property table
        """
        properties = self.sort_properties(qt_object.list_properties())
        for prop in properties:
            try:
                property_value = prop[1]
                child_id = self.properties_tree.insert(
                    tree_id,
                    tk.END,
                    text=prop[0],
                    values=(str(property_value),), open=False)
                if isinstance(property_value, qat.QtCustomObject):
                    self.add_custom_object(child_id, property_value)

            except Exception: # pylint: disable=broad-exception-caught
                pass


    def add_custom_object(self, tree_id, custom_object: qat.QtCustomObject):
        """
        Add the given custom object to the property table
        """
        for prop in custom_object:
            try:
                property_value = custom_object[prop]
                self.properties_tree.insert(
                    tree_id,
                    tk.END,
                    text=prop,
                    values=(str(property_value),),
                    open=False)
            except: # pylint: disable=bare-except
                pass


    def sort_properties(self, properties: list) -> list:
        """
        Sort given properties to move most important ones to the beginning of the list
        """
        properties = dict(properties)
        properties = dict(sorted(properties.items()))
        # Parent and children are in the tree
        if 'children' in properties:
            del properties['children']
        if 'parent' in properties:
            del properties['parent']
        top_properties_names = ['objectName', 'type', 'id']
        top_properties = {}
        for top_prop in top_properties_names:
            if top_prop in properties:
                top_properties[top_prop] = properties[top_prop]
                del properties[top_prop]

        return list(top_properties.items()) + list(properties.items())


    def item_opened(self, _):
        """
        Callback when an item is opened in the tree.
        Populate children of the expanded object.
        """
        selected_id = self.tree.selection()[0]
        selected_children_ids = self.tree.get_children(selected_id)
        if len(selected_children_ids) > 1:
            # Tree has already been expanded
            return
        for temp_id in selected_children_ids:
            self.tree.delete(temp_id)
        children = self.ids[selected_id].children
        for child in reversed(children):
            if child.type == 'RootItem':
                continue
            tree_id = self.tree.insert(selected_id, index=0, text=str(
                child), values=(child.className,), open=False)
            self.ids[tree_id] = child
            if len(child.children) > 0:
                self.tree.insert(tree_id, index=0, text="loading",
                                 values=("loading",), open=False)


    def item_selected(self, _):
        """
        Callback when an item is selected in the tree.
        Populate the property table.
        """
        if len(self.tree.selection()) == 0:
            self.properties_tree.delete(*self.properties_tree.get_children())
            self._selected_object = None
            return
        selected_object = self.ids[self.tree.selection()[0]]
        if selected_object == self._selected_object:
            return
        self._selected_object = selected_object
        self.populate_properties(selected_object)


    def pick_item(self):
        """
        Toggle picking mode
        """
        self.is_picking = not self.is_picking
        self.picker_button.config(
            relief="sunken" if self.is_picking else "raised")
        self.up_button["state"] = tk.DISABLED if self.is_picking else tk.NORMAL
        if self.is_picking:
            self.wait_for_picker()
        else:
            try:
                for conn in self._picker_connections:
                    qat.disconnect(conn)
                self._picker_connections = []
                qat.deactivate_picker()
            except: # pylint: disable=bare-except
                print('error while deactivating picker')


    def wait_for_picker(self):
        """
        Connect to the object picker to retrieve the picked object
        """
        def set_picked_object(picked_object):
            self.populate_tree(picked_object)
            first_id = self.tree.get_children('')[0]
            self.tree.focus(first_id)
            self.tree.selection_set(first_id)
            self.picker_button.invoke()

        if self.is_picking:
            try:
                qat.activate_picker()
                picker_def = {
                    'objectName': 'QatObjectPicker'
                }

                pickers = qat.find_all_objects(picker_def)
                self._picker_connections = []
                for picker in pickers:
                    self._picker_connections.append(qat.connect(
                        picker, 'pickedObject', set_picked_object))
            except: # pylint: disable=bare-except
                print('error while activating picker')
                self.picker_button.invoke()
