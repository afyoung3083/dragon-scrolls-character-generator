# ============================================================
# IMPORTS
# External libraries used by the program.
#
# tkinter: builds the GUI.
# PIL / Pillow: handles pasted, chosen, resized, and displayed images.
# os/json: handles saved character bundles and printing.
# random: supports GUI-side reroll behavior and pixel-stone banner.
# ============================================================

# Built-in Python libraries
import json
import os
import random
import re

# Tkinter GUI libraries
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk

# Pillow image libraries
from PIL import Image, ImageTk

# Project modules
from data_tables import *
from character_generator import *
from text_generator import *
from pdf_exporter import *
from theme import *
from file_manager import *
from portrait_tools import *
from header_art import *

# ============================================================
# GLOBAL STATE
# These variables remember what character is currently loaded,
# what portrait image is currently loaded, where the character
# was saved, and what saved-character folder/list is active.
# ============================================================
current_character_data = None
current_portrait_image = None
current_portrait_photo = None
current_character_file_path = None
current_character_has_unsaved_changes = False

saved_character_files = []
filtered_saved_character_files = []
saved_character_index = -1
saved_character_folder = ""

# Saved table sorting state.
# These track which column is currently sorted and in what direction.
saved_character_sort_column = "name"
saved_character_sort_reverse = False

# Controls whether the Character Options panel is visible.
options_visible = True
left_torch_frames = []
right_torch_frames = []
torch_frame_index = 0
dice_roll_history = []
last_dice_roll_text = ""

APP_SETTINGS_FILE = "dragon_scrolls_settings.json"
LAST_CHARACTER_FOLDER_KEY = "last_character_folder"

# ============================================================
# GUI CHARACTER DISPLAY / REROLL HELPERS
# These functions update the visible character tabs and handle
# rerolling a character while respecting the Keep checkboxes.
# ============================================================

def update_status_bar(message=None):
    if message is not None:
        status_text.set(message)
        return

    if current_character_data is None:
        status_text.set("No character loaded.")
        return

    character_name = current_character_data.get("name", "Unnamed Character")

    if current_character_file_path is None:
        status_text.set(f"Unsaved new character: {character_name}")
        return

    file_name = os.path.basename(current_character_file_path)

    if current_character_has_unsaved_changes:
        status_text.set(f"Unsaved changes: {character_name} | {file_name}")
    else:
        status_text.set(f"Saved character: {character_name} | {file_name}")

def mark_current_character_changed():
    global current_character_has_unsaved_changes

    if current_character_data is None:
        return

    current_character_has_unsaved_changes = True
    update_status_bar()

def display_character_data(character_data):
    summary_text = generate_summary_text(character_data)
    abilities_text = generate_abilities_text(character_data)
    skills_text = generate_skills_text(character_data)
    combat_text = generate_combat_text(character_data)
    equipment_text = generate_equipment_text(character_data)
    features_text = generate_features_text(character_data)
    roleplay_text = generate_roleplay_text(character_data)
    spells_text = generate_spells_text(character_data)
    spellbook_text = generate_spellbook_text(character_data)
    image_prompt_text = generate_image_prompt_text(character_data)

    sheet_identity_display.delete("1.0", tk.END)
    sheet_identity_display.insert(tk.END, summary_text)

    sheet_abilities_display.delete("1.0", tk.END)
    sheet_abilities_display.insert(tk.END, abilities_text)

    sheet_combat_display.delete("1.0", tk.END)
    sheet_combat_display.insert(tk.END, combat_text + "\n\n" + skills_text)

    sheet_roleplay_display.delete("1.0", tk.END)
    sheet_roleplay_display.insert(tk.END, roleplay_text)

    sheet_equipment_display.delete("1.0", tk.END)
    sheet_equipment_display.insert(tk.END, equipment_text)

    sheet_spells_display.delete("1.0", tk.END)
    sheet_spells_display.insert(tk.END, spells_text)

    sheet_features_display.delete("1.0", tk.END)
    sheet_features_display.insert(tk.END, features_text)

    summary_display.delete("1.0", tk.END)
    summary_display.insert(tk.END, summary_text)

    abilities_display.delete("1.0", tk.END)
    abilities_display.insert(tk.END, abilities_text)

    skills_display.delete("1.0", tk.END)
    skills_display.insert(tk.END, skills_text)

    combat_display.delete("1.0", tk.END)
    combat_display.insert(tk.END, combat_text)

    equipment_display.delete("1.0", tk.END)
    equipment_display.insert(tk.END, equipment_text)

    spells_display.delete("1.0", tk.END)
    spells_display.insert(tk.END, spells_text)
    spellbook_display.delete("1.0", tk.END)
    spellbook_display.insert(tk.END, spellbook_text)

    roleplay_display.delete("1.0", tk.END)
    roleplay_display.insert(tk.END, roleplay_text)

    features_display.delete("1.0", tk.END)
    features_display.insert(tk.END, features_text)

    image_prompt_display.delete("1.0", tk.END)
    image_prompt_display.insert(tk.END, image_prompt_text)

    name_entry.delete(0, tk.END)
    name_entry.insert(0, character_data["name"])

    level_choice.set(str(character_data.get("level", 1)))
    roll_method_choice.set(character_data.get("roll_method", "4d6 Drop Lowest"))

    update_subclass_options()
    update_status_bar()

    loaded_subclass = character_data.get("subclass", "Random")

    if loaded_subclass == "None":
        subclass_choice.set("Random")
    else:
        subclass_choice.set(loaded_subclass)

def reroll_character_data():
    if current_character_data is None:
        return generate_character_data(
            class_choice.get(),
            species_choice.get(),
            alignment_choice.get(),
            sex_choice.get(),
            background_choice.get(),
            level_choice.get(),
            roll_method_choice.get(),
            subclass_choice.get()
        )
    selected_class = class_choice.get()
    selected_species = species_choice.get()
    selected_alignment = alignment_choice.get()
    selected_sex = sex_choice.get()
    selected_background = background_choice.get()
    selected_level = level_choice.get()

    if keep_class_var.get():
        selected_class = current_character_data["class"]

    if keep_species_var.get():
        selected_species = current_character_data["species"]

    if keep_alignment_var.get():
        selected_alignment = current_character_data["alignment"]

    if keep_sex_var.get():
        selected_sex = current_character_data.get("sex", "Random")

    if keep_background_var.get():
        selected_background = current_character_data["background"]

    new_character_data = generate_character_data(
        selected_class,
        selected_species,
        selected_alignment,
        selected_sex,
        selected_background,
        selected_level,
        roll_method_choice.get(),
        subclass_choice.get()
    )
    if keep_name_var.get():
        new_character_data["name"] = current_character_data["name"]

    return new_character_data

# ============================================================
# CHARACTER CLEARING AND PORTRAIT IMAGE LOGIC
# These functions reset character displays, reset portrait state,
# load/paste/choose portrait images, resize portraits to fit the
# GUI frame, and open a larger portrait preview window.
# ============================================================
def reset_portrait_image():
    global current_portrait_image
    global current_portrait_photo

    current_portrait_image = None
    current_portrait_photo = None

    portrait_label.config(
        image="",
        text="Copy an image from ChatGPT,\nthen click 'Paste Portrait'."
    )

    portrait_label.image = None

def clear_character_displays():
    global current_character_data
    global current_character_file_path
    global current_character_has_unsaved_changes

    current_character_data = None
    current_character_file_path = None
    current_character_has_unsaved_changes = False
    name_entry.delete(0, tk.END)

    reset_portrait_image()

    starting_message = "Click 'Generate Character' to create your first GUI character.\n"

    sheet_identity_display.delete("1.0", tk.END)
    sheet_identity_display.insert(tk.END, starting_message)

    sheet_abilities_display.delete("1.0", tk.END)
    sheet_combat_display.delete("1.0", tk.END)
    sheet_roleplay_display.delete("1.0", tk.END)
    sheet_equipment_display.delete("1.0", tk.END)
    sheet_spells_display.delete("1.0", tk.END)
    sheet_features_display.delete("1.0", tk.END)

    summary_display.delete("1.0", tk.END)
    summary_display.insert(tk.END, starting_message)

    abilities_display.delete("1.0", tk.END)
    skills_display.delete("1.0", tk.END)
    combat_display.delete("1.0", tk.END)
    equipment_display.delete("1.0", tk.END)
    spells_display.delete("1.0", tk.END)
    spellbook_display.delete("1.0", tk.END)
    roleplay_display.delete("1.0", tk.END)
    features_display.delete("1.0", tk.END)

    image_prompt_display.delete("1.0", tk.END)
    image_prompt_display.insert(
        tk.END,
        "Generate a character, then click 'Copy Image Prompt'.\n"
    )

    notebook.select(sheet_tab)
    update_status_bar("Character cleared. No character loaded.")

def save_portrait_next_to_file(character_file_path):
    if current_portrait_image is None:
        return None

    portrait_file_path = get_portrait_file_path(character_file_path)

    return save_portrait_image_to_file(
        current_portrait_image,
        portrait_file_path
    )


def display_portrait_image(portrait_image):
    global current_portrait_image

    current_portrait_image = portrait_image.copy()
    resize_portrait_to_frame()

def resize_portrait_to_frame(event=None):
    global current_portrait_photo

    if current_portrait_image is None:
        return

    frame_width = portrait_label.winfo_width()
    frame_height = portrait_label.winfo_height()

    # If the widget has not finished drawing yet, use safe fallback dimensions.
    if frame_width <= 1:
        frame_width = 280

    if frame_height <= 1:
        frame_height = 400

    # Leave a little padding inside the frame.
    max_width = frame_width - 20
    max_height = frame_height - 20

    if max_width < 50:
        max_width = 50

    if max_height < 50:
        max_height = 50

    display_image = make_resized_portrait_copy(
        current_portrait_image,
        max_width,
        max_height
    )

    current_portrait_photo = ImageTk.PhotoImage(display_image)

    portrait_label.config(image=current_portrait_photo, text="")
    portrait_label.image = current_portrait_photo

def open_large_portrait_window(event=None):
    """
    Open a larger portrait preview window.

    The preview window also includes Previous / Next buttons so the
    user can browse saved characters visually, like a character gallery.

    Important:
    Previous / Next reuse the existing saved-character navigation logic.
    That means the main GUI and this large portrait window stay synced.
    """

    if current_portrait_image is None:
        messagebox.showwarning(
            "No Portrait",
            "Load, paste, or choose a portrait first."
        )
        return

    portrait_window = tk.Toplevel(window)
    portrait_window.title("Large Character Portrait")
    portrait_window.geometry("850x900")
    portrait_window.config(bg=COLOR_STONE_DARK)
    portrait_window.lift()
    portrait_window.focus_force()

    title_text_variable = tk.StringVar()

    def update_large_portrait_title():
        if current_character_data is None:
            title_text_variable.set("Character Portrait")
        else:
            title_text_variable.set(
                current_character_data["name"] + " - Character Portrait"
            )

    update_large_portrait_title()

    portrait_title_label = tk.Label(
        portrait_window,
        textvariable=title_text_variable,
        font=("Georgia", 18, "bold"),
        bg=COLOR_STONE_DARK,
        fg=COLOR_GOLD
    )
    portrait_title_label.pack(pady=10)

    large_portrait_label = tk.Label(
        portrait_window,
        bg=COLOR_STONE,
        relief=tk.SUNKEN,
        bd=4
    )
    large_portrait_label.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

    def resize_large_portrait(event=None):
        if current_portrait_image is None:
            large_portrait_label.config(
                image="",
                text="No portrait loaded.",
                fg=COLOR_TEXT_LIGHT,
                bg=COLOR_STONE
            )
            large_portrait_label.image = None
            return

        frame_width = large_portrait_label.winfo_width()
        frame_height = large_portrait_label.winfo_height()

        if frame_width <= 1:
            frame_width = 800

        if frame_height <= 1:
            frame_height = 780

        max_width = frame_width - 20
        max_height = frame_height - 20

        display_image = make_resized_portrait_copy(
            current_portrait_image,
            max_width,
            max_height
        )

        large_photo = ImageTk.PhotoImage(display_image)

        large_portrait_label.config(image=large_photo, text="")
        large_portrait_label.image = large_photo

    def refresh_large_portrait_window():
        update_large_portrait_title()
        resize_large_portrait()

    def large_previous_button_clicked():
        if len(filtered_saved_character_files) == 0:
            messagebox.showwarning(
                "No Saved Characters",
                "Load a saved character folder first."
            )
            return

        previous_character_button_clicked()
        refresh_large_portrait_window()

    def large_next_button_clicked():
        if len(filtered_saved_character_files) == 0:
            messagebox.showwarning(
                "No Saved Characters",
                "Load a saved character folder first."
            )
            return

        next_character_button_clicked()
        refresh_large_portrait_window()

    large_portrait_label.bind("<Configure>", resize_large_portrait)

    navigation_frame = tk.Frame(
        portrait_window,
        bg=COLOR_STONE_DARK
    )
    navigation_frame.pack(pady=8)

    previous_button = tk.Button(
        navigation_frame,
        text="< Previous",
        font=("Georgia", 11, "bold"),
        bg=COLOR_RED,
        fg=COLOR_TEXT_LIGHT,
        activebackground=COLOR_RED_DARK,
        activeforeground=COLOR_GOLD,
        command=large_previous_button_clicked
    )
    previous_button.pack(side=tk.LEFT, padx=6)

    next_button = tk.Button(
        navigation_frame,
        text="Next >",
        font=("Georgia", 11, "bold"),
        bg=COLOR_RED,
        fg=COLOR_TEXT_LIGHT,
        activebackground=COLOR_RED_DARK,
        activeforeground=COLOR_GOLD,
        command=large_next_button_clicked
    )
    next_button.pack(side=tk.LEFT, padx=6)

    close_button = tk.Button(
        navigation_frame,
        text="Close",
        font=("Georgia", 11, "bold"),
        bg=COLOR_RED,
        fg=COLOR_TEXT_LIGHT,
        activebackground=COLOR_RED_DARK,
        activeforeground=COLOR_GOLD,
        command=portrait_window.destroy
    )
    close_button.pack(side=tk.LEFT, padx=6)

    portrait_window.after(100, resize_large_portrait)

