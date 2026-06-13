# ============================================================
# HEADER ART
# Pixel-art torch and title-banner drawing helpers.
#
# This file should NOT create the main window.
# This file should NOT run the Tkinter event loop.
# This file should NOT generate characters or save files.
# ============================================================

import random

from PIL import Image, ImageDraw, ImageTk

from theme import *

def draw_pixel_block(draw, x, y, size, color):
    draw.rectangle(
        [x * size, y * size, (x + 1) * size - 1, (y + 1) * size - 1],
        fill=color
    )

def create_pixel_torch_frame(frame_number):
    pixel_size = 4
    grid_width = 16
    grid_height = 20

    image = Image.new(
        "RGBA",
        (grid_width * pixel_size, grid_height * pixel_size),
        (0, 0, 0, 0)
    )
    draw = ImageDraw.Draw(image)

    brown_dark = "#5a3a22"
    brown_light = "#8b5a2b"
    metal = "#999999"
    metal_dark = "#666666"
    red = "#ff5a1f"
    orange = "#ff9a1f"
    yellow = "#ffd84d"
    pale_yellow = "#fff2a8"

    # Wall bracket
    for x, y in [(3, 11), (4, 11), (5, 11), (4, 12), (5, 12), (6, 12)]:
        draw_pixel_block(draw, x, y, pixel_size, metal)

    for x, y in [(3, 12), (4, 10), (5, 10)]:
        draw_pixel_block(draw, x, y, pixel_size, metal_dark)

    # Torch handle
    for y in range(8, 17):
        draw_pixel_block(draw, 8, y, pixel_size, brown_dark)
        draw_pixel_block(draw, 9, y, pixel_size, brown_light)

    # Torch head
    for x, y in [(7, 7), (8, 7), (9, 7), (10, 7), (8, 6), (9, 6)]:
        draw_pixel_block(draw, x, y, pixel_size, metal)

    # Flicker variations
    flame_frames = [
        [
            (8, 5, red), (9, 5, orange),
            (7, 4, orange), (8, 4, yellow), (9, 4, orange), (10, 4, red),
            (8, 3, yellow), (9, 3, pale_yellow),
            (8, 2, yellow)
        ],
        [
            (8, 5, orange), (9, 5, red),
            (7, 4, red), (8, 4, orange), (9, 4, yellow), (10, 4, orange),
            (7, 3, orange), (8, 3, yellow), (9, 3, pale_yellow),
            (8, 2, pale_yellow)
        ],
        [
            (8, 5, red), (9, 5, orange),
            (7, 4, orange), (8, 4, yellow), (9, 4, pale_yellow), (10, 4, yellow),
            (8, 3, orange), (9, 3, yellow),
            (9, 2, pale_yellow)
        ],
        [
            (8, 5, orange), (9, 5, yellow),
            (7, 4, red), (8, 4, orange), (9, 4, yellow), (10, 4, orange),
            (8, 3, yellow), (9, 3, pale_yellow),
            (7, 2, orange), (8, 2, yellow)
        ]
    ]

    for x, y, color in flame_frames[frame_number]:
        draw_pixel_block(draw, x, y, pixel_size, color)

    return image

def build_torch_animation_frames():
    left_torch_frames = []
    right_torch_frames = []

    for i in range(4):
        torch_image = create_pixel_torch_frame(i)

        left_photo = ImageTk.PhotoImage(torch_image)
        right_photo = ImageTk.PhotoImage(torch_image.copy())

        left_torch_frames.append(left_photo)
        right_torch_frames.append(right_photo)

    return left_torch_frames, right_torch_frames

def draw_pixel_rect(canvas, x, y, width, height, color, tag="panel_bg"):
    canvas.create_rectangle(
        x,
        y,
        x + width,
        y + height,
        fill=color,
        outline="",
        tags=tag
    )

