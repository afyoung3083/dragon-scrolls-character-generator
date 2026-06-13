# ============================================================
# THEME
# Colors, fonts, and reusable widget styling helpers for the
# Dragon Scrolls GUI.
#
# This module controls the visual language of the app:
# - stone dungeon UI
# - red/gold fantasy buttons
# - pixel-art title/banner colors
# - parchment-style text panels
#
# This file should NOT generate characters.
# This file should NOT save files.
# This file should NOT build PDFs.
# This file should NOT create the main window.
# ============================================================

import random
import tkinter as tk
from tkinter import scrolledtext


# ============================================================
# CORE COLOR PALETTE
# These are the main colors used across the entire interface.
# ============================================================

# Dark stone colors for the main app background and panels.
COLOR_STONE_DARK = "#2b2b2b"
COLOR_STONE = "#3a3a3a"
COLOR_STONE_LIGHT = "#555555"

# Gold and red give the app its old-school fantasy menu feel.
COLOR_GOLD = "#d4af37"
COLOR_RED = "#7b1e1e"
COLOR_RED_DARK = "#4a1010"

# Text colors.
COLOR_TEXT_DARK = "#1f1a12"
COLOR_TEXT_LIGHT = "#f5e6b8"

# Deep shadow used for borders and dark edges.
COLOR_BORDER_SHADOW = "#1a1a1a"


# ============================================================
# PIXEL PARCHMENT PALETTE
# These colors replace the old flat yellow look.
#
# Visual rule:
# - SHADOW: outside edge / deepest border
# - DARK: dark pixel edge
# - MID: parchment panel body
# - LIGHT: readable writing surface
# - INK: text color
# ============================================================

COLOR_PARCHMENT_LIGHT = "#ead8aa"
COLOR_PARCHMENT_MID = "#b8844b"
COLOR_PARCHMENT_DARK = "#7a4b25"
COLOR_PARCHMENT_SHADOW = "#3f2614"
COLOR_PARCHMENT_EDGE = "#5b351b"
COLOR_PARCHMENT_HIGHLIGHT = "#f4dfad"
COLOR_INK = "#241407"

# Backward-compatible names.
# These keep older code working while letting the newer palette
# drive the visual style.
COLOR_PARCHMENT = COLOR_PARCHMENT_LIGHT
COLOR_TEXT_DARK = COLOR_INK


# ============================================================
# GRIMOIRE / NOTEBOOK FRAME COLORS
# These are used around the notebook and large content areas.
# ============================================================

COLOR_GRIMOIRE_BORDER = COLOR_GOLD
COLOR_GRIMOIRE_INNER_BORDER = COLOR_RED_DARK
COLOR_GRIMOIRE_PAGE = COLOR_PARCHMENT_LIGHT
COLOR_GRIMOIRE_PAGE_DARK = COLOR_PARCHMENT_MID
COLOR_GRIMOIRE_INK = COLOR_INK
COLOR_GRIMOIRE_SHADOW = "#171717"


# ============================================================
# PIXEL STONE TITLE BANNER COLORS
# These are used by header_art.py to draw the 80s-style stone
# title banner and torch area.
# ============================================================

COLOR_STONE_BANNER = "#6f6a5c"

PIXEL_STONE_COLORS = [
    "#5f5a4f",
    "#6b665a",
    "#777263",
    "#4f4b42",
    "#888272"
]

PIXEL_MORTAR_COLOR = "#2f2c27"
PIXEL_STONE_OUTLINE = "#3b3832"
PIXEL_STONE_HIGHLIGHT = "#9a9483"
PIXEL_STONE_SHADOW = "#47433b"
PIXEL_TITLE_SHADOW = "#3d2608"


# ============================================================
# NOTEBOOK TAB COLORS
# ttk.Notebook tabs need their own style setup in the main GUI.
# These constants are used by apply_theme() in the main file.
# ============================================================

