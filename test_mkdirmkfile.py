import ctypes
from wrappers import *

class Test_MkdirMkfile:

    def test_mkdirmkfile_easy(self):
        fs = setup(4)
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/test","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].name.decode("utf-8") =="test","UTF-8"
        assert fs.inodes[1].n_type == 1
        assert fs.inodes[0].direct_blocks[0] == 1
        assert fs.inodes[1].parent == 0
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/test/testFile","UTF-8")))
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test","UTF-8")))
        assert retval == 0
        assert fs.inodes[2].name.decode("utf-8") =="test","UTF-8"
        assert fs.inodes[2].n_type == 2
        assert fs.inodes[0].direct_blocks[1] == 2
        assert fs.inodes[2].parent == 0
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/test/testFile","UTF-8")))
        assert retval == 0
        assert fs.inodes[3].name.decode("utf-8") =="testFile","UTF-8"
        assert fs.inodes[3].n_type == 1
        assert fs.inodes[2].direct_blocks[0] == 3
        assert fs.inodes[3].parent == 2
        assert fs.inodes[1].direct_blocks[0] == -1

    def test_mkdirmkfile_easy2(self):
        fs = setup(4)
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/test","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].name.decode("utf-8") =="test","UTF-8"
        assert fs.inodes[1].n_type == 1
        assert fs.inodes[0].direct_blocks[0] == 1
        assert fs.inodes[1].parent == 0
        # we do not have to cover
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/test","UTF-8")))
        assert retval == -2
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test","UTF-8")))
        assert retval == 0
        assert fs.inodes[2].name.decode("utf-8") =="test","UTF-8"
        assert fs.inodes[2].n_type == 2
        assert fs.inodes[0].direct_blocks[1] == 2
        assert fs.inodes[2].parent == 0
        # we do not have to cover
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test","UTF-8")))
        assert retval == -1
    # we do not have to cover
    def test_mkdirmkfile_many(self):
        fs = setup(16)
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test1","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test2","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test3","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test4","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test5","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test6","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test7","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test8","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test9","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test10","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test11","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test12","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test13","UTF-8")))
        assert retval == -1
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/test14","UTF-8")))
        assert retval == -1
    # we do not have to cover
    def test_mkdirmkfile_many2(self):
        fs = setup(3)
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test1","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test2","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test3","UTF-8")))
        assert retval == -1
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/test4","UTF-8")))
        assert retval == -1

    def test_mkdirmkfile_invalid_nichtsowichtig(self):
        fs = setup(3)
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("test1","UTF-8")))
        assert retval == -1
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("test2","UTF-8")))
        assert retval == -1
    #    retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/////","UTF-8")))
    #    assert retval == -1
    #    retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/////","UTF-8")))
    #    assert retval == -1

    #    retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/","UTF-8")))
    #    assert retval == -1
    #    retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/","UTF-8")))
    #    assert retval == -1

    #    retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/test1","UTF-8")))
    #    assert retval == 0
        #retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("test1/test1","UTF-8")))
        #assert retval == -1
        #retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("test1/test1","UTF-8")))
        #assert retval == -1
        #retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/","UTF-8")))
        #assert retval == -1
        #retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/","UTF-8")))
        #assert retval == -1