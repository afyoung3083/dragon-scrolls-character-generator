# ============================================================
# CHARACTER GENERATION LOGIC
# Creates random names, rolls ability scores, applies species
# bonuses, calculates modifiers, saving throws, skills, hit
# points, armor class, attacks, spells, equipment, class features,
# roleplay traits, and the full character_data dictionary.
#
# This file should NOT create GUI widgets.
# This file should NOT save files.
# This file should NOT build PDFs.
# ============================================================

import random

from data_tables import *

def generate_fantasy_name(character_species="Human"):
    if character_species in name_profiles:
        profile = name_profiles[character_species]
        first_part = random.choice(profile["starts"])
        middle_part = random.choice(profile["middles"])
        last_part = random.choice(profile["endings"])
    else:
        first_part = random.choice(name_starts)
        middle_part = random.choice(name_middles)
        last_part = random.choice(name_endings)

    first_name = first_part + middle_part + last_part

    if character_species in surname_profiles:
        surname = random.choice(surname_profiles[character_species])
    else:
        surname = ""

    # Most characters get a surname/title, but not always.
    # This keeps the names from becoming too long every single time.
    include_surname = random.choice([True, True, True, False])

    if include_surname and surname != "":
        full_name = first_name + " " + surname
    else:
        full_name = first_name

    return full_name


def roll_ability_score():
    rolls = []

    for i in range(4):
        rolls.append(random.randint(1, 6))

    rolls.sort()

    best_three_rolls = rolls[1:]
    score = sum(best_three_rolls)

    return score

def roll_3d6_score():
    score = 0

    for i in range(3):
        score += random.randint(1, 6)

    return score


def roll_heroic_score():
    # Heroic method: 2d6 + 6.
    # This creates stronger adventurers and avoids very low scores.
    score = random.randint(1, 6) + random.randint(1, 6) + 6

    return score

def generate_point_buy_scores(character_class):
    # Automatic 27-point-buy spread.
    # Cost table:
    # 8 = 0, 9 = 1, 10 = 2, 11 = 3, 12 = 4,
    # 13 = 5, 14 = 7, 15 = 9
    #
    # 15 + 15 + 14 + 10 + 8 + 8 costs:
    # 9 + 9 + 7 + 2 + 0 + 0 = 27 points.
    point_buy_scores = [15, 15, 14, 10, 8, 8]

    ability_scores = {}
    priority_order = class_ability_priorities[character_class]

    for i in range(6):
        ability = priority_order[i]
        score = point_buy_scores[i]
        ability_scores[ability] = score

    return ability_scores

def generate_ability_scores(character_class, roll_method="4d6 Drop Lowest"):
    ability_scores = {}

    if roll_method == "Point Buy":
        return generate_point_buy_scores(character_class)

    # 3d6 Straight means roll in the fixed ability order.
    # This ignores class optimization and gives an old-school feel.
    if roll_method == "3d6 Straight":
        for ability in ability_order:
            ability_scores[ability] = roll_3d6_score()

        return ability_scores

    # Standard Array uses fixed scores, then assigns the best scores
    # according to the class's ability priorities.
    if roll_method == "Standard Array":
        rolled_scores = [15, 14, 13, 12, 10, 8]

    else:
        rolled_scores = []

        for i in range(6):
            if roll_method == "Heroic 2d6+6":
                rolled_scores.append(roll_heroic_score())
            else:
                rolled_scores.append(roll_ability_score())

        rolled_scores.sort(reverse=True)

    priority_order = class_ability_priorities[character_class]

    for i in range(6):
        ability = priority_order[i]
        score = rolled_scores[i]
        ability_scores[ability] = score

    return ability_scores


def apply_species_bonuses(ability_scores, character_species):
    bonuses = species_ability_bonuses[character_species]

    for ability, bonus in bonuses.items():
        ability_scores[ability] = ability_scores[ability] + bonus

    return ability_scores


def calculate_modifier(score):
    modifier = (score - 10) // 2

    return modifier


def format_bonus(number):
    if number >= 0:
        bonus_text = f"+{number}"
    else:
        bonus_text = str(number)

    return bonus_text

def calculate_proficiency_bonus(level):
    if level >= 17:
        proficiency_bonus = 6
    elif level >= 13:
        proficiency_bonus = 5
    elif level >= 9:
        proficiency_bonus = 4
    elif level >= 5:
        proficiency_bonus = 3
    else:
        proficiency_bonus = 2

    return proficiency_bonus


def calculate_saving_throws(character_class, ability_scores, proficiency_bonus):
    proficient_saves = class_saving_throw_proficiencies[character_class]
    saving_throws = {}

    for ability in ability_order:
        score = ability_scores[ability]
        modifier = calculate_modifier(score)

        if ability in proficient_saves:
            saving_throw_bonus = modifier + proficiency_bonus
        else:
            saving_throw_bonus = modifier

        saving_throws[ability] = saving_throw_bonus

    return saving_throws


