import ctypes
from wrappers import *

class Test_Mkdir:
    # successful mkdir operation on a fresh filesystem
    # * valid path
    # * valid name
    # Expected outcome:
    # * return 0
    # * first direct block of root node points to inode[1]
    # * inode[1] is set as a directory, name is set
    # * parent of new directory is set to root dir inode number
    def test_mkdir_easy(self):
        fs = setup(5)
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].name.decode("utf-8") =="testDirectory","UTF-8" 
        assert fs.inodes[1].n_type == 2 # meaning it is marked as directory
        assert fs.inodes[0].direct_blocks[0] == 1 #fs.inodes[0] is the root node. its first direct block should point to the 1st inode (where the new dir is located)
        assert fs.inodes[1].parent == 0

    # successful nested mkdir operation on a fresh filesystem
    # * 2 mkdir operations. 
    # * the second one creates a new directory inside the first one
    # Expected outcome:
    # * return 0
    # * The second directory is located at fs.inodes[2]
    # * name is correct
    # * 0th direct block of first directory points to the correct folder
    # * parents are set correctly
    def test_mkdir_nested(self):
        fs = setup(5)
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8"))) #new dir located at inode 1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest","UTF-8"))) #new dir located at inode 2
        assert retval == 0
        assert fs.inodes[1].name.decode("utf-8") == "testDirectory","UTF-8" 
        assert fs.inodes[1].n_type == 2 # meaning it is marked as directory
        assert fs.inodes[1].direct_blocks[0] == 2 # meaning it is marked as directory
        assert fs.inodes[1].parent == 0
        assert fs.inodes[2].name.decode("utf-8") == "testNest","UTF-8" 
        assert fs.inodes[2].n_type == 2 # meaning it is marked as directory
        assert fs.inodes[2].parent == 1

    # failed mkdir operation because the path is not correctly named (missing a / in the beginning)
    # Expected outcome
    # * return value is -1 
    # * first direct block of root still at default -1
    # * name not set in inodes[1] (where the new directory would be in case of a correct name)
    def test_mkdir_wrong_name(self):
        fs = setup(5)
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("testDirectory","UTF-8"))) #new dir would be located at inode 1 if it wasn't for the error
        assert retval == -1
        assert fs.inodes[0].direct_blocks[0] == -1
        assert fs.inodes[1].name.decode("utf-8") =="" 
        assert fs.inodes[1].n_type == 3 # meaning it is marked as free block

    # Failed creation of nested directory
    # * parent directory of new directory not present
    # Expected outcome
    # * return value is -1
    # every inode (except for root node) at default state
    def test_mkdir_wrong_nested(self):
        fs = setup(5)
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest","UTF-8")))
        assert retval == -1
        
        # check every inode for default state
        for i in range(1,5):
            assert fs.inodes[i].name.decode("utf-8") =="" 
            assert fs.inodes[i].n_type == 3 # meaning it is marked as free block

