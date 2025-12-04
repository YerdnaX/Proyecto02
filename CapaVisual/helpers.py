import tkinter as tk
from tkinter import ttk


def _safe_get(entry: tk.Entry) -> str:
    return entry.get().strip()


def apply_modern_dark(root: tk.Tk) -> None:
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    bg = "#1E1E1E"
    panel = "#242424"
    fg = "#F0F0F0"
    hover = "#505050"
    button = "#3C3C3C"
    border = "#444444"
    focus = "#5A5A5A"
    alt_row = "#2a2a2a"
    sel_bg = "#3f6ad8"
    sel_fg = "#ffffff"

    root.configure(bg=bg)

    style.configure(".", background=panel, foreground=fg, font=("Segoe UI", 10))
    style.configure("TFrame", background=panel, borderwidth=0, relief="flat")
    style.configure("TLabel", background=panel, foreground=fg)
    style.configure(
        "TButton",
        background=button,
        foreground=fg,
        borderwidth=0,
        focusthickness=1,
        focuscolor=panel,
        padding=6,
    )
    style.map(
        "TButton",
        background=[("active", hover), ("pressed", hover)],
        foreground=[("disabled", "#888888")],
    )

    style.configure(
        "TEntry",
        fieldbackground=panel,
        foreground=fg,
        bordercolor=border,
        lightcolor=focus,
        darkcolor=border,
        insertcolor=fg,
        padding=6,
    )
    style.map(
        "TEntry",
        fieldbackground=[("disabled", "#2a2a2a"), ("readonly", "#2a2a2a")],
        bordercolor=[("focus", focus)],
    )

    style.configure(
        "TCombobox",
        fieldbackground=panel,
        background=panel,
        foreground=fg,
        arrowcolor=fg,
        bordercolor=border,
        lightcolor=focus,
        darkcolor=border,
        padding=6,
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", panel)],
        bordercolor=[("focus", focus)],
        arrowcolor=[("active", fg)],
    )

    style.configure(
        "Treeview",
        background=panel,
        fieldbackground=panel,
        foreground=fg,
        bordercolor=border,
        lightcolor=border,
        darkcolor=border,
        rowheight=24,
    )
    style.map(
        "Treeview",
        background=[("selected", sel_bg)],
        foreground=[("selected", sel_fg)],
    )
    style.configure("Treeview.Heading", background=panel, foreground=fg, bordercolor=border)
    style.layout(
        "Treeview",
        [
            (
                "Treeview.field",
                {
                    "sticky": "nswe",
                    "border": 0,
                    "children": [
                        ("Treeview.padding", {"sticky": "nswe", "children": [("Treeview.treearea", {"sticky": "nswe"})]})
                    ],
                },
            )
        ],
    )
    style.configure("oddrow", background=panel)
    style.configure("evenrow", background=alt_row)

    style.configure(
        "TNotebook",
        background=bg,
        borderwidth=0,
    )
    style.configure(
        "TNotebook.Tab",
        background=bg,
        foreground=fg,
        padding=(10, 5),
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", panel)],
        foreground=[("selected", fg)],
    )

    style.configure(
        "Vertical.TScrollbar",
        gripcount=0,
        background=panel,
        troughcolor=bg,
        bordercolor=border,
        arrowcolor=fg,
    )
    style.map("Vertical.TScrollbar", background=[("active", hover)])
    style.configure(
        "Horizontal.TScrollbar",
        gripcount=0,
        background=panel,
        troughcolor=bg,
        bordercolor=border,
        arrowcolor=fg,
    )
    style.map("Horizontal.TScrollbar", background=[("active", hover)])