def calculate_skills(character_class, ability_scores, proficiency_bonus):
    proficient_skills = class_skill_proficiencies[character_class]
    skills = {}

    for skill, ability in skill_ability_map.items():
        ability_score = ability_scores[ability]
        modifier = calculate_modifier(ability_score)

        if skill in proficient_skills:
            skill_bonus = modifier + proficiency_bonus
        else:
            skill_bonus = modifier

        skills[skill] = skill_bonus

    return skills

def calculate_hit_points(character_class, ability_scores, level=1):
    hit_die = class_hit_dice[character_class]
    constitution_score = ability_scores["Constitution"]
    constitution_modifier = calculate_modifier(constitution_score)

    # Level 1 gets the full hit die.
    hit_points = hit_die + constitution_modifier

    # Later levels use a simple average roll estimate.
    # Example: d10 average becomes 6, d8 average becomes 5.
    average_hit_points_per_level = (hit_die // 2) + 1

    for i in range(level - 1):
        hit_points += average_hit_points_per_level + constitution_modifier

    if hit_points < level:
        hit_points = level

    return hit_points


def calculate_armor_class(ability_scores):
    dexterity_score = ability_scores["Dexterity"]
    dexterity_modifier = calculate_modifier(dexterity_score)

    armor_class = 10 + dexterity_modifier

    return armor_class


def calculate_initiative(ability_scores):
    dexterity_score = ability_scores["Dexterity"]
    dexterity_modifier = calculate_modifier(dexterity_score)

    return dexterity_modifier


def calculate_speed(character_species):
    speed = species_speeds[character_species]

    return speed


def calculate_passive_perception(skills):
    passive_perception = 10 + skills["Perception"]

    return passive_perception


def calculate_weapon_attacks(character_class, ability_scores, proficiency_bonus):
    weapons = class_starting_weapons[character_class]
    weapon_attacks = {}

    for weapon_name in weapons:
        weapon = weapon_rules[weapon_name]
        ability = weapon["ability"]
        ability_score = ability_scores[ability]
        ability_modifier = calculate_modifier(ability_score)

        attack_bonus = ability_modifier + proficiency_bonus
        damage_bonus = ability_modifier

        weapon_attacks[weapon_name] = {
            "attack_bonus": attack_bonus,
            "damage": weapon["damage"],
            "damage_bonus": damage_bonus,
            "ability": ability
        }

    return weapon_attacks


def calculate_spellcasting(character_class, ability_scores, proficiency_bonus, level=1):
    if character_class not in spellcasting_classes:
        return None

    spellcasting_info = spellcasting_classes[character_class]
    spellcasting_ability = spellcasting_info["spellcasting_ability"]
    spellcasting_score = ability_scores[spellcasting_ability]
    spellcasting_modifier = calculate_modifier(spellcasting_score)

    spell_save_dc = 8 + proficiency_bonus + spellcasting_modifier
    spell_attack_bonus = proficiency_bonus + spellcasting_modifier
    spell_slot_text = get_spell_slot_text(character_class, level)
    spell_lists = get_sample_spell_list(character_class, level)

    character_spellcasting = {
        "spellcasting_ability": spellcasting_ability,
        "spell_save_dc": spell_save_dc,
        "spell_attack_bonus": spell_attack_bonus,
        "spell_slots": spell_slot_text,
        "cantrips": spell_lists["cantrips"],
        "level_1_spells": spell_lists["level_1_spells"],
        "higher_level_spells": spell_lists["higher_level_spells"]
    }

    return character_spellcasting

def get_spell_slot_text(character_class, level):
    if character_class not in class_spell_progression_type:
        return "No spell slots."

    progression_type = class_spell_progression_type[character_class]
    progression_table = spell_slot_progression[progression_type]

    return progression_table.get(level, "No spell slot data.")

def get_highest_spell_level(character_class, level):
    if character_class not in class_spell_progression_type:
        return 0

    progression_type = class_spell_progression_type[character_class]

    if progression_type == "full":
        if level >= 17:
            return 9
        elif level >= 15:
            return 8
        elif level >= 13:
            return 7
        elif level >= 11:
            return 6
        elif level >= 9:
            return 5
        elif level >= 7:
            return 4
        elif level >= 5:
            return 3
        elif level >= 3:
            return 2
        elif level >= 1:
            return 1

    elif progression_type == "half":
        if level >= 17:
            return 5
        elif level >= 13:
            return 4
        elif level >= 9:
            return 3
        elif level >= 5:
            return 2
        elif level >= 2:
            return 1
        else:
            return 0

    elif progression_type == "warlock":
        if level >= 9:
            return 5
        elif level >= 7:
            return 4
        elif level >= 5:
            return 3
        elif level >= 3:
            return 2
        elif level >= 1:
            return 1

    return 0

def get_sample_spell_list(character_class, level):
    if character_class not in spell_examples_by_class:
        return {
            "cantrips": [],
            "level_1_spells": [],
            "higher_level_spells": []
        }

    spell_table = spell_examples_by_class[character_class]
    highest_spell_level = get_highest_spell_level(character_class, level)

    cantrips = list(spell_table.get("cantrips", []))
    cantrips = cantrips[:MAX_CANTRIPS_TO_SHOW]

    if highest_spell_level >= 1:
        level_1_spells = list(spell_table.get(1, []))
        level_1_spells = level_1_spells[:MAX_LEVEL_1_SPELLS_TO_SHOW]
    else:
        level_1_spells = []

    higher_level_spells = []

    for spell_level in range(2, highest_spell_level + 1):
        spells_for_level = spell_table.get(spell_level, [])

        for spell in spells_for_level:
            higher_level_spells.append(f"Level {spell_level}: {spell}")

    higher_level_spells = higher_level_spells[:MAX_HIGHER_LEVEL_SPELLS_TO_SHOW]

    return {
        "cantrips": cantrips,
        "level_1_spells": level_1_spells,
        "higher_level_spells": higher_level_spells
    }

def generate_starting_equipment(character_class):
    equipment = class_starting_equipment[character_class]

    return equipment

def generate_class_features(character_class, level=1):
    if character_class not in class_features_by_level:
        return class_features[character_class]

    features = []

    level_feature_table = class_features_by_level[character_class]

    for feature_level, feature_list in level_feature_table.items():
        if level >= feature_level:
            for feature in feature_list:
                features.append(feature)

    return features

def generate_subclass(character_class, level, selected_subclass="Random"):
    if character_class not in class_subclasses:
        return "None"

    subclass_level = class_subclass_levels.get(character_class, 99)

    if level < subclass_level:
        return "None"

    available_subclasses = class_subclasses[character_class]

    if selected_subclass != "Random" and selected_subclass in available_subclasses:
        return selected_subclass

    return random.choice(available_subclasses)

def generate_subclass_features(subclass_name, level):
    if subclass_name == "None":
        return []

    if subclass_name not in subclass_features_by_level:
        return []

    subclass_features = []
    feature_table = subclass_features_by_level[subclass_name]

    for feature_level, feature_list in feature_table.items():
        if level >= feature_level:
            for feature in feature_list:
                subclass_features.append(feature)

    return subclass_features

def generate_roleplay_traits():
    roleplay_traits = {
        "Personality Trait": random.choice(personality_traits),
        "Ideal": random.choice(ideals),
        "Bond": random.choice(bonds),
        "Flaw": random.choice(flaws)
    }

    return roleplay_traits

def generate_character_data(selected_class="Random", selected_species="Random", selected_alignment="Random", selected_sex="Random", selected_background="Random", selected_level="1", selected_roll_method="4d6 Drop Lowest", selected_subclass="Random"):
    if selected_species == "Random":
        character_species = random.choice(species)
    else:
        character_species = selected_species

    character_name = generate_fantasy_name(character_species)

    if selected_class == "Random":
        character_class = random.choice(classes)
    else:
        character_class = selected_class

    if selected_background == "Random":
        character_background = random.choice(backgrounds)
    else:
        character_background = selected_background

    if selected_alignment == "Random":
        character_alignment = random.choice(alignments)
    else:
        character_alignment = selected_alignment

    if selected_sex == "Random":
        character_sex = random.choice(sex_options)
    else:
        character_sex = selected_sex

    if str(selected_level).isdigit():
        character_level = int(selected_level)
    else:
        character_level = 1    
            
    if selected_roll_method in roll_method_options:
        character_roll_method = selected_roll_method
    else:
        character_roll_method = "4d6 Drop Lowest"

    raw_ability_scores = generate_ability_scores(character_class, character_roll_method)
    character_ability_scores = apply_species_bonuses(raw_ability_scores, character_species)
    proficiency_bonus = calculate_proficiency_bonus(character_level)
    character_saving_throws = calculate_saving_throws(character_class, character_ability_scores, proficiency_bonus)
    character_skills = calculate_skills(character_class, character_ability_scores, proficiency_bonus)
    character_hit_points = calculate_hit_points(character_class, character_ability_scores, character_level)
    character_armor_class = calculate_armor_class(character_ability_scores)
    character_initiative = calculate_initiative(character_ability_scores)
    character_speed = calculate_speed(character_species)
    character_passive_perception = calculate_passive_perception(character_skills)
    character_weapon_attacks = calculate_weapon_attacks(character_class, character_ability_scores, proficiency_bonus)
    character_spellcasting = calculate_spellcasting(
        character_class,
        character_ability_scores,
        proficiency_bonus,
        character_level
    )
    character_equipment = generate_starting_equipment(character_class)
    character_class_features = generate_class_features(character_class, character_level)
    character_subclass = generate_subclass(character_class, character_level, selected_subclass)
    character_subclass_features = generate_subclass_features(character_subclass, character_level)
    character_roleplay_traits = generate_roleplay_traits()

    character_data = {
        "name": character_name,
        "species": character_species,
        "class": character_class,
        "subclass": character_subclass,
        "background": character_background,
        "alignment": character_alignment,
        "sex": character_sex,
        "level": character_level,
        "roll_method": character_roll_method,
        "proficiency_bonus": proficiency_bonus,
        "ability_scores": character_ability_scores,
        "saving_throws": character_saving_throws,
        "skills": character_skills,
        "hit_points": character_hit_points,
        "armor_class": character_armor_class,
        "initiative": character_initiative,
        "speed": character_speed,
        "passive_perception": character_passive_perception,
        "weapon_attacks": character_weapon_attacks,
        "spellcasting": character_spellcasting,
        "equipment": character_equipment,
        "class_features": character_class_features,
        "subclass_features": character_subclass_features,
        "roleplay_traits": character_roleplay_traits
    }

    return character_data

def reroll_ability_scores_for_character(character_data, roll_method=None):
    character_class = character_data["class"]
    character_species = character_data["species"]
    character_level = character_data["level"]

    if roll_method is None:
        roll_method = character_data.get("roll_method", "4d6 Drop Lowest")

    if roll_method not in roll_method_options:
        roll_method = "4d6 Drop Lowest"

    old_ability_scores = dict(character_data["ability_scores"])

    # Try a few times so the user actually sees a change.
    # It is possible, though unlikely, for random rolls to produce the same final scores.
    new_ability_scores = old_ability_scores

    for attempt in range(10):
        raw_ability_scores = generate_ability_scores(character_class, roll_method)
        new_ability_scores = apply_species_bonuses(raw_ability_scores, character_species)

        if new_ability_scores != old_ability_scores:
            break

    proficiency_bonus = calculate_proficiency_bonus(character_level)
    new_saving_throws = calculate_saving_throws(
        character_class,
        new_ability_scores,
        proficiency_bonus
    )
    new_skills = calculate_skills(
        character_class,
        new_ability_scores,
        proficiency_bonus
    )

    character_data["roll_method"] = roll_method
    character_data["ability_scores"] = new_ability_scores
    character_data["proficiency_bonus"] = proficiency_bonus
    character_data["saving_throws"] = new_saving_throws
    character_data["skills"] = new_skills
    character_data["hit_points"] = calculate_hit_points(
        character_class,
        new_ability_scores,
        character_level
    )
    character_data["armor_class"] = calculate_armor_class(new_ability_scores)
    character_data["initiative"] = calculate_initiative(new_ability_scores)
    character_data["passive_perception"] = calculate_passive_perception(new_skills)
    character_data["weapon_attacks"] = calculate_weapon_attacks(
        character_class,
        new_ability_scores,
        proficiency_bonus
    )
    character_data["spellcasting"] = calculate_spellcasting(
        character_class,
        new_ability_scores,
        proficiency_bonus,
        character_level
    )

    return character_data

def reroll_roleplay_traits_for_character(character_data):
    character_data["roleplay_traits"] = generate_roleplay_traits()

    return character_data

def recalculate_character_after_level_change(character_data):
    """
    Recalculate level-dependent values after changing a character's level.

    This keeps the same:
    - name
    - class
    - species
    - background
    - alignment
    - sex
    - ability scores
    - roleplay traits

    But updates:
    - proficiency bonus
    - saving throws
    - skills
    - hit points
    - weapon attacks
    - spellcasting
    - class features
    - subclass/subclass features
    """
    character_class = character_data["class"]
    character_species = character_data["species"]
    character_level = character_data["level"]
    ability_scores = character_data["ability_scores"]

    proficiency_bonus = calculate_proficiency_bonus(character_level)

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
    character_data["speed"] = calculate_speed(character_species)
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
    character_data["class_features"] = generate_class_features(
        character_class,
        character_level
    )

    selected_subclass = character_data.get("subclass", "Random")
    character_data["subclass"] = generate_subclass(
        character_class,
        character_level,
        selected_subclass
    )
    character_data["subclass_features"] = generate_subclass_features(
        character_data.get("subclass", "None"),
        character_level
    )

    return character_data