def load_portrait_if_it_exists(character_file_path):
    portrait_file_path = get_portrait_file_path(character_file_path)

    if not os.path.exists(portrait_file_path):
        return None

    loaded_image = load_portrait_image_from_file(portrait_file_path)
    display_portrait_image(loaded_image)

    return loaded_image

# ============================================================
# APP SETTINGS HELPERS
# These helpers remember small user preferences between runs,
# such as the last folder used for saving/loading characters.
# ============================================================

def load_app_settings():
    if not os.path.exists(APP_SETTINGS_FILE):
        return {}

    try:
        with open(APP_SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)

        return settings

    except Exception:
        return {}


def save_app_settings(settings):
    try:
        with open(APP_SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(settings, file, indent=4)

    except Exception:
        # Settings are helpful, but not mission-critical.
        # If saving settings fails, the main app should still work.
        pass


def get_last_character_folder():
    settings = load_app_settings()
    folder_path = settings.get(LAST_CHARACTER_FOLDER_KEY, "")

    if folder_path != "" and os.path.exists(folder_path):
        return folder_path

    return ""


def remember_last_character_folder(folder_path):
    if folder_path == "":
        return

    if not os.path.exists(folder_path):
        return

    settings = load_app_settings()
    settings[LAST_CHARACTER_FOLDER_KEY] = folder_path
    save_app_settings(settings)

# ============================================================
# FILE SAVE / LOAD HELPERS
# These functions manage the saved character bundle:
#
# TXT-...      readable text character sheet
# PDF-...      printable character sheet
# JSON-...     reloadable character data
# PNG-...      saved portrait image
#
# The helper functions keep all matching files connected.
# ============================================================
def get_saved_character_table_values(character_file_path):
    """
    Return one row of display values for the Saved Characters table.

    The first column is the friendly display name. The remaining columns
    come from the saved JSON/TXT character data when available.
    """
    display_name = get_saved_character_display_name(character_file_path)
    character_data = load_character_data_if_it_exists(character_file_path)

    if character_data is None:
        return (
            display_name,
            "",
            "",
            "",
            "",
            "",
            ""
        )

    return (
        character_data.get("name", display_name),
        character_data.get("class", ""),
        character_data.get("subclass", ""),
        character_data.get("species", ""),
        str(character_data.get("level", "")),
        character_data.get("background", ""),
        character_data.get("alignment", "")
    )

def get_saved_character_sort_value(character_file_path, column_name):
    """
    Return a sortable value for one saved-character table column.

    Text columns sort alphabetically.
    Level sorts numerically.
    """
    row_values = get_saved_character_table_values(character_file_path)

    column_index_map = {
        "name": 0,
        "class": 1,
        "subclass": 2,
        "species": 3,
        "level": 4,
        "background": 5,
        "alignment": 6
    }

    if column_name not in column_index_map:
        return ""

    value = row_values[column_index_map[column_name]]

    if column_name == "level":
        try:
            return int(value)
        except ValueError:
            return 0

    return str(value).lower()

def sort_filtered_saved_characters():
    """
    Sort the current filtered saved-character list.

    This keeps search and sorting working together:
    - search decides which characters are visible
    - sort decides what order those visible characters appear in
    """
    filtered_saved_character_files.sort(
        key=lambda file_path: get_saved_character_sort_value(
            file_path,
            saved_character_sort_column
        ),
        reverse=saved_character_sort_reverse
    )

def saved_character_column_heading_clicked(column_name):
    """
    Sort the Saved Characters table when the user clicks a column header.

    Clicking the same column repeatedly toggles ascending/descending.
    Clicking a new column starts ascending.
    """
    global saved_character_sort_column
    global saved_character_sort_reverse
    global saved_character_index

    if saved_character_sort_column == column_name:
        saved_character_sort_reverse = not saved_character_sort_reverse
    else:
        saved_character_sort_column = column_name
        saved_character_sort_reverse = False

    saved_character_index = 0
    refresh_saved_character_listbox()

def refresh_saved_character_listbox():
    """
    Refresh the Saved Characters table.

    If the search box is empty, every saved character is shown.
    If the search box has text, only matching characters are shown.

    The table shows columns so the user can see why a result matched:
    name, class, subclass, species, level, background, and alignment.
    """
    global filtered_saved_character_files
    global saved_character_index

    # Clear old table rows.
    for row_id in saved_character_tree.get_children():
        saved_character_tree.delete(row_id)

    search_text = saved_character_search_entry.get().strip().lower()

    if search_text == "":
        filtered_saved_character_files = list(saved_character_files)
    else:
        filtered_saved_character_files = []

        for file_path in saved_character_files:
            character_search_text = get_saved_character_search_text(file_path)

            if search_text in character_search_text:
                filtered_saved_character_files.append(file_path)

    sort_filtered_saved_characters()
    update_saved_character_table_headings()
    
    for index, file_path in enumerate(filtered_saved_character_files):
        row_values = get_saved_character_table_values(file_path)

        saved_character_tree.insert(
            "",
            tk.END,
            iid=str(index),
            values=row_values
        )

    if len(filtered_saved_character_files) == 0:
        saved_character_index = -1
        saved_character_count_label.config(
            text=f"0 of {len(saved_character_files)} saved characters shown"
        )
        return

    if saved_character_index < 0:
        saved_character_index = 0

    if saved_character_index >= len(filtered_saved_character_files):
        saved_character_index = len(filtered_saved_character_files) - 1

    saved_character_tree.selection_set(str(saved_character_index))
    saved_character_tree.see(str(saved_character_index))

    sort_direction_text = "descending" if saved_character_sort_reverse else "ascending"

    saved_character_count_label.config(
        text=(
            f"{len(filtered_saved_character_files)} of {len(saved_character_files)} shown | "
            f"Sorted by {saved_character_sort_column} {sort_direction_text}"
        )
    )

def save_character_data_next_to_file(character_file_path):
    if current_character_data is None:
        return None

    data_file_path = get_character_data_file_path(character_file_path)

    with open(data_file_path, "w", encoding="utf-8") as file:
        json.dump(current_character_data, file, indent=4)

    return data_file_path


def load_character_into_main_gui(character_data, character_file_path=None):
    global current_character_data
    global current_character_file_path
    global current_character_has_unsaved_changes

    current_character_data = character_data
    current_character_file_path = character_file_path
    current_character_has_unsaved_changes = False

    display_character_data(current_character_data)
    name_entry.delete(0, tk.END)
    name_entry.insert(0, current_character_data["name"])

    if character_file_path is not None:
        loaded_portrait = load_portrait_if_it_exists(character_file_path)

        if loaded_portrait is None:
            reset_portrait_image()
    else:
        reset_portrait_image()

    notebook.select(sheet_tab)
    update_status_bar()

def load_saved_character_by_index(index):
    """
    Load a saved character by index from the currently filtered list.

    If no search is active, the filtered list is the full saved list.
    If search is active, Previous / Next move through only the matches.
    """
    global saved_character_index

    if len(filtered_saved_character_files) == 0:
        messagebox.showwarning(
            "No Saved Characters",
            "No saved characters match the current search."
        )
        return

    # Wrap around when moving before first or after last.
    if index < 0:
        index = len(filtered_saved_character_files) - 1

    if index >= len(filtered_saved_character_files):
        index = 0

    saved_character_index = index
    file_path = filtered_saved_character_files[saved_character_index]

    loaded_character_data = load_character_data_from_file(file_path)

    if loaded_character_data is None:
        messagebox.showwarning(
            "Cannot Load Character",
            "This saved character could not be loaded."
        )
        return

    load_character_into_main_gui(loaded_character_data, file_path)
    refresh_saved_character_listbox()
    

# ============================================================
# GUI STYLE HELPERS
# These functions create reusable GUI pieces and apply the
# fantasy theme to buttons, labels, text boxes, cards, and panels.
# ============================================================

def create_grimoire_frame(parent):
    outer_frame = tk.Frame(
        parent,
        bg=COLOR_GRIMOIRE_BORDER,
        bd=0
    )

    inner_frame = tk.Frame(
        outer_frame,
        bg=COLOR_GRIMOIRE_INNER_BORDER,
        bd=0
    )

    page_frame = tk.Frame(
        inner_frame,
        bg=COLOR_GRIMOIRE_PAGE_DARK,
        bd=3,
        relief=tk.RIDGE
    )

    inner_frame.pack(padx=3, pady=3, fill=tk.BOTH, expand=True)
    page_frame.pack(padx=4, pady=4, fill=tk.BOTH, expand=True)

    return outer_frame, page_frame


def animate_torches():
    global torch_frame_index

    if len(left_torch_frames) == 0 or len(right_torch_frames) == 0:
        return

    left_frame = left_torch_frames[torch_frame_index]
    right_frame = right_torch_frames[torch_frame_index]

    top_panel_canvas.itemconfig(left_torch_item, image=left_frame)
    top_panel_canvas.itemconfig(right_torch_item, image=right_frame)

    torch_frame_index = (torch_frame_index + 1) % len(left_torch_frames)

    window.after(180, animate_torches)


def apply_theme():
    window.config(bg=COLOR_STONE_DARK)

    # --------------------------------------------------------
    # Notebook tab styling
    # ttk.Notebook tabs do not use normal tk widget colors,
    # so they must be themed with ttk.Style.
    # --------------------------------------------------------
    notebook_style = ttk.Style()
    notebook_style.theme_use("clam")

    notebook_style.configure(
        "Dungeon.TNotebook",
        background=COLOR_STONE_DARK,
        borderwidth=0,
        tabmargins=[6, 6, 6, 0]
    )

    notebook_style.configure(
        "Dungeon.TNotebook.Tab",
        background=COLOR_TAB_BG,
        foreground=COLOR_TAB_TEXT,
        font=NOTEBOOK_TAB_FONT,
        padding=[7, 5],
        borderwidth=2,
        relief="raised"
    )

    notebook_style.map(
        "Dungeon.TNotebook.Tab",
        background=[
            ("selected", COLOR_TAB_SELECTED),
            ("active", COLOR_TAB_ACTIVE)
        ],
        foreground=[
            ("selected", COLOR_TAB_SELECTED_TEXT),
            ("active", COLOR_GOLD)
        ],
        expand=[
            ("selected", [1, 1, 1, 0])
        ]
    )

    notebook.configure(style="Dungeon.TNotebook")

    top_panel_canvas.config(
        bg=PIXEL_MORTAR_COLOR,
        highlightthickness=0,
        bd=0
    )

    top_panel_canvas.itemconfig(
        title_shadow_item,
        fill=PIXEL_TITLE_SHADOW,
        font=TITLE_FONT
    )

    top_panel_canvas.itemconfig(
        title_text_item,
        fill=COLOR_GOLD,
        font=TITLE_FONT
    )
    
    notebook_outer_frame.config(bg=COLOR_GOLD)
    notebook_middle_frame.config(bg=COLOR_RED_DARK)
    notebook_inner_frame.config(
        bg=COLOR_PARCHMENT_SHADOW,
        highlightthickness=2,
        highlightbackground=COLOR_PARCHMENT_EDGE,
        highlightcolor=COLOR_PARCHMENT_EDGE
    )
    
    controls_frame.config(bg=COLOR_STONE_DARK)
    controls_row_1.config(bg=COLOR_STONE_DARK)
    controls_row_2.config(bg=COLOR_STONE_DARK)

    status_bar.config(
        bg=COLOR_STONE,
        fg=COLOR_TEXT_LIGHT,
        font=("Consolas", 9),
        anchor=tk.W,
        relief=tk.SUNKEN,
        bd=1
    )

    main_actions_frame.config(bg=COLOR_STONE_DARK, fg=COLOR_GOLD)
    reroll_actions_frame.config(bg=COLOR_STONE_DARK, fg=COLOR_GOLD)
    saved_actions_frame.config(bg=COLOR_STONE_DARK, fg=COLOR_GOLD)
    portrait_actions_frame.config(bg=COLOR_STONE_DARK, fg=COLOR_GOLD)
    options_frame.config(bg=COLOR_STONE_DARK, fg=COLOR_GOLD)

    name_frame.config(bg=COLOR_STONE_DARK)
    choice_frame.config(bg=COLOR_STONE_DARK)
    choice_row_1.config(bg=COLOR_STONE_DARK)
    choice_row_2.config(bg=COLOR_STONE_DARK)
    surgical_edit_frame.config(bg=COLOR_STONE_DARK)
    keep_frame.config(bg=COLOR_STONE_DARK)

    sheet_container.config(bg=COLOR_PARCHMENT_MID)
    sheet_top_row.config(bg=COLOR_PARCHMENT_MID)
    sheet_bottom_row.config(bg=COLOR_PARCHMENT_MID)
    portrait_frame.config(
        bg=COLOR_PARCHMENT_SHADOW,
        highlightthickness=2,
        highlightbackground=COLOR_PARCHMENT_EDGE,
        highlightcolor=COLOR_PARCHMENT_EDGE
    )

    portrait_title.config(
        bg=COLOR_PARCHMENT_SHADOW,
        fg=COLOR_GOLD
    )
    portrait_label.config(
        bg=COLOR_PARCHMENT_LIGHT,
        fg=COLOR_INK,
        bd=0,
        relief=tk.FLAT,
        highlightthickness=2,
        highlightbackground=COLOR_PARCHMENT_EDGE,
        highlightcolor=COLOR_PARCHMENT_EDGE
    )

    saved_characters_frame.config(bg=COLOR_STONE_DARK)
    saved_search_frame.config(bg=COLOR_STONE_DARK)
    saved_characters_label.config(bg=COLOR_STONE_DARK, fg=COLOR_GOLD)
    saved_characters_help.config(bg=COLOR_STONE_DARK, fg=COLOR_TEXT_LIGHT)

    saved_tree_style = ttk.Style()

    saved_tree_style.configure(
        "Dungeon.Treeview",
        background=COLOR_PARCHMENT_LIGHT,
        foreground=COLOR_INK,
        fieldbackground=COLOR_PARCHMENT_LIGHT,
        rowheight=28,
        font=("Consolas", 10),
        borderwidth=0
    )

    saved_tree_style.configure(
        "Dungeon.Treeview.Heading",
        background=COLOR_RED_DARK,
        foreground=COLOR_GOLD,
        font=("Georgia", 10, "bold"),
        relief=tk.RAISED,
        borderwidth=2
    )

    saved_tree_style.map(
        "Dungeon.Treeview",
        background=[
            ("selected", COLOR_RED)
        ],
        foreground=[
            ("selected", COLOR_TEXT_LIGHT)
        ]
    )
    
    saved_character_search_entry.config(
        bg=COLOR_PARCHMENT_LIGHT,
        fg=COLOR_INK,
        insertbackground=COLOR_INK,
        relief=tk.FLAT,
        bd=0,
        font=("Consolas", 11),
        highlightthickness=2,
        highlightbackground=COLOR_PARCHMENT_EDGE,
        highlightcolor=COLOR_PARCHMENT_EDGE
    )    

    labels = [
        name_label,
        class_label,
        subclass_label,
        species_label,
        alignment_label,
        sex_label,
        background_label,
        level_label,
        roll_method_label,
        saved_character_search_label,
        saved_character_count_label
    ]

    for label in labels:
        style_label(label)

    buttons = [
        generate_button,
        reroll_name_button,
        reroll_stats_button,
        reroll_roleplay_button,
        save_button,
        save_as_new_button,
        print_button,
        dice_roller_button,
        view_saved_button,
        previous_character_button,
        next_character_button,
        delete_character_button,
        copy_prompt_button,
        paste_portrait_button,
        choose_portrait_button,
        image_prompt_button,
        toggle_options_button,
        apply_selected_options_button,
        apply_identity_only_button,
        apply_level_only_button,
        apply_subclass_only_button,
        apply_name_button,
        clear_saved_character_search_button,
        refresh_saved_characters_button,
        roll_method_help_button
    ]

    for button in buttons:
        style_button(button)
        
    name_entry.config(
        bg=COLOR_PARCHMENT_LIGHT,
        fg=COLOR_INK,
        insertbackground=COLOR_INK,
        relief=tk.FLAT,
        bd=0,
        font=("Georgia", 11),
        highlightthickness=2,
        highlightbackground=COLOR_PARCHMENT_EDGE,
        highlightcolor=COLOR_PARCHMENT_EDGE
    )
    checkboxes = [
        keep_name_checkbox,
        keep_class_checkbox,
        keep_species_checkbox,
        keep_alignment_checkbox,
        keep_sex_checkbox,
        keep_background_checkbox
    ]

    for checkbox in checkboxes:
        checkbox.config(
            bg=COLOR_STONE_DARK,
            fg=COLOR_TEXT_LIGHT,
            activebackground=COLOR_STONE_DARK,
            activeforeground=COLOR_GOLD,
            selectcolor=COLOR_STONE,
            font=("Georgia", 10, "bold")
        )

    tab_frames = [
        sheet_tab,
        summary_tab,
        abilities_tab,
        skills_tab,
        combat_tab,
        equipment_tab,
        spells_tab,
        spellbook_tab,
        roleplay_tab,
        features_tab,
        image_prompt_tab,
        saved_characters_tab
    ]

    for tab_frame in tab_frames:
        tab_frame.config(bg=COLOR_PARCHMENT_MID)
    
    text_boxes = [
        sheet_identity_display,
        sheet_abilities_display,
        sheet_combat_display,
        sheet_roleplay_display,
        sheet_equipment_display,
        sheet_spells_display,
        sheet_features_display,
        summary_display,
        abilities_display,
        skills_display,
        combat_display,
        equipment_display,
        spells_display,
        spellbook_display,
        roleplay_display,
        features_display,
        image_prompt_display
    ]

    for text_box in text_boxes:
        style_text_box(text_box)

# ============================================================
# DICE ROLLER HELPERS
# These functions power the simple dice roller popup window.
# Later sprints can replace or enhance this with animated dice.
# ============================================================

def get_natural_d20_note(roll_value):
    """
    Return a special D&D note for natural d20 rolls.

    This looks only at the die face itself, not the final total
    after modifiers.
    """
    if roll_value == 20:
        return "Natural 20! Critical success energy.\n"

    if roll_value == 1:
        return "Natural 1! Critical failure energy.\n"

    return ""

def roll_dice_expression(dice_expression):
    """
    Roll a dice expression and return readable result text.

    Supported examples:
    - 1d20
    - d20
    - 1d20+5
    - 2d8+3
    - 8d6
    - 2d6+1d4+3
    - 2d6+1d4-2
    - 4d6 Drop Lowest
    - 1d20 Advantage
    - 1d20 Disadvantage
    - 1d20 Advantage+5
    - 1d20 Disadvantage-2

    Limits:
    - Up to 100 dice total
    - Die size up to d1000
    """

    original_expression = dice_expression.strip()

    if original_expression == "":
        return "Enter or choose a dice expression first.\n"

    normalized_expression = original_expression.lower().replace(" ", "")

    # --------------------------------------------------------
    # Special case: D&D ability score roll
    # --------------------------------------------------------
    if normalized_expression == "4d6droplowest":
        rolls = []

        for i in range(4):
            rolls.append(random.randint(1, 6))

        dropped_roll = min(rolls)
        kept_rolls = list(rolls)
        kept_rolls.remove(dropped_roll)

        total = sum(kept_rolls)

        return (
            "Roll: 4d6 Drop Lowest\n"
            f"All dice: {rolls}\n"
            f"Dropped: {dropped_roll}\n"
            f"Kept: {kept_rolls}\n"
            f"Final Total: {total}\n"
        )

    # --------------------------------------------------------
    # Special cases: D&D advantage/disadvantage.
    #
    # These support optional modifiers:
    # - 1d20 Advantage+5
    # - 1d20 Disadvantage-2
    # --------------------------------------------------------
    if normalized_expression.startswith("1d20advantage"):
        modifier_text = normalized_expression.replace("1d20advantage", "")
        modifier = 0

        if modifier_text != "":
            try:
                modifier = int(modifier_text)
            except ValueError:
                return "Invalid advantage modifier. Use something like 1d20 Advantage+5.\n"

        rolls = [
            random.randint(1, 20),
            random.randint(1, 20)
        ]

        kept_roll = max(rolls)
        final_total = kept_roll + modifier
        natural_note = get_natural_d20_note(kept_roll)

        result_text = ""
        result_text += "Roll: 1d20 Advantage\n"
        result_text += f"Dice: {rolls}\n"
        result_text += f"Kept Higher Roll: {kept_roll}\n"

        if natural_note != "":
            result_text += natural_note

        if modifier != 0:
            result_text += f"Modifier: {modifier:+d}\n"

        result_text += f"Final Total: {final_total}\n"

        return result_text

    if normalized_expression.startswith("1d20disadvantage"):
        modifier_text = normalized_expression.replace("1d20disadvantage", "")
        modifier = 0

        if modifier_text != "":
            try:
                modifier = int(modifier_text)
            except ValueError:
                return "Invalid disadvantage modifier. Use something like 1d20 Disadvantage-2.\n"

        rolls = [
            random.randint(1, 20),
            random.randint(1, 20)
        ]

        kept_roll = min(rolls)
        final_total = kept_roll + modifier
        natural_note = get_natural_d20_note(kept_roll)

        result_text = ""
        result_text += "Roll: 1d20 Disadvantage\n"
        result_text += f"Dice: {rolls}\n"
        result_text += f"Kept Lower Roll: {kept_roll}\n"

        if natural_note != "":
            result_text += natural_note

        if modifier != 0:
            result_text += f"Modifier: {modifier:+d}\n"

        result_text += f"Final Total: {final_total}\n"

        return result_text

    # --------------------------------------------------------
    # General dice expression parser.
    #
    # This supports chains like:
    # - 2d6+1d4+3
    # - 2d6+1d4-2
    # - d20+5
    #
    # Pattern meaning:
    #   optional sign: + or -
    #   then either:
    #       dice term like 2d6, d20, 8d6
    #       or flat number like 3
    # --------------------------------------------------------
    token_pattern = re.compile(r"([+-]?)(\d*d\d+|\d+)")

    position = 0
    total = 0
    total_dice_count = 0
    result_lines = []

    while position < len(normalized_expression):
        match = token_pattern.match(normalized_expression, position)

        if match is None:
            return (
                "Invalid dice expression.\n"
                "Use examples like 1d20, 1d20+5, 2d6+1d4+3, or 8d6.\n"
            )

        sign_text = match.group(1)
        token_text = match.group(2)

        sign = -1 if sign_text == "-" else 1

        if "d" in token_text:
            dice_parts = token_text.split("d")

            dice_count_text = dice_parts[0]
            die_size_text = dice_parts[1]

            # Allow d20 as shorthand for 1d20.
            if dice_count_text == "":
                number_of_dice = 1
            else:
                number_of_dice = int(dice_count_text)

            die_size = int(die_size_text)

            if number_of_dice <= 0 or die_size <= 0:
                return "Dice count and die size must be positive.\n"

            total_dice_count += number_of_dice

            if total_dice_count > 100:
                return "Too many dice. Please roll 100 dice or fewer.\n"

            if die_size > 1000:
                return "Die size too large. Please use d1000 or smaller.\n"

            rolls = []

            for i in range(number_of_dice):
                rolls.append(random.randint(1, die_size))

            dice_total = sum(rolls)
            signed_dice_total = sign * dice_total
            total += signed_dice_total

            natural_note = ""

            if number_of_dice == 1 and die_size == 20:
                natural_note = get_natural_d20_note(rolls[0])

            if sign == -1:
                result_lines.append(
                    f"-{token_text}: {rolls} = -{dice_total}"
                )
            else:
                result_lines.append(
                    f"{token_text}: {rolls} = {dice_total}"
                )

            if natural_note != "":
                result_lines.append(natural_note.strip())

        else:
            modifier = sign * int(token_text)
            total += modifier

            result_lines.append(f"Modifier: {modifier:+d}")

        position = match.end()

    result_text = ""
    result_text += f"Roll: {original_expression}\n"

    for line in result_lines:
        result_text += line + "\n"

    result_text += f"Final Total: {total}\n"

    return result_text

def open_dice_roller_window():
    """
    Open the Dragon Scrolls dice roller popup window.

    Current dice roller features:
    - Preset dice expressions from a dropdown.
    - Custom typed dice expressions, such as:
        1d20+5
        2d6+1d4+3
        8d6
        1d20 Advantage+5
    - Quick-roll buttons for common D&D rolls.
    - Roll history during the current app session.
    - Copy Latest button for copying the most recent roll.
    - Copy History button for copying the full visible dice log.
    - Clear button for clearing the visible roll history.

    Important design note:
    The small helper functions are nested inside this function because
    they need direct access to this specific popup window's widgets:
    dice_choice and result_display.
    """

    # ------------------------------------------------------------
    # Create popup window
    # ------------------------------------------------------------
    dice_window = tk.Toplevel(window)
    dice_window.title("Dice Roller")
    dice_window.geometry("660x520")
    dice_window.config(bg=COLOR_STONE_DARK)
    dice_window.lift()
    dice_window.focus_force()

    # ------------------------------------------------------------
    # Title
    # ------------------------------------------------------------
    title_label = tk.Label(
        dice_window,
        text="Dragon Scrolls Dice Roller",
        font=("Georgia", 18, "bold"),
        bg=COLOR_STONE_DARK,
        fg=COLOR_GOLD
    )
    title_label.pack(pady=10)

    # ------------------------------------------------------------
    # Dice selection row
    # The combobox is state="normal" so the user can either choose
    # a preset or type a custom dice expression.
    # ------------------------------------------------------------
    controls_frame = tk.Frame(
        dice_window,
        bg=COLOR_STONE_DARK
    )
    controls_frame.pack(pady=8)

    dice_label = tk.Label(
        controls_frame,
        text="Dice:",
        font=LABEL_FONT,
        bg=COLOR_STONE_DARK,
        fg=COLOR_GOLD
    )
    dice_label.pack(side=tk.LEFT, padx=5)

    dice_options = [
        "1d4",
        "1d6",
        "1d8",
        "1d10",
        "1d12",
        "1d20",
        "1d20+5",
        "1d20 Advantage",
        "1d20 Advantage+5",
        "1d20 Disadvantage",
        "1d20 Disadvantage-2",
        "2d6",
        "2d6+1d4+3",
        "3d6",
        "4d6",
        "4d6 Drop Lowest",
        "8d6",
        "1d100"
    ]

    dice_choice = ttk.Combobox(
        controls_frame,
        values=dice_options,
        state="normal",
        width=26
    )
    dice_choice.set("1d20")
    dice_choice.pack(side=tk.LEFT, padx=5)

    custom_help_label = tk.Label(
        dice_window,
        text="Choose dice or type your own: 1d20+5, 2d6+1d4+3, 8d6, or 1d20 Advantage+5.",
        font=("Consolas", 9),
        bg=COLOR_STONE_DARK,
        fg=COLOR_TEXT_LIGHT
    )
    custom_help_label.pack(pady=(0, 5))

    # ------------------------------------------------------------
    # Result display
    # This is where roll history is shown.
    # ------------------------------------------------------------
    result_display = scrolledtext.ScrolledText(
        dice_window,
        wrap=tk.WORD,
        font=("Consolas", 12),
        height=12
    )
    result_display.pack(
        padx=15,
        pady=10,
        fill=tk.BOTH,
        expand=True
    )
    style_text_box(result_display)

    # ------------------------------------------------------------
    # Nested button handlers
    # ------------------------------------------------------------
    def roll_button_clicked():
        """
        Roll the selected or typed dice expression, append it to the
        visible history, and remember it as the latest copied roll.
        """
        global last_dice_roll_text

        dice_expression = dice_choice.get()
        result_text = roll_dice_expression(dice_expression)

        last_dice_roll_text = result_text
        dice_roll_history.append(result_text)

        result_display.insert(
            tk.END,
            f"Roll #{len(dice_roll_history)}\n{result_text}"
        )
        result_display.insert(tk.END, "-" * 36 + "\n")
        result_display.see(tk.END)


    def quick_roll_button_clicked(dice_expression):
        """
        Put a common dice expression into the dice box and roll it.

        This uses the same central roll logic as the normal Roll button.
        """
        dice_choice.set(dice_expression)
        roll_button_clicked()


    def clear_roll_history_button_clicked():
        """
        Clear the visible dice history and reset the latest roll.
        """
        global last_dice_roll_text

        result_display.delete("1.0", tk.END)
        dice_roll_history.clear()
        last_dice_roll_text = ""

        result_display.insert(
            tk.END,
            "Roll history cleared.\n"
            + "-" * 36 + "\n"
        )


    def copy_latest_roll_button_clicked():
        """
        Copy only the most recent roll result to the clipboard.
        """
        if last_dice_roll_text == "":
            messagebox.showwarning(
                "No Roll Yet",
                "Roll some dice before copying the latest result."
            )
            return

        window.clipboard_clear()
        window.clipboard_append(last_dice_roll_text)
        window.update()

        messagebox.showinfo(
            "Roll Copied",
            "The latest dice roll was copied to your clipboard."
        )


    def copy_full_history_button_clicked():
        """
        Copy the full visible dice history to the clipboard.

        This copies exactly what the user sees in the result box,
        including roll numbers and separators.
        """
        full_history_text = result_display.get("1.0", tk.END).strip()

        if full_history_text == "":
            messagebox.showwarning(
                "No Roll History",
                "There is no dice history to copy yet."
            )
            return

        window.clipboard_clear()
        window.clipboard_append(full_history_text)
        window.update()

        messagebox.showinfo(
            "History Copied",
            "The full dice roll history was copied to your clipboard."
        )

    # Pressing Enter while focused in the dice box rolls the dice.
    dice_choice.bind("<Return>", lambda event: roll_button_clicked())

    # ------------------------------------------------------------
    # Quick-roll buttons
    # These are shortcuts for common D&D rolls.
    #
    # Placement matters:
    # These are created after quick_roll_button_clicked() exists.
    # ------------------------------------------------------------
    quick_roll_frame = tk.Frame(
        dice_window,
        bg=COLOR_STONE_DARK
    )
    quick_roll_frame.pack(pady=(0, 5))

    def create_quick_roll_button(button_text, dice_expression):
        """
        Create one small quick-roll button.

        The button text is short for readability.
        The dice_expression is the actual expression sent to the roller.
        """
        quick_button = tk.Button(
            quick_roll_frame,
            text=button_text,
            font=("Georgia", 10, "bold"),
            command=lambda: quick_roll_button_clicked(dice_expression)
        )
        quick_button.pack(side=tk.LEFT, padx=3)
        style_button(quick_button)

    create_quick_roll_button("d20", "1d20")
    create_quick_roll_button("d20+5", "1d20+5")
    create_quick_roll_button("Adv", "1d20 Advantage")
    create_quick_roll_button("Adv+5", "1d20 Advantage+5")
    create_quick_roll_button("Dis", "1d20 Disadvantage")
    create_quick_roll_button("Dis-2", "1d20 Disadvantage-2")
    create_quick_roll_button("2d6", "2d6")
    create_quick_roll_button("1d8", "1d8")
    create_quick_roll_button("8d6", "8d6")
    create_quick_roll_button("Stats", "4d6 Drop Lowest")

    # ------------------------------------------------------------
    # Main button row
    # ------------------------------------------------------------
    button_frame = tk.Frame(
        dice_window,
        bg=COLOR_STONE_DARK
    )
    button_frame.pack(pady=8)

    roll_button = tk.Button(
        button_frame,
        text="Roll",
        font=("Georgia", 12, "bold"),
        command=roll_button_clicked
    )
    roll_button.pack(side=tk.LEFT, padx=6)
    style_button(roll_button)

    clear_button = tk.Button(
        button_frame,
        text="Clear",
        font=("Georgia", 12, "bold"),
        command=clear_roll_history_button_clicked
    )
    clear_button.pack(side=tk.LEFT, padx=6)
    style_button(clear_button)

    copy_latest_button = tk.Button(
        button_frame,
        text="Copy Latest",
        font=("Georgia", 12, "bold"),
        command=copy_latest_roll_button_clicked
    )
    copy_latest_button.pack(side=tk.LEFT, padx=6)
    style_button(copy_latest_button)

    copy_history_button = tk.Button(
        button_frame,
        text="Copy History",
        font=("Georgia", 12, "bold"),
        command=copy_full_history_button_clicked
    )
    copy_history_button.pack(side=tk.LEFT, padx=6)
    style_button(copy_history_button)

    close_button = tk.Button(
        button_frame,
        text="Close",
        font=("Georgia", 12, "bold"),
        command=dice_window.destroy
    )
    close_button.pack(side=tk.LEFT, padx=6)
    style_button(close_button)

    # ------------------------------------------------------------
    # Startup instructions
    # ------------------------------------------------------------
    result_display.insert(
        tk.END,
        "Choose dice or type your own expression, then click Roll.\n"
        "Examples: 1d20, d20+5, 2d8+3, 2d6+1d4+3, 8d6.\n"
        "D&D checks: use 1d20 Advantage+5 or 1d20 Disadvantage-2.\n"
        "Ability scores: use 4d6 Drop Lowest.\n"
        + "-" * 36 + "\n"
    )

    # Put the cursor in the dice box so the user can immediately type
    # a custom expression and press Enter.
    dice_choice.focus_set()

    # ------------------------------------------------------------
    # Quick-roll buttons
    # These are shortcuts for common D&D rolls.
    # ------------------------------------------------------------
    quick_roll_frame = tk.Frame(
        dice_window,
        bg=COLOR_STONE_DARK
    )
    quick_roll_frame.pack(pady=(0, 5))

def quick_roll_button_clicked(dice_expression):
    """
    Put a common dice expression into the dice box and roll it.
    """
    dice_choice.set(dice_expression)
    roll_button_clicked()

def create_quick_roll_button(button_text, dice_expression):
    """
    Create one small quick-roll button.
    """
    quick_button = tk.Button(
        quick_roll_frame,
        text=button_text,
        font=("Georgia", 10, "bold"),
        command=lambda: quick_roll_button_clicked(dice_expression)
    )
    quick_button.pack(side=tk.LEFT, padx=3)
    style_button(quick_button)

    create_quick_roll_button("d20", "1d20")
    create_quick_roll_button("d20+5", "1d20+5")
    create_quick_roll_button("Adv", "1d20 Advantage")
    create_quick_roll_button("Adv+5", "1d20 Advantage+5")
    create_quick_roll_button("Dis", "1d20 Disadvantage")
    create_quick_roll_button("2d6", "2d6")
    create_quick_roll_button("1d8", "1d8")
    create_quick_roll_button("8d6", "8d6")
    create_quick_roll_button("Stats", "4d6 Drop Lowest")    

    # ------------------------------------------------------------
    # Button row
    # ------------------------------------------------------------
    button_frame = tk.Frame(
        dice_window,
        bg=COLOR_STONE_DARK
    )
    button_frame.pack(pady=8)

    roll_button = tk.Button(
        button_frame,
        text="Roll",
        font=("Georgia", 12, "bold"),
        command=roll_button_clicked
    )
    roll_button.pack(side=tk.LEFT, padx=6)
    style_button(roll_button)

    clear_button = tk.Button(
        button_frame,
        text="Clear",
        font=("Georgia", 12, "bold"),
        command=clear_roll_history_button_clicked
    )
    clear_button.pack(side=tk.LEFT, padx=6)
    style_button(clear_button)

    copy_latest_button = tk.Button(
        button_frame,
        text="Copy Latest",
        font=("Georgia", 12, "bold"),
        command=copy_latest_roll_button_clicked
    )
    copy_latest_button.pack(side=tk.LEFT, padx=6)
    style_button(copy_latest_button)

    copy_history_button = tk.Button(
        button_frame,
        text="Copy History",
        font=("Georgia", 12, "bold"),
        command=copy_full_history_button_clicked
    )
    copy_history_button.pack(side=tk.LEFT, padx=6)
    style_button(copy_history_button)

    close_button = tk.Button(
        button_frame,
        text="Close",
        font=("Georgia", 12, "bold"),
        command=dice_window.destroy
    )
    close_button.pack(side=tk.LEFT, padx=6)
    style_button(close_button)

    # ------------------------------------------------------------
    # Startup instructions
    # ------------------------------------------------------------
    result_display.insert(
        tk.END,
        "Choose dice or type your own expression, then click Roll.\n"
        "Examples: 1d20, d20+5, 2d8+3, 2d6+1d4+3, 8d6.\n"
        "D&D checks: use 1d20 Advantage+5 or 1d20 Disadvantage-2.\n"
        "Ability scores: use 4d6 Drop Lowest.\n"
        + "-" * 36 + "\n"
    )

    # Put the cursor in the dice box so the user can immediately type
    # a custom expression and press Enter.
    dice_choice.focus_set()

# ============================================================
# MAIN GUI EVENT HANDLERS
# These functions respond to user button clicks:
# generate character, reroll name, apply custom name, load saved
# character, navigate previous/next, copy prompt, paste/choose
# portrait, show prompt, and toggle options.
# ============================================================

def ask_to_save_unsaved_changes_before_continuing():
    if not current_character_has_unsaved_changes:
        return True

    user_choice = messagebox.askyesnocancel(
        "Unsaved Changes",
        "You have unsaved changes.\n\n"
        "Do you want to save the current character before continuing?\n\n"
        "Yes = Save first\n"
        "No = Continue without saving\n"
        "Cancel = Stay here"
    )

    # User clicked Cancel or closed the dialog.
    if user_choice is None:
        return False

    # User clicked No.
    if user_choice is False:
        return True

    # User clicked Yes.
    save_character_bundle_button_clicked()

    # If the save worked, this flag should now be False.
    # If the user canceled the save dialog, it should still be True.
    if current_character_has_unsaved_changes:
        return False

    return True

def close_window_button_clicked():
    if current_character_has_unsaved_changes:
        should_close = messagebox.askyesno(
            "Unsaved Changes",
            "You have unsaved changes.\n\n"
            "If you close now, those changes may be lost.\n\n"
            "Close anyway?"
        )

        if not should_close:
            return

    window.destroy()

def generate_character_button_clicked():
    """
    Generate a new character using the current GUI options.

    If the current character has unsaved changes, the user is asked
    whether to save, discard, or cancel before the new character replaces it.
    """
    global current_character_data
    global current_character_file_path
    global current_character_has_unsaved_changes

    should_continue = ask_to_save_unsaved_changes_before_continuing()

    if not should_continue:
        return

    current_character_data = reroll_character_data()
    current_character_file_path = None
    current_character_has_unsaved_changes = True

    reset_portrait_image()
    display_character_data(current_character_data)
    update_status_bar()

def reroll_name_button_clicked():
    global current_character_data

    if current_character_data is None:
        current_character_data = generate_character_data(
            class_choice.get(),
            species_choice.get(),
            alignment_choice.get(),
            sex_choice.get(),
            background_choice.get(),
            level_choice.get(),
            roll_method_choice.get(),
            subclass_choice.get()
        )
    else:
        current_character_data["name"] = generate_fantasy_name(
            current_character_data["species"]
        )

    display_character_data(current_character_data)
    mark_current_character_changed()


def reroll_ability_scores_button_clicked():
    global current_character_data

    if current_character_data is None:
        messagebox.showwarning(
            "No Character",
            "Generate a character before rerolling ability scores."
        )
        return

    current_character_data = reroll_ability_scores_for_character(
        current_character_data,
        roll_method_choice.get()
    )

    display_character_data(current_character_data)
    mark_current_character_changed()


def reroll_roleplay_traits_button_clicked():
    global current_character_data

    if current_character_data is None:
        messagebox.showwarning(
            "No Character",
            "Generate a character before rerolling roleplay traits."
        )
        return

    current_character_data = reroll_roleplay_traits_for_character(
        current_character_data
    )

    display_character_data(current_character_data)
    mark_current_character_changed()

def apply_custom_name_button_clicked():
    global current_character_data

    custom_name = name_entry.get().strip()

    if custom_name == "":
        messagebox.showwarning(
            "No Name Entered",
            "Type a character name before clicking Apply Name."
        )
        return

    if current_character_data is None:
        current_character_data = generate_character_data(
            class_choice.get(),
            species_choice.get(),
            alignment_choice.get(),
            sex_choice.get(),
            background_choice.get(),
            level_choice.get(),
            roll_method_choice.get(),
            subclass_choice.get()
        )

    current_character_data["name"] = custom_name

    display_character_data(current_character_data)
    mark_current_character_changed()

    messagebox.showinfo(
        "Name Updated",
        f"Character name changed to {custom_name}."
    )

def apply_selected_options_button_clicked():
    """
    Apply the current dropdown selections to the loaded/generated character.

    This is intended for editing an existing character after loading it.
    It keeps the current name and portrait, but rebuilds the character's
    mechanics and roleplay from the selected options:
    - class
    - subclass
    - species
    - alignment
    - sex
    - background
    - level
    - roll method

    The user still needs to click Save afterward to write the changes
    back to TXT, JSON, PDF, and portrait files.
    """
    global current_character_data

    if current_character_data is None:
        messagebox.showwarning(
            "No Character",
            "Load or generate a character before applying selected options."
        )
        return

    old_name = current_character_data["name"]

    updated_character_data = generate_character_data(
        class_choice.get(),
        species_choice.get(),
        alignment_choice.get(),
        sex_choice.get(),
        background_choice.get(),
        level_choice.get(),
        roll_method_choice.get(),
        subclass_choice.get()
    )

    # Keep the name the user already has unless they deliberately
    # change it with Apply Name or Reroll Name.
    updated_character_data["name"] = old_name

    current_character_data = updated_character_data

    display_character_data(current_character_data)
    mark_current_character_changed()

def apply_identity_only_button_clicked():
    """
    Apply only identity/roleplay dropdown fields.

    This does NOT reroll ability scores.
    This does NOT change class mechanics.
    This does NOT change equipment or spells.

    It only updates:
    - species
    - alignment
    - sex
    - background

    Note:
    Species normally affects ability bonuses and speed. This surgical edit
    intentionally does not recalculate those mechanics. It is for editing
    the character description/identity without rebuilding the sheet.
    """
    global current_character_data

    if current_character_data is None:
        messagebox.showwarning(
            "No Character",
            "Load or generate a character before editing identity."
        )
        return

    current_character_data["species"] = species_choice.get()
    current_character_data["alignment"] = alignment_choice.get()
    current_character_data["sex"] = sex_choice.get()
    current_character_data["background"] = background_choice.get()

    display_character_data(current_character_data)
    mark_current_character_changed()


def apply_level_only_button_clicked():
    """
    Apply only the selected level.

    This keeps the same character, ability scores, class, species,
    background, roleplay, and portrait, but recalculates level-dependent
    mechanics like proficiency bonus, hit points, spells, and features.
    """
    global current_character_data

    if current_character_data is None:
        messagebox.showwarning(
            "No Character",
            "Load or generate a character before editing level."
        )
        return

    selected_level_text = level_choice.get()

    if not selected_level_text.isdigit():
        messagebox.showwarning(
            "Invalid Level",
            "Choose a valid level before applying level."
        )
        return

    current_character_data["level"] = int(selected_level_text)
    current_character_data = recalculate_character_after_level_change(
        current_character_data
    )

    display_character_data(current_character_data)
    mark_current_character_changed()


def apply_subclass_only_button_clicked():
    """
    Apply only the selected subclass.

    This keeps the same class and level. If the character is too low-level
    for a subclass, the generator will set subclass to None.
    """
    global current_character_data

    if current_character_data is None:
        messagebox.showwarning(
            "No Character",
            "Load or generate a character before editing subclass."
        )
        return

    character_class = current_character_data["class"]
    character_level = current_character_data["level"]
    selected_subclass = subclass_choice.get()

    current_character_data["subclass"] = generate_subclass(
        character_class,
        character_level,
        selected_subclass
    )
    current_character_data["subclass_features"] = generate_subclass_features(
        current_character_data.get("subclass", "None"),
        character_level
    )

    display_character_data(current_character_data)
    mark_current_character_changed()

def update_subclass_options(event=None):
    selected_class = class_choice.get()

    if selected_class in class_subclasses:
        subclass_values = ["Random"] + class_subclasses[selected_class]
    else:
        subclass_values = ["Random"]

    subclass_choice.config(values=subclass_values)

    if subclass_choice.get() not in subclass_values:
        subclass_choice.set("Random")

# ============================================================
# SAVE / PRINT / DELETE EVENT HANDLERS
# These button-click functions save character bundles, print PDFs,
# delete saved character bundles, and protect against accidental
# permanent deletion.
# ============================================================
def save_character_bundle_button_clicked():
    """
    Save the current character bundle.

    A character bundle includes:
    - TXT readable character sheet
    - JSON editable character data
    - PDF printable character sheet
    - PNG portrait image, if one exists

    If the character has never been saved before, the user chooses
    a PDF filename. The helper functions then derive the matching
    TXT, JSON, and PNG paths from that same core filename.
    """
    global current_character_file_path
    global current_character_has_unsaved_changes

    if current_character_data is None:
        messagebox.showwarning(
            "No Character",
            "Generate or load a character before saving."
        )
        return

    if current_character_file_path is None:
        character_name = current_character_data["name"]
        suggested_file_name = "PDF-" + character_name + "_character.pdf"
        initial_folder = get_last_character_folder()

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialdir=initial_folder,
            initialfile=suggested_file_name,
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )

        if file_path == "":
            return

        remember_last_character_folder(os.path.dirname(file_path))
        current_character_file_path = file_path

    else:
        file_path = current_character_file_path

    bundle_paths = get_character_bundle_paths(file_path)

    txt_path = bundle_paths["txt"]
    pdf_path = bundle_paths["pdf"]
    json_path = bundle_paths["json"]
    portrait_path = bundle_paths["portrait"]

    full_character_text = generate_full_character_text(current_character_data)

    # Save readable TXT sheet.
    with open(txt_path, "w", encoding="utf-8") as file:
        file.write(full_character_text)

    # Save editable JSON data.
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(current_character_data, file, indent=4)

    # Save portrait image only if one is loaded.
    if current_portrait_image is not None:
        image_to_save = current_portrait_image.copy()
        image_to_save.save(portrait_path, "PNG")

    # Always build the PDF, even if there is no portrait.
    build_character_sheet_pdf(
        pdf_path,
        current_character_data,
        current_portrait_image
    )

    current_character_has_unsaved_changes = False
    update_status_bar()

    if saved_character_folder != "":
        saved_character_files.clear()
        saved_character_files.extend(find_saved_character_files(saved_character_folder))

        filtered_saved_character_files.clear()
        filtered_saved_character_files.extend(saved_character_files)

        refresh_saved_character_listbox()

    if current_portrait_image is None:
        messagebox.showinfo(
            "Character Saved",
            "Saved TXT, PDF, and JSON files. No portrait image was saved because no portrait is loaded."
        )
    else:
        messagebox.showinfo(
            "Character Saved",
            "Saved TXT, PDF, JSON, and portrait image files."
        )