COLOR_TAB_BG = "#4a1010"
COLOR_TAB_ACTIVE = "#5c1818"
COLOR_TAB_SELECTED = "#7b1e1e"
COLOR_TAB_TEXT = "#f5e6b8"
COLOR_TAB_SELECTED_TEXT = "#d4af37"
COLOR_TAB_BORDER = "#d4af37"


# ============================================================
# PIXEL PARCHMENT DECORATION CONSTANTS
# These are used to create visible pixel-art wear, chips,
# and discoloration on parchment panel borders.
# ============================================================

PIXEL_PANEL_SIZE = 4

PARCHMENT_WEAR_LIGHT = "#d9b37b"
PARCHMENT_WEAR_MEDIUM = "#b97841"
PARCHMENT_WEAR_DARK = "#6b3f20"
PARCHMENT_WEAR_GRAY = "#7c7260"

PARCHMENT_WEAR_COLORS = [
    PARCHMENT_WEAR_LIGHT,
    PARCHMENT_WEAR_MEDIUM,
    PARCHMENT_WEAR_DARK,
    PARCHMENT_WEAR_GRAY
]

# ============================================================
# FONT CONSTANTS
# Keep fonts centralized so the whole app can be adjusted from
# one place.
# ============================================================

TITLE_FONT = ("Georgia", 24, "bold")
LABEL_FONT = ("Georgia", 11, "bold")
BUTTON_FONT = ("Georgia", 10, "bold")

# Consolas gives the content areas a readable old-school RPG /
# terminal-adjacent feel.
TEXT_FONT = ("Consolas", 10)
TAB_TEXT_FONT = ("Consolas", 10)

NOTEBOOK_TAB_FONT = ("Consolas", 10, "bold")
NOTEBOOK_TAB_SELECTED_FONT = ("Consolas", 10, "bold")


# ============================================================
# LOW-LEVEL PARCHMENT HELPERS
# These helper functions create the blocky parchment effect.
# ============================================================

def style_pixel_parchment_frame(frame):
    """
    Style a normal frame as a pixel-parchment outer border.

    Use this for containers that should look like parchment panels.
    The effect is intentionally simple and blocky rather than
    photo-realistic.
    """
    frame.config(
        bg=COLOR_PARCHMENT_SHADOW,
        bd=0,
        highlightthickness=2,
        highlightbackground=COLOR_PARCHMENT_EDGE,
        highlightcolor=COLOR_PARCHMENT_EDGE
    )


def style_pixel_parchment_inner_frame(frame):
    """
    Style an inner frame as the warmer parchment body.

    This normally sits inside a darker outer parchment frame.
    """
    frame.config(
        bg=COLOR_PARCHMENT_MID,
        bd=0,
        highlightthickness=1,
        highlightbackground=COLOR_PARCHMENT_DARK,
        highlightcolor=COLOR_PARCHMENT_DARK
    )


def style_pixel_parchment_text_area(text_box):
    """
    Style a text widget as the light writing surface of a parchment
    panel.

    The readable part should be lighter than the surrounding panel.
    """
    text_box.config(
        bg=COLOR_PARCHMENT_LIGHT,
        fg=COLOR_INK,
        insertbackground=COLOR_INK,
        selectbackground=COLOR_PARCHMENT_DARK,
        selectforeground=COLOR_PARCHMENT_LIGHT,
        relief=tk.FLAT,
        bd=0,
        font=TEXT_FONT,
        padx=8,
        pady=8,
        highlightthickness=2,
        highlightbackground=COLOR_PARCHMENT_EDGE,
        highlightcolor=COLOR_PARCHMENT_EDGE
    )


# ============================================================
# DECORATIVE PIXEL PARCHMENT HELPERS
# These helpers add visible corner chips, edge wear, and
# pixel-art imperfections so the cards feel more retro and less
# like flat colored rectangles.
# ============================================================

