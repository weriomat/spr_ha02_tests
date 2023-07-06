import ctypes
from wrappers import *

class Test_Complex:

    # Creates a file then deletes it. The inode should be set to "free" again
    def test_complex_create_and_delete_easy(self):
        fs = setup(5)
        libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8")))
        retval = libc.fs_rm(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].n_type == 3, "The inode should be set as 'free'==3"
        assert fs.inodes[0].direct_blocks[0] == -1, "The parent node should not point to the file anymore"

    # Creates a file, puts data in it then deletes it. The inode should be set to "free" again
    def test_complex_create_write_delete(self):
        fs = setup(5)
        libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8")))
        fs = set_data_block_with_string(block_num = 0, string_data=SHORT_DATA,parent_inode = 1,parent_block_num = 0, fs=fs)
        retval = libc.fs_rm(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].n_type == 3, "The inode should be set as 'free'==3"
        assert fs.inodes[0].direct_blocks[0] == -1, "The parent node should not point to the file anymore"
        assert fs.free_list[0] == 1, "The free list needs to be updated when a file that holds data is removed"

# TODO: Maybe think of more tests
