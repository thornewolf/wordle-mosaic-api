import numpy as np
from PIL import Image
from dataclasses import dataclass
from common import WordleSquare, Resolution


def load_image(image_path: str) -> Image.Image:
    with open(image_path, "rb") as f:
        i = Image.open(f)
        i.load()
    return i


def downscale_image(img: Image.Image, target_resulution: Resolution) -> Image.Image:
    return img.resize((target_resulution.width, target_resulution.height))


def dist_from_color(pixel, color):
    return np.sqrt(sum(map(np.square, np.array(pixel) - np.array(color))))


def select_square_for_pixel(
    pixel: tuple[int, int, int], dominant_colors: tuple[tuple[int, int, int]]
) -> WordleSquare:
    pixel = tuple(map(int, pixel))
    green_level = dist_from_color(pixel, dominant_colors[0])
    yellow_level = dist_from_color(pixel, dominant_colors[1])
    black_level = dist_from_color(pixel, dominant_colors[2])
    return [
        WordleSquare.BLACK,
        WordleSquare.YELLOW,
        WordleSquare.GREEN,
    ][np.argmin([green_level, yellow_level, black_level])]


def get_dominant_colors(img: Image.Image) -> tuple[tuple[int, int, int]]:
    # Resize image to speed up processing
    img = img.copy()
    img.thumbnail((100, 100))

    # Reduce colors (uses k-means internally)
    paletted = img.convert("P", palette=Image.ADAPTIVE, colors=3)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    dominant_index = color_counts[0][1]
    secondary_index = color_counts[1][1]
    ternary_index = color_counts[-1][1]
    dominant_color = palette[dominant_index * 3 : dominant_index * 3 + 3]
    secondary_color = palette[secondary_index * 3 : secondary_index * 3 + 3]
    ternary_color = palette[ternary_index * 3 : ternary_index * 3 + 3]

    return dominant_color, secondary_color, ternary_color


def image_to_wordle_squares(img: Image.Image) -> list[list[WordleSquare]]:
    data = np.asarray(img)
    dominant_colors = get_dominant_colors(img)
    squares = [
        [select_square_for_pixel(p, dominant_colors) for p in row] for row in data
    ]
    return squares


def wordle_squares_to_str(squares: list[list[WordleSquare]]) -> str:
    return "\n".join(["".join([s.value for s in r]) for r in squares])


def convert_image(image_path, resolution):
    # Load image
    img = load_image(image_path)
    # Downscale image
    img = downscale_image(img, resolution)
    # Determine appropriate wordle square for each pixel
    wordle_squares = image_to_wordle_squares(img)
    # Construct resultant string from selected squares
    return wordle_squares_to_str(wordle_squares)


def convert_existing_image(img, resolution):
    img = downscale_image(img, resolution)
    # Determine appropriate wordle square for each pixel
    wordle_squares = image_to_wordle_squares(img)
    # Construct resultant string from selected squares
    return wordle_squares_to_str(wordle_squares)
