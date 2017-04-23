from unittest import TestCase
from lib.bitmap import Bitmap
import os


class TestBitmap(TestCase):

    def setUp(self):
        # self.lena_bitmap = Bitmap(open("img/lena.bmp", "rb"))
        self.two_black_pixels_bitmap = Bitmap(open("img/two_black_pixels.bmp", "rb"))

    def test_extract_header(self):
        expected_result = [0x42, 0x4D, 0x8A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7A, 0x00, 0x00, 0x00]
        self.assertEqual(expected_result, self.two_black_pixels_bitmap.file_header.hex_array)

    def test_bitmap_header_file_size(self):
        expected_result = os.stat("img/two_black_pixels.bmp").st_size
        self.assertEqual(expected_result, self.two_black_pixels_bitmap.file_header.bmp_file_size)

    def test_bitmap_header_image_start_offset(self):
        expected_result = 122
        self.assertEqual(expected_result, self.two_black_pixels_bitmap.file_header.bmp_image_data_start_offset)

    def test_bitmap_data(self):
        expected_result = [0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0x00, 0x00]
        self.assertEqual(expected_result, self.two_black_pixels_bitmap.pixel_array)

    def test_bitmap_dib_header_width(self):
        expected_result = 2
        self.assertEqual(expected_result, self.two_black_pixels_bitmap.bitmap_dib_header.width)

    def test_bitmap_dib_header_height(self):
        expected_result = 2
        self.assertEqual(expected_result, self.two_black_pixels_bitmap.bitmap_dib_header.height)

    def test_bitmap_lena_width(self):
        expected_result = 512
        self.assertEqual(expected_result, self.lena_bitmap.bitmap_dib_header.width)

    def test_two_black_pixels_bitmap_first_row(self):
        expected_result = [0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00]
        self.assertEqual(expected_result, self.two_black_pixels_bitmap.pixel_matrix[0])

    def test_two_black_pixels_bitmap_second_row(self):
        expected_result = [0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF]
        self.assertEqual(expected_result, self.two_black_pixels_bitmap.pixel_matrix[1])
