# -*- coding: utf-8 -*-
# (c) Copyright 2024, Qat’s Authors

"""
Provides utilities to help work with GUI components.
"""

import tkinter as tk
from tktooltip import ToolTip


def create_button_tooltip(
    widget : tk.Widget,
    delay: float = 0.0):
    """
    Create a tooltip to all button under the widget.
    Assign button text to the tooltip.  

    Parameters
    ----------
    widget : tk.Widget
        The parent widget where to create the tooltip
    delay : float, optional
        Delay in seconds before the ToolTip appears, by default 0.0
    """
    for children in widget.winfo_children():
        if isinstance(children, tk.Button):
            ToolTip(children, msg=children['text'], delay=delay)