def save_as_new_character_button_clicked():
    """
    Save the current character as a new bundle.

    This intentionally clears the current file path first, so the normal
    save function prompts for a new filename and then saves TXT, JSON,
    PDF, and optional PNG files together.
    """
    global current_character_file_path

    if current_character_data is None:
        messagebox.showwarning(
            "No Character",
            "Generate or load a character before saving as new."
        )
        return

    # Force the normal save function to ask for a new file path.
    current_character_file_path = None
    save_character_bundle_button_clicked()

def print_current_character_pdf():
    if current_character_data is None:
        messagebox.showwarning(
            "No Character",
            "Generate or load a character before printing."
        )
        return

    if current_character_file_path is None:
        messagebox.showwarning(
            "Character Not Saved",
            "Save the character before printing so a PDF file can be created."
        )
        return

    bundle_paths = get_character_bundle_paths(current_character_file_path)
    pdf_path = bundle_paths["pdf"]

    build_character_sheet_pdf(
        pdf_path,
        current_character_data,
        current_portrait_image
    )

    if not os.path.exists(pdf_path):
        messagebox.showwarning(
            "PDF Not Found",
            "No PDF was found for this character. Click Save Character first."
        )
        return

    try:
        os.startfile(pdf_path, "print")
    except Exception as error:
        messagebox.showerror(
            "Print Failed",
            f"The program could not send the PDF to the printer.\n\n{error}"
        )