def _make_pixel_block(parent, x, y, width_pixels, height_pixels, color):
    """
    Create a tiny solid-color block positioned with place().

    These little blocks are the building pieces for corner chips,
    wear marks, and discoloration.
    """
    block = tk.Frame(
        parent,
        bg=color,
        width=width_pixels * PIXEL_PANEL_SIZE,
        height=height_pixels * PIXEL_PANEL_SIZE,
        bd=0,
        highlightthickness=0
    )
    block.place(x=x, y=y)
    block.pack_propagate(False)
    return block


def _add_corner_cluster(parent, corner_name):
    """
    Add a small pixel-art damage / wear cluster to one corner
    of a parchment frame.
    """
    cluster_size = PIXEL_PANEL_SIZE * 5

    cluster = tk.Frame(
        parent,
        bg=parent.cget("bg"),
        width=cluster_size,
        height=cluster_size,
        bd=0,
        highlightthickness=0
    )
    cluster.pack_propagate(False)

    if corner_name == "top_left":
        cluster.place(x=2, y=2)
    elif corner_name == "top_right":
        cluster.place(relx=1.0, x=-(cluster_size + 2), y=2)
    elif corner_name == "bottom_left":
        cluster.place(x=2, rely=1.0, y=-(cluster_size + 2))
    elif corner_name == "bottom_right":
        cluster.place(relx=1.0, rely=1.0, x=-(cluster_size + 2), y=-(cluster_size + 2))

    _make_pixel_block(cluster, 0, PIXEL_PANEL_SIZE, 1, 3, PARCHMENT_WEAR_DARK)
    _make_pixel_block(cluster, PIXEL_PANEL_SIZE, 0, 3, 1, PARCHMENT_WEAR_LIGHT)
    _make_pixel_block(cluster, PIXEL_PANEL_SIZE, PIXEL_PANEL_SIZE, 1, 1, PARCHMENT_WEAR_GRAY)
    _make_pixel_block(cluster, PIXEL_PANEL_SIZE * 2, PIXEL_PANEL_SIZE * 2, 2, 1, PARCHMENT_WEAR_MEDIUM)
    _make_pixel_block(cluster, PIXEL_PANEL_SIZE * 3, PIXEL_PANEL_SIZE * 3, 1, 1, PARCHMENT_WEAR_DARK)


def _add_edge_wear(parent):
    """
    Add a few small worn marks and discoloration blocks around
    the border of a parchment frame.

    These are intentionally simple and pixel-ish rather than
    smooth or realistic.
    """
    width = 24
    height = 12

    top_mark = tk.Frame(parent, bg=PARCHMENT_WEAR_MEDIUM, width=width, height=height, bd=0, highlightthickness=0)
    top_mark.place(relx=0.35, y=2)
    top_mark.pack_propagate(False)

    bottom_mark = tk.Frame(parent, bg=PARCHMENT_WEAR_DARK, width=width, height=height, bd=0, highlightthickness=0)
    bottom_mark.place(relx=0.62, rely=1.0, y=-(height + 2))
    bottom_mark.pack_propagate(False)

    left_mark = tk.Frame(parent, bg=PARCHMENT_WEAR_GRAY, width=height, height=width, bd=0, highlightthickness=0)
    left_mark.place(x=2, rely=0.45)
    left_mark.pack_propagate(False)

    right_mark = tk.Frame(parent, bg=PARCHMENT_WEAR_MEDIUM, width=height, height=width, bd=0, highlightthickness=0)
    right_mark.place(relx=1.0, x=-(height + 2), rely=0.25)
    right_mark.pack_propagate(False)

    # Add a few extra tiny wear pixels at semi-random positions.
    for i in range(6):
        wear_width = random.choice([1, 2, 2, 3])
        wear_height = random.choice([1, 1, 2])
        wear_color = random.choice(PARCHMENT_WEAR_COLORS)

        tiny = tk.Frame(
            parent,
            bg=wear_color,
            width=wear_width * PIXEL_PANEL_SIZE,
            height=wear_height * PIXEL_PANEL_SIZE,
            bd=0,
            highlightthickness=0
        )
        tiny.pack_propagate(False)

        edge_choice = random.choice(["top", "bottom", "left", "right"])

        if edge_choice == "top":
            tiny.place(relx=random.uniform(0.10, 0.90), y=2)
        elif edge_choice == "bottom":
            tiny.place(relx=random.uniform(0.10, 0.90), rely=1.0, y=-(wear_height * PIXEL_PANEL_SIZE + 2))
        elif edge_choice == "left":
            tiny.place(x=2, rely=random.uniform(0.12, 0.88))
        else:
            tiny.place(relx=1.0, x=-(wear_width * PIXEL_PANEL_SIZE + 2), rely=random.uniform(0.12, 0.88))