def draw_top_panel_background(
    top_panel_canvas,
    title_shadow_item,
    title_text_item,
    left_torch_item,
    right_torch_item,
    event=None
):
    top_panel_canvas.delete("panel_bg")

    canvas_width = top_panel_canvas.winfo_width()
    canvas_height = top_panel_canvas.winfo_height()

    if canvas_width <= 1:
        canvas_width = 1100

    if canvas_height <= 1:
        canvas_height = 140

    pixel = 4

    # Mortar background
    draw_pixel_rect(
        top_panel_canvas,
        0,
        0,
        canvas_width,
        canvas_height,
        PIXEL_MORTAR_COLOR
    )

    # Outer pixel border
    draw_pixel_rect(top_panel_canvas, 0, 0, canvas_width, pixel, COLOR_GOLD)
    draw_pixel_rect(top_panel_canvas, 0, canvas_height - pixel, canvas_width, pixel, COLOR_GOLD)
    draw_pixel_rect(top_panel_canvas, 0, 0, pixel, canvas_height, COLOR_GOLD)
    draw_pixel_rect(top_panel_canvas, canvas_width - pixel, 0, pixel, canvas_height, COLOR_GOLD)

    # Inner red/dark border
    draw_pixel_rect(top_panel_canvas, pixel, pixel, canvas_width - (2 * pixel), pixel, COLOR_RED_DARK)
    draw_pixel_rect(top_panel_canvas, pixel, canvas_height - (2 * pixel), canvas_width - (2 * pixel), pixel, COLOR_RED_DARK)
    draw_pixel_rect(top_panel_canvas, pixel, pixel, pixel, canvas_height - (2 * pixel), COLOR_RED_DARK)
    draw_pixel_rect(top_panel_canvas, canvas_width - (2 * pixel), pixel, pixel, canvas_height - (2 * pixel), COLOR_RED_DARK)

    # Draw chunky pixel-stone blocks.
    # The fixed seed makes the stone pattern stable instead of flickering every redraw.
    rng = random.Random(f"pixel-stone-{canvas_width}-{canvas_height}")

    left_margin = 12
    right_margin = 12
    top_margin = 12
    bottom_margin = 12

    y = top_margin

    while y < canvas_height - bottom_margin - 16:
        block_height = rng.choice([16, 20, 24])
        x = left_margin

        while x < canvas_width - right_margin - 24:
            block_width = rng.choice([44, 52, 60, 68, 76])

            if x + block_width > canvas_width - right_margin:
                block_width = canvas_width - right_margin - x

            if block_width < 24:
                break

            stone_color = rng.choice(PIXEL_STONE_COLORS)

            # Main block
            draw_pixel_rect(top_panel_canvas, x, y, block_width, block_height, stone_color)

            # Pixel outline
            draw_pixel_rect(top_panel_canvas, x, y, block_width, pixel, PIXEL_STONE_OUTLINE)
            draw_pixel_rect(top_panel_canvas, x, y + block_height - pixel, block_width, pixel, PIXEL_STONE_OUTLINE)
            draw_pixel_rect(top_panel_canvas, x, y, pixel, block_height, PIXEL_STONE_OUTLINE)
            draw_pixel_rect(top_panel_canvas, x + block_width - pixel, y, pixel, block_height, PIXEL_STONE_OUTLINE)

            # Highlight and shadow
            draw_pixel_rect(
                top_panel_canvas,
                x + pixel,
                y + pixel,
                block_width - (2 * pixel),
                pixel,
                PIXEL_STONE_HIGHLIGHT
            )

            draw_pixel_rect(
                top_panel_canvas,
                x + pixel,
                y + block_height - (2 * pixel),
                block_width - (2 * pixel),
                pixel,
                PIXEL_STONE_SHADOW
            )

            # Small pixel cracks
            if rng.random() < 0.45:
                crack_x = x + rng.choice([8, 12, 16, 20])
                crack_y = y + rng.choice([8, 12])

                for i in range(rng.choice([2, 3, 4])):
                    draw_pixel_rect(
                        top_panel_canvas,
                        crack_x + (i * pixel),
                        crack_y + (i * pixel),
                        pixel,
                        pixel,
                        PIXEL_STONE_OUTLINE
                    )

            # Small chips
            if rng.random() < 0.30:
                chip_x = x + block_width - rng.choice([8, 12, 16])
                chip_y = y + rng.choice([8, 12, 16])

                draw_pixel_rect(top_panel_canvas, chip_x, chip_y, pixel, pixel, PIXEL_MORTAR_COLOR)
                draw_pixel_rect(top_panel_canvas, chip_x + pixel, chip_y, pixel, pixel, PIXEL_MORTAR_COLOR)

            x += block_width + pixel

        y += block_height + pixel

    # Put title and torches where they belong.
    center_x = canvas_width // 2
    center_y = canvas_height // 2

    top_panel_canvas.coords(title_shadow_item, center_x + 3, center_y + 3)
    top_panel_canvas.coords(title_text_item, center_x, center_y)

    top_panel_canvas.coords(left_torch_item, 80, center_y)
    top_panel_canvas.coords(right_torch_item, canvas_width - 80, center_y)

    # Keep background behind the title and torches.
    top_panel_canvas.tag_lower("panel_bg")
    top_panel_canvas.tag_raise(title_shadow_item)
    top_panel_canvas.tag_raise(title_text_item)
    top_panel_canvas.tag_raise(left_torch_item)
    top_panel_canvas.tag_raise(right_torch_item)