def delete_character_button_clicked():
    global current_character_data
    global current_character_file_path

    if current_character_file_path is None:
        messagebox.showwarning(
            "No Saved Character Selected",
            "Load a saved character before trying to delete it."
        )
        return

    character_name = "this character"

    if current_character_data is not None:
        character_name = current_character_data["name"]

    first_confirm = messagebox.askyesno(
        "Permanently Delete Character?",
        f"Are you sure you want to permanently delete {character_name}?\n\n"
        "This will delete all associated TXT, PDF, JSON, and portrait image files.\n\n"
        "This cannot be undone."
    )

    if not first_confirm:
        return

    confirmation_window = tk.Toplevel(window)
    confirmation_window.title("Confirm Permanent Delete")
    confirmation_window.geometry("450x220")
    confirmation_window.grab_set()

    warning_label = tk.Label(
        confirmation_window,
        text=(
            f"To permanently delete {character_name}, type DELETE below.\n\n"
            "This will remove the character sheet, PDF, JSON data,\n"
            "and portrait image files."
        ),
        font=("Arial", 11),
        justify=tk.CENTER
    )
    warning_label.pack(pady=15)

    delete_entry = tk.Entry(
        confirmation_window,
        font=("Arial", 12),
        width=20,
        justify=tk.CENTER
    )
    delete_entry.pack(pady=5)
    delete_entry.focus()

    def final_delete_confirmed():
        typed_text = delete_entry.get()

        if typed_text != "DELETE":
            messagebox.showwarning(
                "Delete Cancelled",
                "You must type DELETE exactly to permanently delete this character."
            )
            return

        deleted_files = delete_character_bundle(current_character_file_path)

        confirmation_window.destroy()
        clear_character_displays()

        if saved_character_folder != "":
            saved_character_files.clear()
            saved_character_files.extend(find_saved_character_files(saved_character_folder))
            filtered_saved_character_files.clear()
            filtered_saved_character_files.extend(saved_character_files)

        refresh_saved_character_listbox()

        if len(deleted_files) == 0:
            messagebox.showinfo(
                "No Files Deleted",
                "No matching character files were found to delete."
            )
        else:
            messagebox.showinfo(
                "Character Deleted",
                f"Deleted {len(deleted_files)} associated character file(s)."
            )

    def cancel_delete():
        confirmation_window.destroy()

    button_frame = tk.Frame(confirmation_window)
    button_frame.pack(pady=15)

    confirm_button = tk.Button(
        button_frame,
        text="Permanently Delete",
        font=("Arial", 11),
        command=final_delete_confirmed
    )
    confirm_button.pack(side=tk.LEFT, padx=5)

    cancel_button = tk.Button(
        button_frame,
        text="Cancel",
        font=("Arial", 11),
        command=cancel_delete
    )
    cancel_button.pack(side=tk.LEFT, padx=5)    

