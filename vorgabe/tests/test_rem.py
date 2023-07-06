import ctypes
from wrappers import *

class Test_Rem:
    def test_rem_one_empty_file(self):
        fs = setup(5)
        fs = set_fil(name="newFil",inode=1,parent=0,parent_block=0,fs=fs)
        retval = libc.fs_rm(ctypes.byref(fs), ctypes.c_char_p(bytes("/newFil","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].n_type == 3 # inode marked as free in the inodes array
        assert fs.inodes[0].direct_blocks[0] == -1

    def test_rem_one_nonempty_file(self):
        fs = setup(5)
        fs = set_fil(name="newFil",inode=1,parent=0,parent_block=0,fs=fs)
        mockup_data = "I am a file"
        fs = set_data_block_with_string(block_num=0,string_data=mockup_data,parent_inode=1,parent_block_num=0,fs=fs)
        retval = libc.fs_rm(ctypes.byref(fs), ctypes.c_char_p(bytes("/newFil","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].n_type == 3
        assert fs.free_list[0] == 1
        assert fs.inodes[0].direct_blocks[0] == -1

    def test_rem_empty_dir(self):
        fs = setup(5)
        fs = set_dir(name="newDir",inode=1,parent=0,parent_block=0,fs=fs)
        retval = libc.fs_rm(ctypes.byref(fs), ctypes.c_char_p(bytes("/newDir","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].n_type == 3
        assert fs.inodes[0].direct_blocks[0] == -1

    def test_rem_dir_one_recursion(self):
        fs = setup(5)
        fs = set_dir(name="newDir",inode=1,parent=0,parent_block=0,fs=fs)
        fs = set_fil(name="newFil",inode=2,parent=1,parent_block=0,fs=fs)
        retval = libc.fs_rm(ctypes.byref(fs), ctypes.c_char_p(bytes("/newDir","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].n_type == 3
        assert fs.inodes[2].n_type == 3
        assert fs.inodes[0].direct_blocks[0] == -1
        assert fs.inodes[1].direct_blocks[0] == -1


    def test_rem_dir_one_recursion_nonempty_file(self):
        fs = setup(5)
        fs = set_dir(name="newDir",inode=1,parent=0,parent_block=0,fs=fs)
        fs = set_fil(name="newFil",inode=2,parent=1,parent_block=0,fs=fs)
        mockup_data = "I am a file"
        fs = set_data_block_with_string(block_num=0,string_data=mockup_data,parent_inode=2,parent_block_num=0,fs=fs)
        retval = libc.fs_rm(ctypes.byref(fs), ctypes.c_char_p(bytes("/newDir","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].n_type == 3
        assert fs.inodes[2].n_type == 3
        assert fs.free_list[0] == 1
        assert fs.inodes[0].direct_blocks[0] == -1
        assert fs.inodes[1].direct_blocks[0] == -1

    def test_rem_dir_two_recursion(self):
        fs = setup(5)
        fs = set_dir(name="firstDir",inode=1,parent=0,parent_block=0,fs=fs)
        fs = set_dir(name="secondDir",inode=2,parent=1,parent_block=0,fs=fs)
        fs = set_fil(name="newFil",inode=3,parent=2,parent_block=0,fs=fs)
        retval = libc.fs_rm(ctypes.byref(fs), ctypes.c_char_p(bytes("/firstDir","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].n_type == 3
        assert fs.inodes[2].n_type == 3
        assert fs.inodes[3].n_type == 3
        assert fs.inodes[0].direct_blocks[0] == -1
        assert fs.inodes[1].direct_blocks[0] == -1
        assert fs.inodes[2].direct_blocks[0] == -1

    def test_rem_recursion_multiple_files(self):
        fs = setup(7)
        fs = set_dir(name="firstDir",inode=1,parent=0,parent_block=0,fs=fs)
        fs = set_fil(name="fil1",inode=2,parent=1,parent_block=0,fs=fs)
        fs = set_fil(name="fil2",inode=3,parent=1,parent_block=1,fs=fs)
        fs = set_fil(name="fil3",inode=4,parent=1,parent_block=2,fs=fs)
        retval = libc.fs_rm(ctypes.byref(fs), ctypes.c_char_p(bytes("/firstDir","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].n_type == 3
        assert fs.inodes[2].n_type == 3
        assert fs.inodes[3].n_type == 3
        assert fs.inodes[4].n_type == 3
        assert fs.inodes[0].direct_blocks[0] == -1
        assert fs.inodes[0].direct_blocks[1] == -1
        assert fs.inodes[0].direct_blocks[2] == -1

