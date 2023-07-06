import ctypes
from wrappers import *

class Test_Mkfile:
    # Successful mkfil operation
    # * creates a new empty file at the root level
    # Expected outcome:
    # * node type is set to reg_file
    # * name is correct
    # * parent node's first direct block points to newly activated inode at position 1
    # * parent node correctly set in new file
    def test_mkfile_easy(self):
        fs = setup(5)
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/testFile","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].n_type == 1 # meaning it is marked as regular file
        assert fs.inodes[1].name.decode("utf-8") =="testFile" 
        assert fs.inodes[0].direct_blocks[0] == 1 #fs.inodes[0] is the root node. its first direct block should point to the 1st inode (where the new file is located)
        assert fs.inodes[1].parent == 0


    # Successful mkfil operation in a nested directory
    # * setup a filesystem with a directory on inodes[1] called newDir
    # * creates a new file at /newDir/newFile
    # Expected outcome:
    # * node type is set to reg_file
    # * name is correct
    # * parent node's first direct block points to newly activated inode at position 2
    def test_mkfile_nested(self):
        fs = setup(5)
        #setting up a directory
        fs = set_dir(name="newDir",inode=1,parent=0,parent_block=0,fs=fs)

        # the actual test
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/newDir/newFile","UTF-8")))
        assert retval == 0
        assert fs.inodes[2].n_type == 1 # meaning it is marked as regular file
        assert fs.inodes[2].name.decode("utf-8") == "newFile" 
        assert fs.inodes[1].direct_blocks[0] == 2 #fs.inodes[1] is the node of /newDir. Its direct block [0] should point to the inode[2] (where the new file is located)
        assert fs.inodes[1].parent == 0
        assert fs.inodes[2].parent == 1

    # failed mkfil operation because the path is not correctly named (missing a / in the beginning)
    # Expected outcome
    # * return value is -1 
    # * first direct block of root still at default -1
    # * name not set in inodes[1] (where the new directory would be in case of a correct name)
    def test_mkfile_wrong_name(self):
        fs = setup(5)
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("testFile","UTF-8"))) #new file would be located at inode 1 if it wasn't for the error
        assert retval == -1
        assert fs.inodes[0].direct_blocks[0] == -1
        assert fs.inodes[1].name.decode("utf-8") =="" 
        assert fs.inodes[1].n_type == 3 # meaning it is marked as free block

    # Failed creation of nested directory
    # * parent directory of new file not present
    # Expected outcome
    # * return value is -1
    # every inode (except for root node) at default state
    def test_mkfile_wrong_nested(self):
        fs = setup(5)
        retval = libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest","UTF-8")))
        assert retval == -1
        
        # check every inode for default state
        for i in range(1,5):
            assert fs.inodes[i].name.decode("utf-8") =="" 
            assert fs.inodes[i].n_type == 3 # meaning it is marked as free block

