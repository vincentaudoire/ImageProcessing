from lib.bitmap import Bitmap

if __name__ == '__main__':
    my_file = open("lena.bmp", "rb")
    my_bitmap = Bitmap(my_file)

    print(my_bitmap.file_header)