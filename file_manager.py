# ============================================================
# FILE MANAGER
# Handles saved character bundle paths, JSON/TXT loading,
# saved-character discovery, and bundle deletion.
#
# This file should NOT create GUI widgets.
# This file should NOT show message boxes.
# This file should NOT directly change GUI state.
# ============================================================

import json
import os

from data_tables import *
from character_generator import *

def get_character_folder(character_file_path):
    return os.path.dirname(character_file_path)


def get_character_core_name(character_file_path):
    file_name = os.path.basename(character_file_path)
    base_name = os.path.splitext(file_name)[0]

    known_prefixes = ["TXT-", "PDF-", "JSON-", "PNG-"]

    for prefix in known_prefixes:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix):]

    if base_name.endswith("_portrait"):
        base_name = base_name.replace("_portrait", "")

    return base_name


def get_character_bundle_paths(character_file_path):
    folder = get_character_folder(character_file_path)
    core_name = get_character_core_name(character_file_path)

    paths = {
        "txt": os.path.join(folder, "TXT-" + core_name + ".txt"),
        "pdf": os.path.join(folder, "PDF-" + core_name + ".pdf"),
        "json": os.path.join(folder, "JSON-" + core_name + ".json"),
        "portrait": os.path.join(folder, "PNG-" + core_name + "_portrait.png")
    }

    return paths


def get_text_file_path(character_file_path):
    return get_character_bundle_paths(character_file_path)["txt"]


def get_pdf_file_path(character_file_path):
    return get_character_bundle_paths(character_file_path)["pdf"]


def get_character_data_file_path(character_file_path):
    return get_character_bundle_paths(character_file_path)["json"]


def get_portrait_file_path(character_file_path):
    return get_character_bundle_paths(character_file_path)["portrait"]

def find_saved_character_files(folder_path):
    found_files = []

    if folder_path == "":
        return found_files

    for file_name in os.listdir(folder_path):
        if file_name.startswith("JSON-") and file_name.endswith(".json"):
            full_path = os.path.join(folder_path, file_name)
            found_files.append(full_path)

    found_files.sort()

    return found_files

def get_saved_character_search_text(character_file_path):
    search_parts = []

    display_name = get_saved_character_display_name(character_file_path)
    search_parts.append(display_name)

    character_data = load_character_data_if_it_exists(character_file_path)

    if character_data is not None:
        search_parts.append(character_data.get("name", ""))
        search_parts.append(character_data.get("class", ""))
        search_parts.append(character_data.get("subclass", ""))
        search_parts.append(character_data.get("species", ""))
        search_parts.append(character_data.get("background", ""))
        search_parts.append(character_data.get("alignment", ""))
        search_parts.append(character_data.get("sex", ""))
        search_parts.append(f"level {character_data.get('level', '')}")
        search_parts.append(str(character_data.get("level", "")))

    return " ".join(search_parts).lower()

def get_saved_character_display_name(file_path):
    core_name = get_character_core_name(file_path)

    display_name = core_name.replace("_character", "")
    display_name = display_name.replace("_", " ")

    return display_name

def get_saved_character_search_text(character_file_path):
    """
    Build one lowercase searchable text blob for a saved character.

    This lets the GUI search by:
    - display name
    - character name
    - class
    - subclass
    - species
    - background
    - alignment
    - sex
    - level
    """
    search_parts = []

    display_name = get_saved_character_display_name(character_file_path)
    search_parts.append(display_name)

    character_data = load_character_data_if_it_exists(character_file_path)

    if character_data is not None:
        search_parts.append(character_data.get("name", ""))
        search_parts.append(character_data.get("class", ""))
        search_parts.append(character_data.get("subclass", ""))
        search_parts.append(character_data.get("species", ""))
        search_parts.append(character_data.get("background", ""))
        search_parts.append(character_data.get("alignment", ""))
        search_parts.append(character_data.get("sex", ""))

        character_level = character_data.get("level", "")
        search_parts.append(str(character_level))
        search_parts.append(f"level {character_level}")

    return " ".join(search_parts).lower()

def load_character_data_if_it_exists(character_file_path):
    data_file_path = get_character_data_file_path(character_file_path)

    if not os.path.exists(data_file_path):
        return None

    with open(data_file_path, "r", encoding="utf-8") as file:
        loaded_character_data = json.load(file)

    return loaded_character_data

