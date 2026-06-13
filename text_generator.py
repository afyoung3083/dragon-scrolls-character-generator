# ============================================================
# TEXT GENERATION
# Converts character_data dictionaries into readable text for
# GUI tabs, TXT export, image prompts, and full character sheets.
#
# This file should NOT create GUI widgets.
# This file should NOT save files.
# This file should NOT build PDFs.
# ============================================================

from data_tables import *
from character_generator import *

def generate_summary_text(character_data):
    character_text = ""
    character_text += "=== D&D Character Generator ===\n\n"
    character_text += f"Name: {character_data['name']}\n"
    character_text += f"Species: {character_data['species']}\n"
    character_text += f"Class: {character_data['class']}\n"
    if character_data.get("subclass", "None") != "None":
        character_text += f"Subclass: {character_data['subclass']}\n"
    character_text += f"Background: {character_data['background']}\n"
    character_text += f"Alignment: {character_data['alignment']}\n"
    character_text += f"Sex: {character_data.get('sex', 'Unknown')}\n"
    character_text += f"Level: {character_data['level']}\n"
    character_text += f"Roll Method: {character_data.get('roll_method', '4d6 Drop Lowest')}\n"

    return character_text


def generate_abilities_text(character_data):
    ability_scores = character_data["ability_scores"]

    character_text = ""
    character_text += "=== Ability Scores ===\n\n"

    for ability in ability_order:
        score = ability_scores[ability]
        modifier = calculate_modifier(score)
        modifier_text = format_bonus(modifier)

        character_text += f"{ability}: {score} ({modifier_text})\n"

    return character_text

def generate_skills_text(character_data):
    character_class = character_data["class"]
    saving_throws = character_data["saving_throws"]
    skills = character_data["skills"]

    character_text = ""
    character_text += "=== Saving Throws ===\n\n"

    for ability in ability_order:
        save_bonus = saving_throws[ability]
        save_text = format_bonus(save_bonus)

        if ability in class_saving_throw_proficiencies[character_class]:
            proficient_text = " proficient"
        else:
            proficient_text = ""

        character_text += f"{ability}: {save_text}{proficient_text}\n"

    character_text += "\n=== Skills ===\n\n"

    for skill, skill_bonus in skills.items():
        skill_text = format_bonus(skill_bonus)
        related_ability = skill_ability_map[skill]

        if skill in class_skill_proficiencies[character_class]:
            proficient_text = " proficient"
        else:
            proficient_text = ""

        character_text += f"{skill} ({related_ability}): {skill_text}{proficient_text}\n"

    return character_text

def generate_combat_text(character_data):
    character_text = ""
    character_text += "=== Combat ===\n\n"
    character_text += f"Hit Points: {character_data['hit_points']}\n"
    character_text += f"Armor Class: {character_data['armor_class']}\n"
    character_text += f"Initiative: {format_bonus(character_data['initiative'])}\n"
    character_text += f"Speed: {character_data['speed']} ft.\n"
    character_text += f"Passive Perception: {character_data['passive_perception']}\n"

    character_text += "\n=== Weapon Attacks ===\n\n"

    for weapon_name, weapon_info in character_data["weapon_attacks"].items():
        attack_bonus_text = format_bonus(weapon_info["attack_bonus"])
        damage_bonus_text = format_bonus(weapon_info["damage_bonus"])

        character_text += f"{weapon_name}: {attack_bonus_text} to hit, "
        character_text += f"{weapon_info['damage']} {damage_bonus_text}\n"

    return character_text

def generate_equipment_text(character_data):
    equipment = character_data["equipment"]

    character_text = ""
    character_text += "=== Equipment ===\n\n"

    for item in equipment:
        character_text += f"- {item}\n"

    return character_text

def generate_features_text(character_data):
    character_text = ""
    character_text += "=== Class Features ===\n\n"

    for feature in character_data["class_features"]:
        character_text += f"- {feature}\n"

    subclass_name = character_data.get("subclass", "None")
    subclass_features = character_data.get("subclass_features", [])

    if subclass_name != "None" and len(subclass_features) > 0:
        character_text += f"\n=== Subclass Features: {subclass_name} ===\n\n"

        for feature in subclass_features:
            character_text += f"- {feature}\n"

    return character_text

def generate_roleplay_text(character_data):
    character_text = ""
    character_text += "=== Roleplay ===\n\n"
    character_text += f"Alignment: {character_data['alignment']}\n\n"
    character_text += "=== Roleplay Traits ===\n\n"

    for trait_name, trait_text in character_data["roleplay_traits"].items():
        character_text += f"{trait_name}: {trait_text}\n\n"

    return character_text

def generate_spells_text(character_data):
    character_text = ""
    character_text += "=== Spells ===\n\n"

    spellcasting = character_data["spellcasting"]

    if spellcasting is None:
        character_text += "This character does not have spellcasting.\n"
        return character_text

    character_text += f"Spellcasting Ability: {spellcasting['spellcasting_ability']}\n"
    character_text += f"Spell Save DC: {spellcasting['spell_save_dc']}\n"
    character_text += f"Spell Attack Bonus: {format_bonus(spellcasting['spell_attack_bonus'])}\n"
    character_text += f"Spell Slots: {spellcasting.get('spell_slots', 'No spell slot data.')}\n"

    if len(spellcasting["cantrips"]) > 0:
        character_text += "\nCantrips Shown:\n"
        for spell in spellcasting["cantrips"]:
            character_text += f"- {spell}\n"

    if len(spellcasting["level_1_spells"]) > 0:
        character_text += "\nLevel 1 Spell Examples:\n"
        for spell in spellcasting["level_1_spells"]:
            character_text += f"- {spell}\n"

    if "higher_level_spells" in spellcasting and len(spellcasting["higher_level_spells"]) > 0:
        character_text += "\nHigher-Level Spell Examples:\n"
        for spell in spellcasting["higher_level_spells"]:
            character_text += f"- {spell}\n"

    if (
        len(spellcasting["cantrips"]) == 0
        and len(spellcasting["level_1_spells"]) == 0
        and len(spellcasting.get("higher_level_spells", [])) == 0
    ):
        character_text += "\nNo spells available at this level.\n"

    character_text += "\nNote: Spell list is a compact sample, not a full prepared spellbook.\n"

    return character_text