def view_saved_character_button_clicked():
    """
    Let the user choose a saved character file, load that character,
    and populate the Saved tab with all saved characters in the same folder.

    The user may select a JSON, TXT, PDF, or PNG file. The file_manager
    helpers resolve that selection back to the matching editable JSON/TXT
    character data when possible.
    """
    global saved_character_files
    global saved_character_index
    global saved_character_folder

    initial_folder = get_last_character_folder()

    file_path = filedialog.askopenfilename(
        initialdir=initial_folder,
        filetypes=[
            ("Character Files", "*.json *.txt *.pdf *.png"),
            ("Character Data Files", "*.json"),
            ("Text Files", "*.txt"),
            ("PDF Files", "*.pdf"),
            ("Portrait Images", "*.png"),
            ("All Files", "*.*")
        ]
    )

    if file_path == "":
        return

    loaded_character_data = load_character_data_from_file(file_path)

    if loaded_character_data is None:
        messagebox.showwarning(
            "Cannot Load Character",
            "No editable character data could be loaded from this file. Try selecting the matching TXT or JSON file."
        )
        return

    folder_path = os.path.dirname(file_path)

    remember_last_character_folder(folder_path)

    saved_character_folder = folder_path
    saved_character_files = find_saved_character_files(saved_character_folder)
    filtered_saved_character_files.clear()
    filtered_saved_character_files.extend(saved_character_files)

    # Prefer selecting the matching JSON file in the saved-character list.
    json_path = get_character_data_file_path(file_path)

    if json_path in saved_character_files:
        saved_character_index = saved_character_files.index(json_path)
    else:
        saved_character_index = 0

    load_character_into_main_gui(loaded_character_data, file_path)
    refresh_saved_character_listbox()

    messagebox.showinfo(
        "Character Loaded",
        "Character loaded into the main generator. You can now use Previous and Next to scroll through saved characters in this folder."
    )