def load_character_data_from_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    loaded_character_data = None
    saved_character_text = ""

    if file_extension == ".json":
        with open(file_path, "r", encoding="utf-8") as file:
            loaded_character_data = json.load(file)

    else:
        loaded_character_data = load_character_data_if_it_exists(file_path)

        if loaded_character_data is None:
            matching_txt_path = get_text_file_path(file_path)

            if os.path.exists(matching_txt_path):
                with open(matching_txt_path, "r", encoding="utf-8") as file:
                    saved_character_text = file.read()

                loaded_character_data = parse_saved_text_character(saved_character_text)

        if loaded_character_data is None and file_extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as file:
                saved_character_text = file.read()

            loaded_character_data = parse_saved_text_character(saved_character_text)

    return loaded_character_data

def parse_saved_text_character(saved_character_text):
    character_data = generate_character_data()

    lines = saved_character_text.splitlines()

    ability_scores = {}

    for line in lines:
        line = line.strip()

        if line.startswith("Name: "):
            character_data["name"] = line.replace("Name: ", "").strip()

        elif line.startswith("Species: "):
            character_data["species"] = line.replace("Species: ", "").strip()

        elif line.startswith("Class: "):
            character_data["class"] = line.replace("Class: ", "").strip()

        elif line.startswith("Subclass: "):
            character_data["subclass"] = line.replace("Subclass: ", "").strip()

        elif line.startswith("Background: "):
            character_data["background"] = line.replace("Background: ", "").strip()

        elif line.startswith("Alignment: "):
            character_data["alignment"] = line.replace("Alignment: ", "").strip()

        elif line.startswith("Sex: "):
            character_data["sex"] = line.replace("Sex: ", "").strip()

        elif line.startswith("Level: "):
            level_text = line.replace("Level: ", "").strip()
            if level_text.isdigit():
                character_data["level"] = int(level_text)
        elif line.startswith("Roll Method: "):
            roll_method_text = line.replace("Roll Method: ", "").strip()

            if roll_method_text in roll_method_options:
                character_data["roll_method"] = roll_method_text
        else:
            for ability in ability_order:
                if line.startswith(ability + ": "):
                    score_part = line.replace(ability + ": ", "").strip()
                    score_text = score_part.split(" ")[0]

                    if score_text.isdigit():
                        ability_scores[ability] = int(score_text)

        if len(ability_scores) == 6:
            character_class = character_data["class"]
            character_level = character_data["level"]
            proficiency_bonus = calculate_proficiency_bonus(character_level)

            if "roll_method" not in character_data:
                character_data["roll_method"] = "4d6 Drop Lowest"

            character_data["ability_scores"] = ability_scores
            character_data["proficiency_bonus"] = proficiency_bonus
            character_data["saving_throws"] = calculate_saving_throws(
                character_class,
                ability_scores,
                proficiency_bonus
            )
            character_data["skills"] = calculate_skills(
                character_class,
                ability_scores,
                proficiency_bonus
            )
            character_data["hit_points"] = calculate_hit_points(
                character_class,
                ability_scores,
                character_level
            )
            character_data["armor_class"] = calculate_armor_class(ability_scores)
            character_data["initiative"] = calculate_initiative(ability_scores)
            character_data["speed"] = calculate_speed(character_data["species"])
            character_data["passive_perception"] = calculate_passive_perception(
                character_data["skills"]
            )
            character_data["weapon_attacks"] = calculate_weapon_attacks(
                character_class,
                ability_scores,
                proficiency_bonus
            )
            character_data["spellcasting"] = calculate_spellcasting(
                character_class,
                ability_scores,
                proficiency_bonus,
                character_level
            )
            character_data["equipment"] = generate_starting_equipment(character_class)
            character_data["class_features"] = generate_class_features(
                character_class,
                character_level
            )

            if "subclass" not in character_data:
                character_data["subclass"] = generate_subclass(
                    character_class,
                    character_level,
                    "Random"
                )
            character_data["subclass_features"] = generate_subclass_features(
                character_data.get("subclass", "None"),
                character_level
            )

    return character_data

def delete_character_bundle(character_file_path):
    bundle_paths = get_character_bundle_paths(character_file_path)

    deleted_files = []

    for file_type, file_path in bundle_paths.items():
        if os.path.exists(file_path):
            os.remove(file_path)
            deleted_files.append(file_path)

    return deleted_files
