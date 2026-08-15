#!/usr/bin/env python3
"""
Generate icons for the MS Skill Mastery Cowork plugin.
- color.png (192x192) - Full-color "learning roadmap" icon: a winding path
  leading up to a flagged summit, evoking a staged mastery journey.
- outline.png (32x32) - Simple white line-art version on a transparent
  background, per the Teams outline icon convention.
"""

from PIL import Image, ImageDraw
import math
import os


def create_color_icon():
    """Create the full-color icon (192x192)."""
    size = 192
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background: rounded square with a blue-to-violet gradient feel
    # (approximated with a vertical gradient fill).
    top_color = (37, 99, 235)      # #2563EB
    bottom_color = (109, 40, 217)  # #6D28D9
    radius = 40
    for y in range(size):
        t = y / (size - 1)
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Mask to rounded-rect shape
    mask = Image.new("L", (size, size), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg.paste(img, (0, 0), mask)
    img = bg
    draw = ImageDraw.Draw(img)

    # Winding mastery path (three curve segments rising left -> right)
    # drawn as a thick dashed-looking road with a center dashed line.
    path_points = [
        (30, 150), (55, 130), (50, 100), (80, 85),
        (95, 60), (130, 50), (120, 25), (150, 18),
    ]
    road_color = (255, 255, 255, 235)
    draw.line(path_points, fill=road_color, width=16, joint="curve")
    # Rounded caps at each vertex so the thick line looks continuous
    for (x, y) in path_points:
        draw.ellipse([x - 8, y - 8, x + 8, y + 8], fill=road_color)

    # Center dashed line to read as a "road"
    dash_color = (37, 99, 235, 255)
    for i in range(len(path_points) - 1):
        x1, y1 = path_points[i]
        x2, y2 = path_points[i + 1]
        dist = math.hypot(x2 - x1, y2 - y1)
        steps = max(1, int(dist // 10))
        for s in range(0, steps, 2):
            t0 = s / steps
            t1 = min(1.0, (s + 1) / steps)
            dx1 = x1 + (x2 - x1) * t0
            dy1 = y1 + (y2 - y1) * t0
            dx2 = x1 + (x2 - x1) * t1
            dy2 = y1 + (y2 - y1) * t1
            draw.line([(dx1, dy1), (dx2, dy2)], fill=dash_color, width=3)

    # Milestone dots along the way (beginner / intermediate stages)
    milestone_color = (16, 185, 129, 255)  # emerald
    for (x, y) in [(50, 100), (95, 60)]:
        draw.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(255, 255, 255, 255))
        draw.ellipse([x - 6, y - 6, x + 6, y + 6], fill=milestone_color)

    # Summit flag (mastery achieved) at the top of the path
    pole_x, pole_top, pole_bottom = 150, 12, 60
    pole_color = (255, 255, 255, 255)
    draw.line([(pole_x, pole_top), (pole_x, pole_bottom)], fill=pole_color, width=4)
    draw.ellipse([pole_x - 4, pole_top - 4, pole_x + 4, pole_top + 4], fill=pole_color)

    flag_color = (245, 158, 11, 255)  # amber
    flag_points = [
        (pole_x, pole_top + 2),
        (pole_x + 34, pole_top + 12),
        (pole_x, pole_top + 24),
    ]
    draw.polygon(flag_points, fill=flag_color)

    # Base "summit" mound under the flag
    draw.ellipse([pole_x - 14, pole_bottom - 6, pole_x + 14, pole_bottom + 10], fill=(255, 255, 255, 235))

    return img


def create_outline_icon():
    """Create the outline icon (32x32) - simple white line art, transparent bg."""
    size = 32
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    outline_color = (255, 255, 255, 255)

    # Simplified winding path
    path_points = [(5, 26), (10, 22), (9, 16), (15, 13), (18, 8), (24, 6)]
    draw.line(path_points, fill=outline_color, width=2, joint="curve")

    # Milestone dot
    mx, my = 15, 13
    draw.ellipse([mx - 2, my - 2, mx + 2, my + 2], outline=outline_color, width=1)

    # Flag pole + pennant at the summit
    pole_x, pole_top, pole_bottom = 24, 3, 9
    draw.line([(pole_x, pole_top), (pole_x, pole_bottom)], fill=outline_color, width=1)
    draw.polygon(
        [(pole_x, pole_top), (pole_x + 6, pole_top + 3), (pole_x, pole_top + 6)],
        outline=outline_color,
        width=1,
    )

    return img


def main():
    plugin_dir = os.path.dirname(os.path.abspath(__file__))

    print("Generating color icon (192x192)...")
    color_img = create_color_icon()
    color_path = os.path.join(plugin_dir, "color.png")
    color_img.save(color_path, "PNG")
    print(f"Created: {color_path}")

    print("Generating outline icon (32x32)...")
    outline_img = create_outline_icon()
    outline_path = os.path.join(plugin_dir, "outline.png")
    outline_img.save(outline_path, "PNG")
    print(f"Created: {outline_path}")

    print("\nIcon generation complete!")
    print(f"   color.png:   {os.path.getsize(color_path)} bytes")
    print(f"   outline.png: {os.path.getsize(outline_path)} bytes")


if __name__ == "__main__":
    main()
