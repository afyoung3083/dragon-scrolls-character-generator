# ============================================================
# PORTRAIT TOOLS
# Reusable image helper functions for loading, saving,
# copying, and resizing portrait images.
#
# This file should NOT create GUI widgets.
# This file should NOT show message boxes.
# This file should NOT directly change GUI state.
# ============================================================

from PIL import Image, ImageGrab


def get_clipboard_image():
    clipboard_content = ImageGrab.grabclipboard()

    if clipboard_content is None:
        return None, "No image was found on the clipboard."

    if isinstance(clipboard_content, list):
        return None, "The clipboard contains a file path, not a copied image."

    return clipboard_content.copy(), None


def load_portrait_image_from_file(file_path):
    portrait_image = Image.open(file_path).copy()

    return portrait_image


def save_portrait_image_to_file(portrait_image, portrait_file_path):
    if portrait_image is None:
        return None

    image_to_save = portrait_image.copy()
    image_to_save.save(portrait_file_path, "PNG")

    return portrait_file_path


def make_resized_portrait_copy(portrait_image, max_width, max_height):
    if portrait_image is None:
        return None

    resized_image = portrait_image.copy()
    resized_image.thumbnail((max_width, max_height))

    return resized_image