def update_saved_character_table_headings():
    """
    Update table heading text so the sorted column shows an arrow.
    """
    heading_labels = {
        "name": "Name",
        "class": "Class",
        "subclass": "Subclass",
        "species": "Species",
        "level": "Level",
        "background": "Background",
        "alignment": "Alignment"
    }

    for column_name, label_text in heading_labels.items():
        if column_name == saved_character_sort_column:
            arrow = "▼" if saved_character_sort_reverse else "▲"
            heading_text = f"{label_text} {arrow}"
        else:
            heading_text = label_text

        saved_character_tree.heading(
            column_name,
            text=heading_text,
            command=lambda col=column_name: saved_character_column_heading_clicked(col)
        )

def copy_image_prompt_button_clicked():
    if current_character_data is None:
        messagebox.showwarning(
            "No Character",
            "Generate a character before copying an image prompt."
        )
        return

    prompt = generate_character_image_prompt(current_character_data)

    window.clipboard_clear()
    window.clipboard_append(prompt)
    window.update()

    image_prompt_display.delete("1.0", tk.END)
    image_prompt_display.insert(tk.END, prompt)

    messagebox.showinfo(
        "Prompt Copied",
        "The image prompt has been copied to your clipboard."
    )

def previous_character_button_clicked():
    """
    Load the previous character from the current saved-character filter.
    """
    if len(filtered_saved_character_files) == 0:
        messagebox.showwarning(
            "No Character Folder Loaded",
            "Load a saved character first. Then Previous and Next will scroll through that folder."
        )
        return

    load_saved_character_by_index(saved_character_index - 1)


def next_character_button_clicked():
    """
    Load the next character from the current saved-character filter.
    """
    if len(filtered_saved_character_files) == 0:
        messagebox.showwarning(
            "No Character Folder Loaded",
            "Load a saved character first. Then Previous and Next will scroll through that folder."
        )
        return

    load_saved_character_by_index(saved_character_index + 1)

def print_character_button_clicked():
    if current_character_file_path is None:
        save_first = messagebox.askyesno(
            "Save Before Printing",
            "This character has not been saved yet. Save it now so the program can create a printable PDF?"
        )

        if not save_first:
            return

        save_character_bundle_button_clicked()

        if current_character_file_path is None:
            return

    print_current_character_pdf()

def toggle_options_button_clicked():
    global options_visible

    if options_visible:
        options_frame.pack_forget()
        toggle_options_button.config(text="Show Character Options")
        options_visible = False
    else:
        options_frame.pack(pady=5)
        toggle_options_button.config(text="Hide Character Options")
        options_visible = True

def saved_character_listbox_double_clicked(event):
    """
    Load the character the user double-clicked in the Saved table.
    """
    selected_items = saved_character_tree.selection()

    if len(selected_items) == 0:
        return

    selected_index = int(selected_items[0])
    load_saved_character_by_index(selected_index)

def saved_character_search_changed(event=None):
    """
    Re-filter the saved-character list whenever the user types
    in the search box.
    """
    global saved_character_index

    saved_character_index = -1
    refresh_saved_character_listbox()


def clear_saved_character_search_button_clicked():
    """
    Clear the saved-character search box and show the full list again.
    """
    global saved_character_index

    saved_character_search_entry.delete(0, tk.END)
    saved_character_index = -1
    refresh_saved_character_listbox()

def refresh_saved_characters_button_clicked():
    """
    Re-scan the current saved-character folder and refresh the Saved tab.

    This is useful after editing and saving a character because the table
    may still be showing old values until the folder is scanned again.
    """
    global saved_character_files
    global filtered_saved_character_files
    global saved_character_index

    if saved_character_folder == "":
        messagebox.showwarning(
            "No Character Folder Loaded",
            "Load a saved character first. Then Refresh will update that folder."
        )
        return

    saved_character_files = find_saved_character_files(saved_character_folder)

    filtered_saved_character_files.clear()
    filtered_saved_character_files.extend(saved_character_files)

    saved_character_index = -1
    refresh_saved_character_listbox()

def paste_portrait_button_clicked():
    portrait_image, error_message = get_clipboard_image()

    if error_message is not None:
        messagebox.showwarning(
            "No Image Found",
            error_message
        )
        return

    display_portrait_image(portrait_image)
    mark_current_character_changed()

def choose_portrait_file_button_clicked():
    initial_folder = get_last_character_folder()

    file_path = filedialog.askopenfilename(
        initialdir=initial_folder,
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.webp *.bmp"),
            ("PNG Files", "*.png"),
            ("JPEG Files", "*.jpg *.jpeg"),
            ("All Files", "*.*")
        ]
    )

    if file_path == "":
        return

    remember_last_character_folder(os.path.dirname(file_path))

    try:
        portrait_image = load_portrait_image_from_file(file_path)
        display_portrait_image(portrait_image)
        mark_current_character_changed()

        messagebox.showinfo(
            "Portrait Loaded",
            "Portrait image loaded successfully."
        )

    except Exception as error:
        messagebox.showerror(
            "Image Load Failed",
            f"The program could not load this image.\n\n{error}"
        )

def show_image_prompt_button_clicked():
    if current_character_data is None:
        messagebox.showwarning(
            "No Character",
            "Generate a character before creating an image prompt."
        )
        return

    notebook.select(image_prompt_tab)

def show_roll_method_help_button_clicked():
    help_text = (
        "Ability Score Roll Methods\n\n"
        "4d6 Drop Lowest:\n"
        "Rolls four six-sided dice, drops the lowest die, and totals the rest. "
        "This is random, so Reroll Stats usually changes the scores.\n\n"

        "3d6 Straight:\n"
        "Rolls three six-sided dice for each ability in fixed order. "
        "This is random and more old-school, often creating weaker or uneven characters.\n\n"

        "Heroic 2d6+6:\n"
        "Rolls two six-sided dice and adds 6. "
        "This is random but usually creates stronger adventurers.\n\n"

        "Standard Array:\n"
        "Uses fixed scores: 15, 14, 13, 12, 10, 8. "
        "This is not random, so rerolling with the same class and species will usually not change anything.\n\n"

        "Point Buy:\n"
        "Uses a fixed fair spread: 15, 15, 14, 10, 8, 8. "
        "This is not random, so rerolling with the same class and species will usually not change anything.\n\n"

        "Note: Class priority decides where the best scores go. "
        "Species bonuses are applied after the base scores are chosen."
    )

    messagebox.showinfo(
        "Roll Method Help",
        help_text
    )

# ============================================================
# GUI LAYOUT
# This section builds the actual Tkinter window:
# title panel, buttons, character options, tabs, sheet cards,
# portrait frame, saved character browser, and starting messages.
# ============================================================

# Create the main window
window = tk.Tk()
window.title("Dragon Scrolls Character Generator")

# ------------------------------------------------------------
# App Icon
# Sets the icon shown in the window title bar and taskbar.
# The .ico file should live in the same folder as this Python file.
# ------------------------------------------------------------
try:
    window.iconbitmap("dragon_scrolls_app_icon.ico")
except tk.TclError:
    # If the icon file is missing or Windows cannot load it,
    # the app still opens normally with the default Tkinter icon.
    pass

# ------------------------------------------------------------
# Status Bar
# Shows whether the current character is new, loaded, saved,
# or cleared.
#
# Important:
# This is created early and packed to the bottom before the
# notebook is created. That way the large notebook area does
# not consume all available space and hide the status bar.
# ------------------------------------------------------------
status_text = tk.StringVar()
status_text.set("No character loaded.")

status_bar = tk.Label(
    window,
    textvariable=status_text,
    anchor=tk.W,
    font=("Consolas", 9),
    relief=tk.SUNKEN,
    bd=1
)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Start with a normal fallback size first.
window.geometry("1450x800")
window.minsize(1100, 700)

# Open maximized on Windows.
# If this ever runs on a system that does not support "zoomed",
# the fallback geometry above will still work.
try:
    window.state("zoomed")
except tk.TclError:
    pass

