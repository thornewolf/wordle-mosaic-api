import unittest
from PIL import Image
from conversion import (
    load_image,
    downscale_image,
    select_square_for_pixel,
    wordle_squares_to_str,
)
from common import WordleSquare, Resolution

TEST_IMAGE = "testdata/conversion_test/flowers.jpeg"

DOWNSCALE_WIDTH = 400
DOWNSCALE_HEIGHT = 800
DOWNSCALE_IMAGE_SIZE = Resolution(DOWNSCALE_WIDTH, DOWNSCALE_HEIGHT)


WORDLE_SQUARES_IN_SEQUENCE = [
    [
        WordleSquare.GREEN,
        WordleSquare.YELLOW,
        WordleSquare.BLACK,
        WordleSquare.WHITE,
    ],
]
STRING_WORDLE_SQUARES = """🟩🟨⬛⬜"""


class TestConversion(unittest.TestCase):
    def test_load_image(self):
        result = load_image(TEST_IMAGE)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Image.Image)

    def test_downscale_image(self):
        image = load_image(TEST_IMAGE)
        downscaled = downscale_image(image, DOWNSCALE_IMAGE_SIZE)
        expected = (DOWNSCALE_WIDTH, DOWNSCALE_HEIGHT)
        self.assertTupleEqual(downscaled.size, expected)

    def test_select_squares_for_pixel(self):
        green_pixel = [0, 255, 0]
        yellow_pixel = [255, 255, 0]
        black_pixel = [0, 0, 0]
        white_pixel = [255, 255, 255]

        self.assertEqual(select_square_for_pixel(green_pixel), WordleSquare.GREEN)
        self.assertEqual(select_square_for_pixel(yellow_pixel), WordleSquare.YELLOW)
        self.assertEqual(select_square_for_pixel(black_pixel), WordleSquare.BLACK)
        self.assertEqual(select_square_for_pixel(white_pixel), WordleSquare.WHITE)

    def test_wordle_squares_to_str(self):
        self.assertEqual(
            wordle_squares_to_str(WORDLE_SQUARES_IN_SEQUENCE), STRING_WORDLE_SQUARES
        )


if __name__ == "__main__":
    unittest.main()