def generate_spellbook_text(character_data):
    character_text = ""
    character_text += "=== Spellbook ===\n\n"

    character_class = character_data["class"]
    character_level = character_data["level"]
    spellcasting = character_data["spellcasting"]

    if spellcasting is None:
        character_text += "This character does not have spellcasting.\n"
        return character_text

    if character_class not in spell_examples_by_class:
        character_text += "No spellbook examples are available for this class yet.\n"
        return character_text

    spell_table = spell_examples_by_class[character_class]
    highest_spell_level = get_highest_spell_level(character_class, character_level)

    character_text += f"Class: {character_class}\n"
    character_text += f"Level: {character_level}\n"
    character_text += f"Spellcasting Ability: {spellcasting['spellcasting_ability']}\n"
    character_text += f"Spell Save DC: {spellcasting['spell_save_dc']}\n"
    character_text += f"Spell Attack Bonus: {format_bonus(spellcasting['spell_attack_bonus'])}\n"
    character_text += f"Spell Slots: {spellcasting.get('spell_slots', 'No spell slot data.')}\n\n"

    cantrips = spell_table.get("cantrips", [])

    if len(cantrips) > 0:
        character_text += "Cantrips:\n"
        for spell in cantrips:
            character_text += f"- {spell}\n"
        character_text += "\n"

    if highest_spell_level == 0:
        character_text += "No spell examples available at this level.\n"
        return character_text

    for spell_level in range(1, highest_spell_level + 1):
        spells_for_level = spell_table.get(spell_level, [])

        if len(spells_for_level) > 0:
            character_text += f"Level {spell_level} Spell Examples:\n"

            for spell in spells_for_level:
                character_text += f"- {spell}\n"

            character_text += "\n"

    character_text += "Note: This is still a sample spellbook, not a complete official spell list.\n"

    return character_text

def generate_image_prompt_text(character_data):
    character_text = ""
    character_text += "=== Character Image Prompt ===\n\n"
    character_text += generate_character_image_prompt(character_data)

    return character_text

def generate_full_character_text(character_data):
    full_text = ""

    full_text += generate_summary_text(character_data)
    full_text += "\n\n"
    full_text += generate_abilities_text(character_data)
    full_text += "\n\n"
    full_text += generate_skills_text(character_data)
    full_text += "\n\n"
    full_text += generate_combat_text(character_data)
    full_text += "\n\n"
    full_text += generate_equipment_text(character_data)
    full_text += "\n\n"
    full_text += generate_spells_text(character_data)
    full_text += "\n\n"
    full_text += generate_roleplay_text(character_data)
    full_text += "\n\n"
    full_text += generate_features_text(character_data)

    return full_text

def get_subclass_image_flavor(character_data):
    subclass_name = character_data.get("subclass", "None")

    if subclass_name == "None":
        return ""

    if subclass_name not in subclass_image_flavor:
        return ""

    return subclass_image_flavor[subclass_name]

def generate_character_image_prompt(character_data):
    equipment_text = ", ".join(character_data["equipment"])

    roleplay_traits = character_data["roleplay_traits"]
    personality_trait = roleplay_traits["Personality Trait"]
    ideal = roleplay_traits["Ideal"]
    bond = roleplay_traits["Bond"]
    flaw = roleplay_traits["Flaw"]

    prompt = ""
    prompt += "Create a high-quality fantasy tabletop RPG character portrait.\n\n"
    prompt += f"Character Name: {character_data['name']}\n"
    prompt += f"Species: {character_data['species']}\n"
    prompt += f"Class: {character_data['class']}\n"
    if character_data.get("subclass", "None") != "None":
        prompt += f"Subclass: {character_data['subclass']}\n"
    prompt += f"Background: {character_data['background']}\n"
    prompt += f"Alignment: {character_data['alignment']}\n"
    prompt += f"Sex: {character_data.get('sex', 'Unknown')}\n"
    prompt += f"Level: {character_data['level']}\n\n"

    prompt += "Visual Description:\n"
    subclass_text = ""

    if character_data.get("subclass", "None") != "None":
        subclass_text = f" with the {character_data['subclass']} subclass"

    prompt += f"The character is a {character_data.get('sex', 'Unknown').lower()} {character_data['species']} {character_data['class']}{subclass_text} named {character_data['name']} "
    prompt += f"with a {character_data['background']} background. "
    prompt += f"They carry or wear the following notable equipment: {equipment_text}. "

    subclass_flavor = get_subclass_image_flavor(character_data)

    if subclass_flavor != "":
        prompt += subclass_flavor + " "

    prompt += "The image should look like a serious fantasy character portrait suitable for a tabletop RPG character sheet.\n\n"

    prompt += "Personality and Mood:\n"
    prompt += f"Personality Trait: {personality_trait}\n"
    prompt += f"Ideal: {ideal}\n"
    prompt += f"Bond: {bond}\n"
    prompt += f"Flaw: {flaw}\n\n"

    prompt += "Art Direction:\n"
    prompt += "Use a detailed painterly fantasy style, dramatic but readable lighting, "
    prompt += "clear face and upper body, detailed armor or clothing appropriate to the class, "
    prompt += "no text, no logo, no watermark, no character sheet borders."

    return prompt
