import ctypes
from wrappers import *

class Test_Mkda:
    # check if a duplicate root directory leads to an error
    def test_mkdir_duplicate(self):
        fs = setup(5)
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8")))
        assert retval == -1
    
    # check if a duplicate root directory leads to an error
    def test_mkdir_nested_duplicate(self):
        fs = setup(5)
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest","UTF-8")))
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8")))
        assert retval == -1
    def test_mkdir_nested_duplicate_2(self):
        fs = setup(6)
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8"))) # inode num 1
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testDirectory","UTF-8"))) # inode num 2 
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8"))) # inode num 1
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testDirectory","UTF-8")))
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testDirectory/testDirectory","UTF-8"))) # inode num 2 
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8"))) # inode num 1
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testDirectory","UTF-8")))
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testDirectory/testDirectory","UTF-8")))
        assert retval == -1
    def test_mkdir_nested_duplicate_3(self):
        fs = setup(11)
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/asdf","UTF-8"))) # inode num 1
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/asdf/asdf","UTF-8"))) # inode num 2 
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/asdf","UTF-8"))) # inode num 1
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/asdf/asdf","UTF-8")))
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/asdf/asdf/asdf","UTF-8"))) # inode num 2 
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/asdf","UTF-8"))) # inode num 1
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/asdf/asdf","UTF-8")))
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/asdf/asdf/asdf","UTF-8")))
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/asdf/asdf/jasdklfjaslkdfj","UTF-8"))) # inode num 1
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/asdf/asdf/jasdklfjaslkdfj","UTF-8"))) # inode num 1
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/asdf/asdaklsdjflkasasdf","UTF-8"))) # inode num 1
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/asdf/asdaklsdjflkasasdf","UTF-8"))) # inode num 1
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/asdf/asdaklsdjflkasasdf/jasdklfjaslkdfj","UTF-8"))) # inode num 1
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/asdf/asdaklsdjflkasasdf/jasdklfjaslkdfj","UTF-8"))) # inode num 1
        assert retval == -1
