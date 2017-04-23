from __future__ import generators


def compute_hex_sum(array):
    sum = 0
    i = 0

    for element in array:
        sum += element * pow(2, i * 8)
        i += 1
    return sum


class Bitmap:

    def __init__(self, file):
        self.__HEADER_SIZE = 0x0E
        self.file_hex_array = list(file.read())
        self.file_header = BitmapHeader(self.file_hex_array[0:self.__HEADER_SIZE])
        self.pixel_array = self.file_hex_array[self.file_header.bmp_image_data_start_offset: len(self.file_hex_array)]
        self.bitmap_dib_header = BitmapDIBHeader(self.file_hex_array)
        self.pixel_matrix = self.extract_pixel_matrix()

    def extract_pixel_matrix(self):

        #  TODO: Change multiplier so that it can work in different spaces than RGB
        bytes_per_width = self.bitmap_dib_header.width * 3
        #  Each row in the Pixel array is padded to a multiple of 4 bytes in size
        normalized_bytes_per_width = (bytes_per_width + 4) % 4 + bytes_per_width

        size_matrix = list(range(0, len(self.pixel_array), normalized_bytes_per_width))

        #  Split the pixel_array into a pixel_matrix of size [[0..bytes_per_width]..height]
        return list(map(lambda x: self.pixel_array[x: x + bytes_per_width], size_matrix))


class BitmapHeader:

    def __init__(self, hex_array):
        self.__BMP_FILE_SIZE_OFFSET = 0x02
        self.__BMP_FILE_SIZE_SIZE = 0x04
        self.__BMP_FILE_SIZE_SLICE = slice(self.__BMP_FILE_SIZE_OFFSET,
                                           self.__BMP_FILE_SIZE_OFFSET + self.__BMP_FILE_SIZE_SIZE)
        self.__BMP_IMAGE_DATA_START_OFFSET = 0x0A
        self.__BMP_IMAGE_DATA_START_SIZE = 0x04
        self.__BMP_IMAGE_DATA_START_SLICE = slice(self.__BMP_IMAGE_DATA_START_OFFSET,
                                                  self.__BMP_IMAGE_DATA_START_OFFSET + self.__BMP_IMAGE_DATA_START_SIZE)

        self.hex_array = hex_array
        self.bmp_file_size = compute_hex_sum(hex_array[self.__BMP_FILE_SIZE_SLICE])
        self.bmp_image_data_start_offset = compute_hex_sum(hex_array[self.__BMP_IMAGE_DATA_START_SLICE])


class BitmapDIBHeader:

    def __init__(self, hex_array):
        self.__DIB_HEADER_BEGIN_OFFSET = 0x0E
        self.__DIB_HEADER_SIZE_SIZE = 0x04

        self.header_size = compute_hex_sum(hex_array[self.__DIB_HEADER_BEGIN_OFFSET: self.__DIB_HEADER_BEGIN_OFFSET + self.__DIB_HEADER_SIZE_SIZE])
        header_type = BitmapDIBHeaderType.factory(self.header_size)
        self.__DIB_HEADER_WIDTH_OFFSET = header_type.HEADER_WIDTH_OFFSET
        self.__DIB_HEADER_WIDTH_SIZE = header_type.HEADER_WIDTH_SIZE
        self.__DIB_HEADER_HEIGHT_OFFSET = header_type.HEADER_HEIGHT_OFFSET
        self.__DIB_HEADER_HEIGHT_SIZE = header_type.HEADER_HEIGHT_SIZE

        self.width = compute_hex_sum(hex_array[self.__DIB_HEADER_WIDTH_OFFSET: self.__DIB_HEADER_WIDTH_OFFSET + self.__DIB_HEADER_WIDTH_SIZE])
        self.height = compute_hex_sum(hex_array[self.__DIB_HEADER_HEIGHT_OFFSET: self.__DIB_HEADER_HEIGHT_OFFSET + self.__DIB_HEADER_HEIGHT_SIZE])


class BitmapDIBHeaderType(object):

    def factory(size):
        if size == 108: return BITMAPV4HEADER()
        if size == 40: return BITMAPINFOHEADER()
        assert 0, "Unkown header type with size: " + size


class BITMAPV4HEADER:

    def __init__(self):
        self.HEADER_WIDTH_OFFSET = 0x12
        self.HEADER_WIDTH_SIZE = 0x04
        self.HEADER_HEIGHT_OFFSET = 0x16
        self.HEADER_HEIGHT_SIZE = 0x04


class BITMAPINFOHEADER:

    def __init__(self):
        self.HEADER_WIDTH_OFFSET = 0x12
        self.HEADER_WIDTH_SIZE = 0x04
        self.HEADER_HEIGHT_OFFSET = 0x16
        self.HEADER_HEIGHT_SIZE = 0x04
