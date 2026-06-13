# ============================================================
# PDF EXPORTER
# Builds printable character sheet PDFs.
#
# This file should NOT create GUI widgets.
# This file should NOT open save dialogs.
# This file should only build a PDF from character data,
# portrait image data, and a destination PDF path.
# ============================================================

import os
import tempfile
import textwrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas

from data_tables import *
from character_generator import *
from text_generator import *

def strip_section_title(text):
    lines = text.splitlines()

    if len(lines) > 0 and lines[0].startswith("==="):
        lines = lines[1:]

    while len(lines) > 0 and lines[0].strip() == "":
        lines = lines[1:]

    return "\n".join(lines)

def build_character_sheet_pdf(pdf_path, character_data, portrait_image=None):
    if character_data is None:
        return

    page_width, page_height = letter

    c = pdf_canvas.Canvas(pdf_path, pagesize=letter)

    temp_image_path = None

    # ------------------------------------------------------------
    # Small drawing helpers used only inside this PDF function.
    # ------------------------------------------------------------
    def draw_section_box(title, x, y, width, height):
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.rect(x, y, width, height)

        c.setFillColor(colors.lightgrey)
        c.rect(x, y + height - 14, width, 14, fill=1, stroke=0)

        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(x + 4, y + height - 10, title)

    def draw_wrapped_text(text, x, y, width, bottom_limit, font_size=6.5, line_height=8):
        c.setFont("Helvetica", font_size)
        c.setFillColor(colors.black)

        approximate_character_width = font_size * 0.52
        max_characters = int(width / approximate_character_width)

        if max_characters < 10:
            max_characters = 10

        lines = str(text).split("\n")

        for line in lines:
            line = line.strip()

            if line == "":
                y -= line_height / 2
                continue

            wrapped_lines = textwrap.wrap(line, width=max_characters)

            if len(wrapped_lines) == 0:
                wrapped_lines = [""]

            for wrapped_line in wrapped_lines:
                if y < bottom_limit:
                    c.drawString(x, y, "...")
                    return y

                c.drawString(x, y, wrapped_line)
                y -= line_height

        return y

    def draw_label_value(label, value, x, y, label_width=55):
        c.setFont("Helvetica-Bold", 6.5)
        c.drawString(x, y, label)

        c.setFont("Helvetica", 6.5)
        c.drawString(x + label_width, y, str(value))

    def draw_ability_box(ability_name, score, modifier_text, x, y, width, height):
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.rect(x, y, width, height)

        c.setFillColor(colors.lightgrey)
        c.rect(x, y + height - 12, width, 12, fill=1, stroke=0)

        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 6)
        c.drawCentredString(x + width / 2, y + height - 8, ability_name.upper())

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(x + width / 2, y + 18, str(score))

        c.setFont("Helvetica", 9)
        c.drawCentredString(x + width / 2, y + 6, modifier_text)

    def draw_basic_text_box(title, body_text, x, y, width, height, font_size=6.5):
        draw_section_box(title, x, y, width, height)
        draw_wrapped_text(
            body_text,
            x + 5,
            y + height - 22,
            width - 10,
            y + 6,
            font_size=font_size
        )

    def draw_writable_box(label, x, y, width, height):
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.rect(x, y, width, height)

        c.setFont("Helvetica-Bold", 5.5)
        c.drawCentredString(x + width / 2, y + height - 8, label)

    # ------------------------------------------------------------
    # Page geometry.
    # ------------------------------------------------------------
    left_x = 24
    ability_x = 24
    center_x = 114
    right_x = 394

    ability_width = 76
    center_width = 270
    right_width = 194

    # ------------------------------------------------------------
    # Header block.
    # ------------------------------------------------------------
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(24, 730, 564, 38)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(32, 752, character_data["name"])

    c.setFont("Helvetica", 7)
    header_line = (
        f"Level {character_data['level']} "
        f"{character_data['species']} "
        f"{character_data['class']}   |   "
        f"Background: {character_data['background']}   |   "
        f"Alignment: {character_data['alignment']}   |   "
        f"Sex: {character_data.get('sex', 'Unknown')}"
    )
    c.drawString(32, 738, header_line)

    # ------------------------------------------------------------
    # Ability score boxes down the left side.
    # ------------------------------------------------------------
    ability_abbreviations = {
        "Strength": "STR",
        "Dexterity": "DEX",
        "Constitution": "CON",
        "Intelligence": "INT",
        "Wisdom": "WIS",
        "Charisma": "CHA"
    }

    ability_scores = character_data["ability_scores"]

    ability_top_y = 674
    ability_box_height = 45
    ability_gap = 5

    for index, ability in enumerate(ability_order):
        score = ability_scores[ability]
        modifier = calculate_modifier(score)
        modifier_text = format_bonus(modifier)

        box_y = ability_top_y - (index * (ability_box_height + ability_gap))

        draw_ability_box(
            ability_abbreviations[ability],
            score,
            modifier_text,
            ability_x,
            box_y,
            ability_width,
            ability_box_height
        )

    # ------------------------------------------------------------
    # Skills and saving throws.
    # ------------------------------------------------------------
    draw_section_box("Saving Throws & Skills", left_x, 24, 76, 390)

    y = 398
    c.setFont("Helvetica-Bold", 6)
    c.drawString(left_x + 5, y, "SAVES")
    y -= 8

    for ability in ability_order:
        save_bonus = character_data["saving_throws"][ability]
        save_text = format_bonus(save_bonus)

        if ability in class_saving_throw_proficiencies[character_data["class"]]:
            proficient_marker = "*"
        else:
            proficient_marker = ""

        ability_short = ability_abbreviations[ability]
        c.setFont("Helvetica", 5.8)
        c.drawString(left_x + 5, y, f"{ability_short}: {save_text}{proficient_marker}")
        y -= 7

    y -= 4
    c.setFont("Helvetica-Bold", 6)
    c.drawString(left_x + 5, y, "SKILLS")
    y -= 8

    for skill, skill_bonus in character_data["skills"].items():
        skill_text = format_bonus(skill_bonus)
        related_ability = skill_ability_map[skill]
        ability_short = ability_abbreviations[related_ability]

        if skill in class_skill_proficiencies[character_data["class"]]:
            proficient_marker = "*"
        else:
            proficient_marker = ""

        c.setFont("Helvetica", 5.3)
        c.drawString(left_x + 5, y, f"{skill[:13]} ({ability_short}) {skill_text}{proficient_marker}")
        y -= 6.5

    c.setFont("Helvetica", 5)
    c.drawString(left_x + 5, 31, "* proficient")

    # ------------------------------------------------------------
    # Center column: combat, attacks, spells, equipment.
    # ------------------------------------------------------------
    # Combat box with writable hit point and death save areas.
    draw_section_box("Combat", center_x, 632, center_width, 87)

    draw_label_value("Max HP:", character_data["hit_points"], center_x + 6, 699, label_width=45)
    draw_label_value("AC:", character_data["armor_class"], center_x + 98, 699, label_width=20)
    draw_label_value("Init:", format_bonus(character_data["initiative"]), center_x + 148, 699, label_width=25)
    draw_label_value("Speed:", f"{character_data['speed']} ft.", center_x + 205, 699, label_width=35)

    draw_label_value("Prof:", format_bonus(character_data["proficiency_bonus"]), center_x + 6, 686, label_width=35)
    draw_label_value("Passive Perception:", character_data["passive_perception"], center_x + 98, 686, label_width=95)

    draw_writable_box("Current HP", center_x + 6, 642, 72, 32)
    draw_writable_box("Temp HP", center_x + 86, 642, 72, 32)

    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(center_x + 166, 642, 98, 32)

    c.setFont("Helvetica-Bold", 5.5)
    c.drawCentredString(center_x + 215, 666, "Death Saves")

    c.setFont("Helvetica", 5.2)
    c.drawString(center_x + 172, 655, "Successes:")
    c.drawString(center_x + 172, 645, "Failures:")

    for i in range(3):
        c.circle(center_x + 218 + (i * 11), 657, 3)
        c.circle(center_x + 218 + (i * 11), 647, 3)

    attacks_text = ""
    for weapon_name, weapon_info in character_data["weapon_attacks"].items():
        attack_bonus_text = format_bonus(weapon_info["attack_bonus"])
        damage_bonus_text = format_bonus(weapon_info["damage_bonus"])
        attacks_text += f"{weapon_name}: {attack_bonus_text} to hit, {weapon_info['damage']} {damage_bonus_text}\n"

    draw_basic_text_box(
        "Attacks",
        attacks_text,
        center_x,
        510,
        center_width,
        112,
        font_size=7
    )

    spells_text = strip_section_title(generate_spells_text(character_data))

    draw_basic_text_box(
        "Spells",
        spells_text,
        center_x,
        375,
        center_width,
        125,
        font_size=6.5
    )

    equipment_text = strip_section_title(generate_equipment_text(character_data))

    draw_basic_text_box(
        "Equipment",
        equipment_text,
        center_x,
        24,
        center_width,
        341,
        font_size=6.7
    )

    # ------------------------------------------------------------
    # Right column: portrait, roleplay, features.
    # ------------------------------------------------------------
    draw_section_box("Portrait", right_x, 535, right_width, 184)

    if portrait_image is not None:
        temp_image_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        temp_image_path = temp_image_file.name
        temp_image_file.close()

        portrait_image.save(temp_image_path)

        c.drawImage(
            temp_image_path,
            right_x + 9,
            548,
            width=right_width - 18,
            height=156,
            preserveAspectRatio=True,
            anchor="c"
        )
    else:
        c.setFont("Helvetica", 7)
        c.drawString(right_x + 10, 620, "No portrait saved.")

    roleplay_traits = character_data["roleplay_traits"]

    roleplay_text = ""
    roleplay_text += f"Personality: {roleplay_traits['Personality Trait']}\n\n"
    roleplay_text += f"Ideal: {roleplay_traits['Ideal']}\n\n"
    roleplay_text += f"Bond: {roleplay_traits['Bond']}\n\n"
    roleplay_text += f"Flaw: {roleplay_traits['Flaw']}"

    draw_basic_text_box(
        "Personality / Ideals / Bonds / Flaws",
        roleplay_text,
        right_x,
        315,
        right_width,
        210,
        font_size=6.2
    )

    features_text = strip_section_title(generate_features_text(character_data))

    draw_basic_text_box(
        "Features & Traits",
        features_text,
        right_x,
        24,
        right_width,
        281,
        font_size=6.7
    )

    # ------------------------------------------------------------
    # Finish the PDF.
    # ------------------------------------------------------------
    c.showPage()
    c.save()

    if temp_image_path is not None:
        os.remove(temp_image_path)
