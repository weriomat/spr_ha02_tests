import ctypes
from wrappers import *

class Test_MkfileRmWriteRead:

    def test_mkfilermwritef_easy(self):
        fs = setup(5)
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFileee1","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].name.decode("utf-8") =="testFileee1","UTF-8"
        assert fs.inodes[1].n_type == 1
        assert fs.inodes[0].direct_blocks[0] == 1
        assert fs.inodes[1].parent == 0

        teststring1 = "Wenn Cem das liest, dann hat er den Test verkackt 🤭🤭🤭"
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFileee1","UTF-8")),ctypes.c_char_p(bytes(teststring1,"utf-8")))
        assert retval == 62
        assert fs.inodes[1].direct_blocks[0] == 0
        assert fs.free_list[0] == 0
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value
        assert outstring.decode("utf-8") == teststring1
        assert fs.data_blocks[0].size == 62

        retval = libc.fs_rm(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFileee1","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].n_type == 3
        assert fs.inodes[0].direct_blocks[0] == -1

        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile2","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].name.decode("utf-8") =="testFile2","UTF-8"
        assert fs.inodes[1].n_type == 1
        assert fs.inodes[0].direct_blocks[0] == 1
        assert fs.inodes[1].parent == 0

        teststring2 = "😎👍"
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile2","UTF-8")),ctypes.c_char_p(bytes(teststring2,"utf-8")))
        assert retval == 8
        assert fs.inodes[1].direct_blocks[0] == 0
        assert fs.free_list[0] == 0
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value
        assert outstring.decode("utf-8") == teststring2
        assert fs.data_blocks[0].size == 8

    def test_mkfilewritef_nowrite(self):
        fs = setup(3)
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].name.decode("utf-8") =="testFile","UTF-8"
        assert fs.inodes[1].n_type == 1
        assert fs.inodes[0].direct_blocks[0] == 1
        assert fs.inodes[1].parent == 0
        teststring = ""
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile","UTF-8")),ctypes.c_char_p(bytes(teststring,"utf-8")))
        assert retval == 0
        assert fs.inodes[1].direct_blocks[0] == -1
        assert fs.free_list[0] == 1
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value
        assert outstring.decode("utf-8") == teststring
        assert fs.data_blocks[0].size == 0

    def test_mkfilewritefreadf_fullwrite(self):
        fs = setup(14)
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].name.decode("utf-8") =="testFile","UTF-8"
        assert fs.inodes[1].n_type == 1
        assert fs.inodes[0].direct_blocks[0] == 1
        assert fs.inodes[1].parent == 0

        teststring = ""
        for i in range (0, BLOCK_SIZE*DIRECT_BLOCKS_COUNT):
            teststring += chr(65+(i%25))
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile","UTF-8")),ctypes.c_char_p(bytes(teststring,"utf-8")))
        assert retval == BLOCK_SIZE*DIRECT_BLOCKS_COUNT
        assert fs.inodes[1].direct_blocks[11] == 11
        assert fs.data_blocks[11].size == BLOCK_SIZE
        assert fs.free_list[11] == 0
        file_length = ctypes.c_int(0)
        retval = libc.fs_readf(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile","utf-8")),ctypes.byref(file_length))
        assert file_length.value == BLOCK_SIZE*DIRECT_BLOCKS_COUNT
        assert retval[:BLOCK_SIZE*DIRECT_BLOCKS_COUNT].decode("utf-8") == teststring
        assert fs.data_blocks[11].size == BLOCK_SIZE
        # we do not have to cover
        teststring2 = "B"
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile","UTF-8")),ctypes.c_char_p(bytes(teststring2,"utf-8")))
        assert retval == -2

    def test_mkfilewritefreadfrm_noteasy(self):
        fs = setup(25)
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile1","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].name.decode("utf-8") =="testFile1","UTF-8"
        assert fs.inodes[1].n_type == 1
        assert fs.inodes[0].direct_blocks[0] == 1
        assert fs.inodes[1].parent == 0

        teststring1 = ""
        for i in range (0, BLOCK_SIZE*6):
            teststring1 += chr(65+(i%25))
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile1","UTF-8")),ctypes.c_char_p(bytes(teststring1,"utf-8")))
        assert retval == BLOCK_SIZE*6

        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile2","UTF-8")))
        assert retval == 0
        assert fs.inodes[2].name.decode("utf-8") =="testFile2","UTF-8"
        assert fs.inodes[2].n_type == 1
        assert fs.inodes[0].direct_blocks[1] == 2
        assert fs.inodes[2].parent == 0

        teststring2 = ""
        for i in range (0, BLOCK_SIZE*DIRECT_BLOCKS_COUNT):
            teststring2 += chr(97+(i%25))
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile2","UTF-8")),ctypes.c_char_p(bytes(teststring2,"utf-8")))
        assert retval == BLOCK_SIZE*DIRECT_BLOCKS_COUNT

        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile1","UTF-8")),ctypes.c_char_p(bytes(teststring1,"utf-8")))
        assert retval == BLOCK_SIZE*6

        file_length1 = ctypes.c_int(0)
        retval = libc.fs_readf(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile1","utf-8")),ctypes.byref(file_length1))
        assert file_length1.value == BLOCK_SIZE*DIRECT_BLOCKS_COUNT
        assert retval[:BLOCK_SIZE*DIRECT_BLOCKS_COUNT].decode("utf-8") == teststring1+teststring1

        file_length2 = ctypes.c_int(0)
        retval = libc.fs_readf(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile2","utf-8")),ctypes.byref(file_length2))
        assert file_length2.value == BLOCK_SIZE*DIRECT_BLOCKS_COUNT
        assert retval[:1024*12].decode("utf-8") == teststring2

        retval = libc.fs_rm(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile1","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].n_type == 3
        assert fs.inodes[0].direct_blocks[0] == -1
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].name.decode("utf-8") =="testFile","UTF-8"
        assert fs.inodes[1].n_type == 1
        assert fs.inodes[0].direct_blocks[0] == 1
        assert fs.inodes[1].parent == 0
        teststring3 = "Swag"
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile","UTF-8")),ctypes.c_char_p(bytes(teststring3,"utf-8")))
        assert retval == 4
        file_length3 = ctypes.c_int(0)
        retval = libc.fs_readf(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile","utf-8")),ctypes.byref(file_length3))
        assert file_length3.value == 4
        assert retval[:4].decode("utf-8") == teststring3
        assert fs.data_blocks[0].size == 4
        assert fs.inodes[1].size == 4
    # we do not have to cover
    def test_mkfilewrite_notenoughdb(self):
        fs = setup(4)
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile1","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].name.decode("utf-8") =="testFile1","UTF-8"
        assert fs.inodes[1].n_type == 1
        assert fs.inodes[0].direct_blocks[0] == 1
        assert fs.inodes[1].parent == 0

        teststring1 = ""
        for i in range (0, BLOCK_SIZE*6):
            teststring1 += "A"
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile1","UTF-8")),ctypes.c_char_p(bytes(teststring1,"utf-8")))
        assert retval == -1