# Dragon Scrolls Character Generator

Dragon Scrolls is a retro fantasy tabletop RPG character generator built with Python and Tkinter.

It creates fantasy RPG characters with:

* species, class, subclass, background, alignment, and level
* ability scores and combat stats
* spells and class features
* roleplay traits
* portrait image prompts
* saved character loading, searching, sorting, and editing
* printable PDF character sheets
* a built-in dice roller

## Portrait Images and AI Image Prompts

Dragon Scrolls does not generate portrait images by itself.

Instead, it creates a detailed portrait prompt for each character. You can copy that prompt and paste it into your favorite image generator, such as ChatGPT, Grok, Copilot, Gemini, or another image generation tool.

The intended portrait workflow is:

1. Generate a character in Dragon Scrolls.
2. Click the portrait prompt/copy prompt option.
3. Paste the prompt into your preferred image generator.
4. Generate the character portrait outside Dragon Scrolls.
5. Save the image as a PNG, JPG, or similar image file.
6. Add that image back into Dragon Scrolls as the character portrait.

You can also skip AI image generation completely and use any normal image file you already have, such as a PNG or JPG character portrait.

Dragon Scrolls supports adding portrait images so they can be saved with the character and included in previews or exports.

## Project Roadmap and Changelog

Dragon Scrolls is under active development.

See the [ROADMAP.md](ROADMAP.md) file for planned features, future ideas, and the current project direction.

See the [CHANGELOG.md](CHANGELOG.md) file for version history and release notes.

## Status

This project is currently an early hobby release.

It works on Windows with Python 3.12, but it is still under active development.

## Screenshots

### Main Character Generator

![Main Character Generator](screenshots/screenshots_main_window.png)

### Saved Character Browser

![Character Portrait](screenshots/screenshots_character_portrait.png)

### Dice Roller

![Dice Roller](screenshots/screenshots_dice_roller.png)

## How to Run

### Windows Quick Start

This project is still a Python app, not a finished Windows installer yet.

For the easiest first run on Windows:

1. Download this project from GitHub.
2. Unzip the downloaded folder.
3. Open the unzipped project folder.
4. Double-click:

```text
Launch Dragon Scrolls.bat
```

The batch launcher opens the Dragon Scrolls GUI without needing to open IDLE.

If the app does not open, install Python 3.12 or newer, then install the required packages from inside the project folder:

```bash
pip install -r requirements.txt
```

After that, double-click `Launch Dragon Scrolls.bat` again.

### Developer / Command-Line Run

You can also run the app from a terminal.

1. Install Python 3.12 or newer.
2. Download this project.
3. Open the project folder in a terminal.
4. Install the required packages:

```bash
pip install -r requirements.txt
```

5. Run the app:

```bash
python dnd_gui_character_generator_v2.py
```

## Required Python Packages

This project uses:

```bash
pip install pillow reportlab
```

Tkinter is included with most standard Python installations on Windows.

## Main Features

### Character Generator

Dragon Scrolls can generate and edit fantasy RPG characters with class, subclass, species, background, alignment, level, ability scores, combat stats, spells, equipment, features, and roleplay traits.

### Saved Character Browser

Saved characters can be loaded, searched, sorted, refreshed, edited, and deleted from inside the app.

### PDF Export

The app can export a printable character sheet as a PDF.

### Portrait Support

The app can create a detailed portrait prompt, copy that prompt for use in an external image generator, and attach a saved PNG/JPG portrait image to the character.

### Dice Roller

The built-in dice roller supports common dice expressions such as:

```text
1d20
1d20+5
2d6+1d4+3
8d6
4d6 Drop Lowest
1d20 Advantage
1d20 Disadvantage
```

## Disclaimer

Dragon Scrolls is an unofficial fantasy tabletop RPG tool.

It is not affiliated with, endorsed by, sponsored by, or approved by Wizards of the Coast, Hasbro, or any official tabletop RPG publisher.

This project does not include official Dungeons & Dragons logos, trade dress, proprietary setting material, or official artwork.

Users are responsible for making sure any images they import into Dragon Scrolls are images they have the right to use.

## Feedback

Feedback, bugs, and feature ideas are welcome.

Planned future improvements include:

* better packaging as a Windows app
* a cleaner installer
* more editing tools
* better dice roller visuals
* campaign and party manager features
* more export options
* mobile or web versions if there is enough interest

## License

This project is released under the MIT License. See the `LICENSE` file for details.