# Top title panel with pixel-art stone banner and flickering torches
top_panel_canvas = tk.Canvas(
    window,
    height=120,
    highlightthickness=0,
    bd=0
)
top_panel_canvas.pack(padx=12, pady=8, fill=tk.X)

title_shadow_item = top_panel_canvas.create_text(
    0,
    0,
    text="Dragon Scrolls Character Generator",
    fill=PIXEL_TITLE_SHADOW,
    font=TITLE_FONT
)

title_text_item = top_panel_canvas.create_text(
    0,
    0,
    text="Dragon Scrolls Character Generator",
    fill=COLOR_GOLD,
    font=TITLE_FONT
)

left_torch_item = top_panel_canvas.create_image(80, 60)
right_torch_item = top_panel_canvas.create_image(0, 60)

top_panel_canvas.bind(
    "<Configure>",
    lambda event: draw_top_panel_background(
        top_panel_canvas,
        title_shadow_item,
        title_text_item,
        left_torch_item,
        right_torch_item,
        event
    )
)

# Main controls area
controls_frame = tk.Frame(window)
controls_frame.pack(pady=5, fill=tk.X)

controls_row_1 = tk.Frame(controls_frame)
controls_row_1.pack(pady=3)

controls_row_2 = tk.Frame(controls_frame)
controls_row_2.pack(pady=3)

main_actions_frame = tk.LabelFrame(
    controls_row_1,
    text="Main Actions",
    font=("Georgia", 10, "bold")
)
main_actions_frame.pack(side=tk.LEFT, padx=8)

reroll_actions_frame = tk.LabelFrame(
    controls_row_1,
    text="Reroll Tools",
    font=("Georgia", 10, "bold")
)
reroll_actions_frame.pack(side=tk.LEFT, padx=8)

saved_actions_frame = tk.LabelFrame(
    controls_row_2,
    text="Saved Characters",
    font=("Georgia", 10, "bold")
)
saved_actions_frame.pack(side=tk.LEFT, padx=8)

portrait_actions_frame = tk.LabelFrame(
    controls_row_2,
    text="Portrait Tools",
    font=("Georgia", 10, "bold")
)
portrait_actions_frame.pack(side=tk.LEFT, padx=8)

toggle_options_button = tk.Button(
    window,
    text="Hide Character Options",
    font=("Arial", 11),
    command=toggle_options_button_clicked
)
toggle_options_button.pack(pady=3)

options_frame = tk.LabelFrame(
    window,
    text="Character Options",
    font=("Georgia", 10, "bold")
)
options_frame.pack(pady=5)

# Custom name frame
name_frame = tk.Frame(options_frame)
name_frame.pack(pady=5)

name_label = tk.Label(
    name_frame,
    text="Name:",
    font=("Arial", 11)
)
name_label.pack(side=tk.LEFT, padx=5)

name_entry = tk.Entry(
    name_frame,
    width=30,
    font=("Georgia", 11)
)
name_entry.pack(side=tk.LEFT, padx=5)

apply_name_button = tk.Button(
    name_frame,
    text="Apply Name",
    font=("Arial", 11),
    command=apply_custom_name_button_clicked
)
apply_name_button.pack(side=tk.LEFT, padx=5)

apply_selected_options_button = tk.Button(
    name_frame,
    text="Apply Selected Options",
    font=("Arial", 11),
    command=apply_selected_options_button_clicked
)
apply_selected_options_button.pack(side=tk.LEFT, padx=5)

# Choice frame
choice_frame = tk.Frame(options_frame)
choice_frame.pack(pady=5)

choice_row_1 = tk.Frame(choice_frame)
choice_row_1.pack(pady=3)

choice_row_2 = tk.Frame(choice_frame)
choice_row_2.pack(pady=3)

class_label = tk.Label(
    choice_row_1,
    text="Class:",
    font=("Arial", 11)
)
class_label.pack(side=tk.LEFT, padx=5)

class_choice = ttk.Combobox(
    choice_row_1,
    values=["Random"] + classes,
    state="readonly",
    width=15
)
class_choice.set("Random")
class_choice.pack(side=tk.LEFT, padx=5)

class_choice.bind("<<ComboboxSelected>>", update_subclass_options)

subclass_label = tk.Label(
    choice_row_1,
    text="Subclass:",
    font=("Arial", 11)
)
subclass_label.pack(side=tk.LEFT, padx=5)

subclass_choice = ttk.Combobox(
    choice_row_1,
    values=["Random"],
    state="readonly",
    width=24
)
subclass_choice.set("Random")
subclass_choice.pack(side=tk.LEFT, padx=5)

species_label = tk.Label(
    choice_row_1,
    text="Species:",
    font=("Arial", 11)
)
species_label.pack(side=tk.LEFT, padx=5)

species_choice = ttk.Combobox(
    choice_row_1,
    values=["Random"] + species,
    state="readonly",
    width=15
)
species_choice.set("Random")
species_choice.pack(side=tk.LEFT, padx=5)

alignment_label = tk.Label(
    choice_row_2,
    text="Alignment:",
    font=("Arial", 11)
)
alignment_label.pack(side=tk.LEFT, padx=5)

alignment_choice = ttk.Combobox(
    choice_row_2,
    values=["Random"] + alignments,
    state="readonly",
    width=18
)
alignment_choice.set("Random")
alignment_choice.pack(side=tk.LEFT, padx=5)

sex_label = tk.Label(
    choice_row_2,
    text="Sex:",
    font=("Arial", 11)
)
sex_label.pack(side=tk.LEFT, padx=5)

sex_choice = ttk.Combobox(
    choice_row_2,
    values=["Random"] + sex_options,
    state="readonly",
    width=10
)
sex_choice.set("Random")
sex_choice.pack(side=tk.LEFT, padx=5)

background_label = tk.Label(
    choice_row_1,
    text="Background:",
    font=("Arial", 11)
)
background_label.pack(side=tk.LEFT, padx=5)

background_choice = ttk.Combobox(
    choice_row_1,
    values=["Random"] + backgrounds,
    state="readonly",
    width=15
)
background_choice.set("Random")
background_choice.pack(side=tk.LEFT, padx=5)

level_label = tk.Label(
    choice_row_2,
    text="Level:",
    font=("Arial", 11)
)
level_label.pack(side=tk.LEFT, padx=5)

level_choice = ttk.Combobox(
    choice_row_2,
    values=level_options,
    state="readonly",
    width=5
)
level_choice.set("1")
level_choice.pack(side=tk.LEFT, padx=5)

roll_method_label = tk.Label(
    choice_row_2,
    text="Rolls:",
    font=("Arial", 11)
)
roll_method_label.pack(side=tk.LEFT, padx=5)

roll_method_choice = ttk.Combobox(
    choice_row_2,
    values=roll_method_options,
    state="readonly",
    width=20
)
roll_method_choice.set("4d6 Drop Lowest")
roll_method_choice.pack(side=tk.LEFT, padx=5)

roll_method_help_button = tk.Button(
    choice_row_2,
    text="?",
    font=("Arial", 10, "bold"),
    width=2,
    command=show_roll_method_help_button_clicked
)
roll_method_help_button.pack(side=tk.LEFT, padx=3)

# Surgical editor frame
# These buttons edit only one part of a loaded/generated character
# instead of rebuilding the whole character.
surgical_edit_frame = tk.Frame(options_frame)
surgical_edit_frame.pack(pady=5)

apply_identity_only_button = tk.Button(
    surgical_edit_frame,
    text="Apply Identity Only",
    font=("Arial", 10),
    command=apply_identity_only_button_clicked
)
apply_identity_only_button.pack(side=tk.LEFT, padx=5)

apply_level_only_button = tk.Button(
    surgical_edit_frame,
    text="Apply Level Only",
    font=("Arial", 10),
    command=apply_level_only_button_clicked
)
apply_level_only_button.pack(side=tk.LEFT, padx=5)

apply_subclass_only_button = tk.Button(
    surgical_edit_frame,
    text="Apply Subclass Only",
    font=("Arial", 10),
    command=apply_subclass_only_button_clicked
)
apply_subclass_only_button.pack(side=tk.LEFT, padx=5)

# Keep options frame
keep_frame = tk.Frame(options_frame)
keep_frame.pack(pady=5)

keep_name_var = tk.BooleanVar()
keep_class_var = tk.BooleanVar()
keep_species_var = tk.BooleanVar()
keep_alignment_var = tk.BooleanVar()
keep_sex_var = tk.BooleanVar()
keep_background_var = tk.BooleanVar()

keep_name_checkbox = tk.Checkbutton(
    keep_frame,
    text="Keep Name",
    variable=keep_name_var,
    font=("Arial", 10)
)
keep_name_checkbox.pack(side=tk.LEFT, padx=5)

keep_class_checkbox = tk.Checkbutton(
    keep_frame,
    text="Keep Class",
    variable=keep_class_var,
    font=("Arial", 10)
)
keep_class_checkbox.pack(side=tk.LEFT, padx=5)

keep_species_checkbox = tk.Checkbutton(
    keep_frame,
    text="Keep Species",
    variable=keep_species_var,
    font=("Arial", 10)
)
keep_species_checkbox.pack(side=tk.LEFT, padx=5)

keep_alignment_checkbox = tk.Checkbutton(
    keep_frame,
    text="Keep Alignment",
    variable=keep_alignment_var,
    font=("Arial", 10)
)
keep_alignment_checkbox.pack(side=tk.LEFT, padx=5)

keep_sex_checkbox = tk.Checkbutton(
    keep_frame,
    text="Keep Sex",
    variable=keep_sex_var,
    font=("Arial", 10)
)
keep_sex_checkbox.pack(side=tk.LEFT, padx=5)

keep_background_checkbox = tk.Checkbutton(
    keep_frame,
    text="Keep Background",
    variable=keep_background_var,
    font=("Arial", 10)
)
keep_background_checkbox.pack(side=tk.LEFT, padx=5)

# Main actions frame
generate_button = tk.Button(
    main_actions_frame,
    text="Generate",
    font=("Arial", 12),
    command=generate_character_button_clicked
)
generate_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(
    main_actions_frame,
    text="Save",
    font=("Arial", 12),
    command=save_character_bundle_button_clicked
)
save_button.pack(side=tk.LEFT, padx=5)

save_as_new_button = tk.Button(
    main_actions_frame,
    text="Save As New",
    font=("Arial", 12),
    command=save_as_new_character_button_clicked
)
save_as_new_button.pack(side=tk.LEFT, padx=5)

print_button = tk.Button(
    main_actions_frame,
    text="Print",
    font=("Arial", 12),
    command=print_character_button_clicked
)
print_button.pack(side=tk.LEFT, padx=5)

dice_roller_button = tk.Button(
    main_actions_frame,
    text="🎲 Dice",
    font=("Arial", 12),
    command=open_dice_roller_window
)
dice_roller_button.pack(side=tk.LEFT, padx=5)


# Reroll actions frame
reroll_name_button = tk.Button(
    reroll_actions_frame,
    text="Reroll Name",
    font=("Arial", 12),
    command=reroll_name_button_clicked
)
reroll_name_button.pack(side=tk.LEFT, padx=5)

reroll_stats_button = tk.Button(
    reroll_actions_frame,
    text="Reroll Stats",
    font=("Arial", 12),
    command=reroll_ability_scores_button_clicked
)
reroll_stats_button.pack(side=tk.LEFT, padx=5)

reroll_roleplay_button = tk.Button(
    reroll_actions_frame,
    text="Reroll RP",
    font=("Arial", 12),
    command=reroll_roleplay_traits_button_clicked
)
reroll_roleplay_button.pack(side=tk.LEFT, padx=5)

# Saved actions frame
view_saved_button = tk.Button(
    saved_actions_frame,
    text="Load Character",
    font=("Arial", 12),
    command=view_saved_character_button_clicked
)
view_saved_button.pack(side=tk.LEFT, padx=5)

previous_character_button = tk.Button(
    saved_actions_frame,
    text="< Previous",
    font=("Arial", 12),
    command=previous_character_button_clicked
)
previous_character_button.pack(side=tk.LEFT, padx=5)

next_character_button = tk.Button(
    saved_actions_frame,
    text="Next >",
    font=("Arial", 12),
    command=next_character_button_clicked
)
next_character_button.pack(side=tk.LEFT, padx=5)

delete_character_button = tk.Button(
    saved_actions_frame,
    text="Delete",
    font=("Arial", 12),
    command=delete_character_button_clicked
)
delete_character_button.pack(side=tk.LEFT, padx=5)