def decorate_pixel_parchment_frame(parent):
    """
    Add all decorative pixel-art parchment elements to a frame.
    """
    _add_corner_cluster(parent, "top_left")
    _add_corner_cluster(parent, "top_right")
    _add_corner_cluster(parent, "bottom_left")
    _add_corner_cluster(parent, "bottom_right")
    _add_edge_wear(parent)

# ============================================================
# SHEET CARD CREATION
# Used by the main Sheet tab to create card-like sections such
# as Identity, Abilities, Combat, Equipment, Spells, and Features.
# ============================================================

def create_sheet_card(parent, title, width=38, height=12):
    """
    Create a readable themed sheet card.

    Important design choice:
    Keep the border thin so the actual text area stays large.
    Earlier decorative parchment frames looked cool in theory,
    but they consumed too much readable space.
    """

    # Outer card: simple dark stone frame with gold title.
    card_frame = tk.LabelFrame(
        parent,
        text=title,
        font=("Georgia", 10, "bold"),
        bg=COLOR_STONE,
        fg=COLOR_GOLD,
        bd=3,
        relief=tk.RIDGE,
        labelanchor="n"
    )

    # Thin parchment border frame.
    # This gives a parchment/card feeling without stealing space.
    inner_frame = tk.Frame(
        card_frame,
        bg=COLOR_PARCHMENT_EDGE,
        bd=0
    )
    inner_frame.pack(
        padx=5,
        pady=5,
        fill=tk.BOTH,
        expand=True
    )

    # Main readable text area.
    card_display = scrolledtext.ScrolledText(
        inner_frame,
        wrap=tk.WORD,
        font=TEXT_FONT,
        width=width,
        height=height,
        bg=COLOR_PARCHMENT_LIGHT,
        fg=COLOR_INK,
        insertbackground=COLOR_INK,
        relief=tk.FLAT,
        bd=0,
        padx=8,
        pady=8,
        highlightthickness=1,
        highlightbackground=COLOR_PARCHMENT_DARK,
        highlightcolor=COLOR_PARCHMENT_DARK
    )

    card_display.pack(
        padx=3,
        pady=3,
        fill=tk.BOTH,
        expand=True
    )

    return card_frame, card_display


# ============================================================
# GENERAL WIDGET STYLING HELPERS
# These are called from apply_theme() in the main GUI file.
# ============================================================

def style_button(button):
    """
    Apply the red/gold fantasy button style.

    Used for action buttons like Generate, Save, Print,
    Reroll Stats, Copy Prompt, etc.
    """
    button.config(
        bg=COLOR_RED,
        fg=COLOR_TEXT_LIGHT,
        activebackground=COLOR_RED_DARK,
        activeforeground=COLOR_GOLD,
        relief=tk.RAISED,
        bd=3,
        font=BUTTON_FONT,
        padx=6,
        pady=3
    )


def style_label(label):
    """
    Apply the standard gold-on-stone label style.

    Used for labels like Class, Species, Background, Level,
    Rolls, and other option labels.
    """
    label.config(
        bg=COLOR_STONE_DARK,
        fg=COLOR_GOLD,
        font=LABEL_FONT
    )


def style_text_box(text_box):
    """
    Apply the standard parchment text-box style.

    Used for the full-tab ScrolledText widgets, such as Summary,
    Abilities, Combat, Equipment, Spells, Spellbook, Roleplay,
    Features, and Image Prompt.
    """
    style_pixel_parchment_text_area(text_box)
