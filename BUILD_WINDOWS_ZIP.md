# Build Windows Test ZIP

This checklist is for preparing a simple Windows test package for Dragon Scrolls Character Generator.

This is not a full Windows installer yet. It is a clean ZIP package that lets a Windows tester unzip the folder and double-click the launcher.

## Goal

Create one folder that contains everything a Windows tester needs to run Dragon Scrolls as a Python app.

The tester should be able to:

1. Download the ZIP.
2. Unzip it.
3. Open the unzipped folder.
4. Double-click `Launch Dragon Scrolls.bat`.

## Package Folder Name

Use this folder name for the test package:

```text
DragonScrolls_Windows_Test_Package
```

When making a release ZIP, use a versioned ZIP name such as:

```text
DragonScrolls_Windows_Test_Package_v0.1.1.zip
```

## Required Files

Copy these files into `DragonScrolls_Windows_Test_Package`:

```text
Launch Dragon Scrolls.bat
dnd_gui_character_generator_v2.py
data_tables.py
character_generator.py
text_generator.py
pdf_exporter.py
theme.py
file_manager.py
portrait_tools.py
header_art.py
dragon_scrolls_app_icon.ico
requirements.txt
README.md
LICENSE
```

## Optional Files

These files are useful for GitHub, development, or documentation, but they are not required for the basic Windows test package:

```text
CHANGELOG.md
ROADMAP.md
screenshots/
.github/
.gitignore
smoke_test.py
pdf_smoke_test.py
run_all_tests.py
```

If `run_all_tests.py` exists, include it in developer builds. For a simple public tester ZIP, it is optional.

## Do Not Include

Do not include these files or folders in the ZIP:

```text
__pycache__/
*.pyc
dragon_scrolls_settings.json
JSON-*_character.json
TXT-*_character.txt
PDF-*_character.pdf
PNG-*_portrait.png
```

These are local cache files, settings files, or generated character files.

## Build Steps

1. Create a clean folder named:

```text
DragonScrolls_Windows_Test_Package
```

2. Copy the required files into that folder.

3. Confirm the launcher file is named exactly:

```text
Launch Dragon Scrolls.bat
```

4. Open the package folder.

5. Double-click:

```text
Launch Dragon Scrolls.bat
```

6. Confirm the app opens.

7. In the app, test the basics:

```text
Generate a character
Open the dice roller
Roll d20
Save a character
Load a saved character
Export or open a PDF
```

8. Close the app.

9. Delete any test character files created during testing unless you intentionally want sample files in the package.

10. Right-click the `DragonScrolls_Windows_Test_Package` folder and choose:

```text
Send to > Compressed (zipped) folder
```

11. Rename the ZIP to a versioned name, such as:

```text
DragonScrolls_Windows_Test_Package_v0.1.1.zip
```

## Tester Instructions

Include these instructions when sharing the ZIP:

```text
This is an early Windows test package for Dragon Scrolls Character Generator.

To run it:

1. Download the ZIP.
2. Unzip it.
3. Open the unzipped folder.
4. Double-click Launch Dragon Scrolls.bat.

If it does not open, install Python 3.12 or newer, then open Command Prompt in the folder and run:

pip install -r requirements.txt

Then double-click Launch Dragon Scrolls.bat again.
```

## Release Checklist

Before sharing the ZIP, confirm:

```text
[ ] App opens from Launch Dragon Scrolls.bat
[ ] Generate button works
[ ] Dice roller opens
[ ] A d20 roll works
[ ] Save works
[ ] Load Character works
[ ] PDF export works
[ ] No __pycache__ folder is included
[ ] No personal saved characters are included
[ ] README.md is included
[ ] LICENSE is included
```

## Future Improvement

A later sprint can replace this ZIP workflow with a real Windows executable or installer using a packaging tool such as PyInstaller.

For now, this ZIP package keeps the release process simple and easy to test.