# Portrait actions frame
copy_prompt_button = tk.Button(
    portrait_actions_frame,
    text="Copy Prompt",
    font=("Arial", 12),
    command=copy_image_prompt_button_clicked
)
copy_prompt_button.pack(side=tk.LEFT, padx=5)

paste_portrait_button = tk.Button(
    portrait_actions_frame,
    text="Paste Image",
    font=("Arial", 12),
    command=paste_portrait_button_clicked
)
paste_portrait_button.pack(side=tk.LEFT, padx=5)

choose_portrait_button = tk.Button(
    portrait_actions_frame,
    text="Choose Portrait",
    font=("Arial", 12),
    command=choose_portrait_file_button_clicked
)
choose_portrait_button.pack(side=tk.LEFT, padx=5)

image_prompt_button = tk.Button(
    portrait_actions_frame,
    text="Show Prompt",
    font=("Arial", 12),
    command=show_image_prompt_button_clicked
)
image_prompt_button.pack(side=tk.LEFT, padx=5)

# ------------------------------------------------------------
# Main Notebook Tabs
# Each tab shows a different view of the same character data.
# ------------------------------------------------------------
notebook_outer_frame = tk.Frame(
    window,
    bg=COLOR_GRIMOIRE_BORDER
)
notebook_outer_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

notebook_middle_frame = tk.Frame(
    notebook_outer_frame,
    bg=COLOR_GRIMOIRE_INNER_BORDER
)
notebook_middle_frame.pack(padx=3, pady=3, fill=tk.BOTH, expand=True)

notebook_inner_frame = tk.Frame(
    notebook_middle_frame,
    bg=COLOR_STONE_DARK,
    bd=4,
    relief=tk.RIDGE
)
notebook_inner_frame.pack(padx=4, pady=4, fill=tk.BOTH, expand=True)

notebook = ttk.Notebook(notebook_inner_frame, style="Dungeon.TNotebook")
notebook.pack(padx=6, pady=6, fill=tk.BOTH, expand=True)

sheet_tab = tk.Frame(notebook)
summary_tab = tk.Frame(notebook)
abilities_tab = tk.Frame(notebook)
skills_tab = tk.Frame(notebook)
combat_tab = tk.Frame(notebook)
equipment_tab = tk.Frame(notebook)
spells_tab = tk.Frame(notebook)
roleplay_tab = tk.Frame(notebook)
features_tab = tk.Frame(notebook)
image_prompt_tab = tk.Frame(notebook)
saved_characters_tab = tk.Frame(notebook)
spellbook_tab = tk.Frame(notebook)

notebook.add(sheet_tab, text="▣ Sheet")
notebook.add(summary_tab, text="📜 Summary")
notebook.add(abilities_tab, text="◆ Abilities")
notebook.add(skills_tab, text="✦ Skills")
notebook.add(combat_tab, text="⚔ Combat")
notebook.add(equipment_tab, text="🎒 Equipment")
notebook.add(spells_tab, text="✦ Spells")
notebook.add(spellbook_tab, text="🧙 Spellbook")
notebook.add(roleplay_tab, text="☽ Roleplay")
notebook.add(features_tab, text="★ Features")
notebook.add(image_prompt_tab, text="▧ Image Prompt")
notebook.add(saved_characters_tab, text="💾 Saved")

# ------------------------------------------------------------
# Sheet Tab
# Main dashboard view with card-style sections and portrait.
# ------------------------------------------------------------
sheet_container = tk.Frame(sheet_tab)
sheet_container.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

sheet_top_row = tk.Frame(sheet_container)
sheet_top_row.pack(fill=tk.BOTH, expand=True)

sheet_bottom_row = tk.Frame(sheet_container)
sheet_bottom_row.pack(fill=tk.BOTH, expand=True)

identity_card, sheet_identity_display = create_sheet_card(
    sheet_top_row,
    "Identity",
    width=32,
    height=11
)
identity_card.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

abilities_card, sheet_abilities_display = create_sheet_card(
    sheet_top_row,
    "Abilities",
    width=28,
    height=11
)
abilities_card.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

combat_card, sheet_combat_display = create_sheet_card(
    sheet_top_row,
    "Combat & Skills",
    width=42,
    height=11
)
combat_card.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

# ------------------------------------------------------------
# Portrait Frame
# Shows the character portrait on the Sheet tab.
# Double-clicking the portrait opens a larger preview window.
# ------------------------------------------------------------
portrait_frame = tk.Frame(
    sheet_top_row,
    width=300,
    bg="gray"
)
portrait_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH)
portrait_frame.pack_propagate(False)

portrait_title = tk.Label(
    portrait_frame,
    text="Character Portrait",
    font=("Arial", 12, "bold"),
    bg="gray",
    fg="white"
)
portrait_title.pack(pady=10)

portrait_label = tk.Label(
    portrait_frame,
    text="Copy an image from ChatGPT,\nthen click 'Paste Portrait'.",
    width=40,
    height=22,
    bg="lightgray",
    fg="black",
    relief=tk.SUNKEN,
    justify=tk.CENTER
)
portrait_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
portrait_label.bind("<Configure>", resize_portrait_to_frame)
portrait_label.bind("<Double-Button-1>", open_large_portrait_window)
portrait_frame.bind("<Double-Button-1>", open_large_portrait_window)
portrait_label.config(cursor="hand2")

roleplay_card, sheet_roleplay_display = create_sheet_card(
    sheet_bottom_row,
    "Roleplay",
    width=38,
    height=12
)
roleplay_card.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

equipment_card, sheet_equipment_display = create_sheet_card(
    sheet_bottom_row,
    "Equipment",
    width=30,
    height=12
)
equipment_card.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

spells_card, sheet_spells_display = create_sheet_card(
    sheet_bottom_row,
    "Spells",
    width=30,
    height=12
)
spells_card.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

features_card, sheet_features_display = create_sheet_card(
    sheet_bottom_row,
    "Features",
    width=30,
    height=12
)
features_card.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

summary_display = scrolledtext.ScrolledText(
    summary_tab,
    wrap=tk.WORD,
    font=("Consolas", 11)
)
summary_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

abilities_display = scrolledtext.ScrolledText(
    abilities_tab,
    wrap=tk.WORD,
    font=("Consolas", 11)
)
abilities_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

skills_display = scrolledtext.ScrolledText(
    skills_tab,
    wrap=tk.WORD,
    font=("Consolas", 11)
)
skills_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

combat_display = scrolledtext.ScrolledText(
    combat_tab,
    wrap=tk.WORD,
    font=("Consolas", 11)
)
combat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

equipment_display = scrolledtext.ScrolledText(
    equipment_tab,
    wrap=tk.WORD,
    font=("Consolas", 11)
)
equipment_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

spells_display = scrolledtext.ScrolledText(
    spells_tab,
    wrap=tk.WORD,
    font=("Consolas", 11)
)
spells_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

spellbook_display = scrolledtext.ScrolledText(
    spellbook_tab,
    wrap=tk.WORD,
    font=TAB_TEXT_FONT
)
spellbook_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

roleplay_display = scrolledtext.ScrolledText(
    roleplay_tab,
    wrap=tk.WORD,
    font=("Consolas", 11)
)
roleplay_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

features_display = scrolledtext.ScrolledText(
    features_tab,
    wrap=tk.WORD,
    font=("Consolas", 11)
)
features_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

image_prompt_display = scrolledtext.ScrolledText(
    image_prompt_tab,
    wrap=tk.WORD,
    font=("Consolas", 11)
)
image_prompt_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# ------------------------------------------------------------
# Saved Characters Tab
# Shows the saved character list after a saved folder is loaded.
#
# Current behavior:
# - Load Character lets the user choose one saved file.
# - The app then scans that folder for other saved characters.
# - Previous / Next scroll through that folder.
# - Double-clicking a list item loads that character.
#
# Search will be added in a later sprint after this section is clean.
# ------------------------------------------------------------
saved_characters_frame = tk.Frame(saved_characters_tab)
saved_characters_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

saved_characters_label = tk.Label(
    saved_characters_frame,
    text="Saved Characters",
    font=("Arial", 16, "bold")
)
saved_characters_label.pack(pady=5)

# Search row for filtering saved characters by name, class,
# subclass, species, background, alignment, sex, or level.
saved_search_frame = tk.Frame(saved_characters_frame)
saved_search_frame.pack(fill=tk.X, padx=10, pady=(5, 2))

saved_character_search_label = tk.Label(
    saved_search_frame,
    text="Search:",
    font=("Arial", 11)
)
saved_character_search_label.pack(side=tk.LEFT, padx=5)

saved_character_search_entry = tk.Entry(
    saved_search_frame,
    font=("Consolas", 11),
    width=40
)
saved_character_search_entry.pack(side=tk.LEFT, padx=5)

saved_character_search_entry.bind(
    "<KeyRelease>",
    saved_character_search_changed
)

clear_saved_character_search_button = tk.Button(
    saved_search_frame,
    text="Clear",
    font=("Arial", 10),
    command=clear_saved_character_search_button_clicked
)
clear_saved_character_search_button.pack(side=tk.LEFT, padx=5)

refresh_saved_characters_button = tk.Button(
    saved_search_frame,
    text="Refresh",
    font=("Arial", 10),
    command=refresh_saved_characters_button_clicked
)
refresh_saved_characters_button.pack(side=tk.LEFT, padx=5)

saved_character_count_label = tk.Label(
    saved_search_frame,
    text="0 saved characters shown",
    font=("Arial", 10)
)
saved_character_count_label.pack(side=tk.LEFT, padx=8)

# Saved character table.
# This replaces the old single-column Listbox with a multi-column
# table so search results are easier to understand.
saved_character_columns = (
    "name",
    "class",
    "subclass",
    "species",
    "level",
    "background",
    "alignment"
)

saved_character_tree = ttk.Treeview(
    saved_characters_frame,
    columns=saved_character_columns,
    show="headings",
    height=18,
    style="Dungeon.Treeview"
)

saved_character_tree.heading(
    "name",
    text="Name",
    command=lambda: saved_character_column_heading_clicked("name")
)

saved_character_tree.heading(
    "class",
    text="Class",
    command=lambda: saved_character_column_heading_clicked("class")
)

saved_character_tree.heading(
    "subclass",
    text="Subclass",
    command=lambda: saved_character_column_heading_clicked("subclass")
)

saved_character_tree.heading(
    "species",
    text="Species",
    command=lambda: saved_character_column_heading_clicked("species")
)

saved_character_tree.heading(
    "level",
    text="Level",
    command=lambda: saved_character_column_heading_clicked("level")
)

saved_character_tree.heading(
    "background",
    text="Background",
    command=lambda: saved_character_column_heading_clicked("background")
)

saved_character_tree.heading(
    "alignment",
    text="Alignment",
    command=lambda: saved_character_column_heading_clicked("alignment")
)

saved_character_tree.column("name", width=180, anchor=tk.W)
saved_character_tree.column("class", width=100, anchor=tk.CENTER)
saved_character_tree.column("subclass", width=160, anchor=tk.CENTER)
saved_character_tree.column("species", width=100, anchor=tk.CENTER)
saved_character_tree.column("level", width=60, anchor=tk.CENTER)
saved_character_tree.column("background", width=130, anchor=tk.CENTER)
saved_character_tree.column("alignment", width=130, anchor=tk.CENTER)

saved_character_tree.pack(
    padx=10,
    pady=10,
    fill=tk.BOTH,
    expand=True
)

saved_character_tree.bind(
    "<Double-Button-1>",
    saved_character_listbox_double_clicked
)

saved_characters_help = tk.Label(
    saved_characters_frame,
    text="Click 'Load Character' to choose a folder. Then double-click a character here, or use Previous and Next.",
    font=("Arial", 10)
)
saved_characters_help.pack(pady=5)

# ------------------------------------------------------------
# Starting Messages
# These messages appear before any character has been generated.
# ------------------------------------------------------------
starting_message = "Click 'Generate Character' to create your first GUI character.\n"
starting_prompt_message = "Generate a character, then click 'Copy Image Prompt'.\n"

sheet_identity_display.insert(tk.END, starting_message)
summary_display.insert(tk.END, starting_message)
image_prompt_display.insert(tk.END, starting_prompt_message)


# ============================================================
# PROGRAM STARTUP
# Applies the theme, builds animation frames, starts torch
# animation, and launches the Tkinter event loop.
# ============================================================
window.protocol("WM_DELETE_WINDOW", close_window_button_clicked)

apply_theme()

left_torch_frames, right_torch_frames = build_torch_animation_frames()

draw_top_panel_background(
    top_panel_canvas,
    title_shadow_item,
    title_text_item,
    left_torch_item,
    right_torch_item
)

animate_torches()

# Run the GUI
window.mainloop()
