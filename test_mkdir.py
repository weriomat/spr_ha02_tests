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
    # check if file in same dir leads to error when creating dir
    def test_mkdir_file(self):
        fs = setup(5)
        fs = set_fil(name="testDirectory",inode=1,parent=0,parent_block=0,fs=fs) # 1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8"))) # 2
        assert retval == 0
        assert fs.inodes[1].n_type == 1 # meaning it is marked as regular file
        assert fs.inodes[1].name.decode("utf-8") == "testDirectory" 
        assert fs.inodes[0].direct_blocks[0] == 1 
        assert fs.inodes[2].n_type == 2 # meaning it is marked as regular file
        assert fs.inodes[2].name.decode("utf-8") == "testDirectory" 
        assert fs.inodes[0].direct_blocks[1] == 2
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8"))) # 3
        assert retval == -1


    # check if exhausted inodes leads to an error
    def test_mkdir_exhausted(self):
        fs = setup(2)
        assert fs.s_block[0].num_blocks == 2 # root + /testDirectory
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8")))
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory2","UTF-8")))
        assert retval == -1
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
    def test_mkdir_nested_duplicate_2(self):
        fs = setup(6)
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8"))) # inode num 1
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testDirectory","UTF-8"))) # inode num 2 
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testDirectory","UTF-8")))
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testDirectory/testDirectory","UTF-8"))) # inode num 2 
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testDirectory/testDirectory","UTF-8")))
        assert retval == -1
        
    # check if a duplicate root directory leads to an error
    def test_mkdir_nested_duplicate_right_parent(self):
        fs = setup(13)
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8"))) # inode num 1
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest","UTF-8"))) # inode num 2 
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest","UTF-8")))
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest/test","UTF-8"))) # inode num 3 
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest/test/asdf","UTF-8"))) # inode num 4
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest/test/asdf","UTF-8"))) # inode num 4
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/tmp","UTF-8"))) # inode num 5
        assert retval == 0
        assert fs.inodes[0].direct_blocks[0] == 1
        assert fs.inodes[1].direct_blocks[0] == 2
        assert fs.inodes[2].direct_blocks[0] == 3
        assert fs.inodes[3].direct_blocks[0] == 4
        assert fs.inodes[1].direct_blocks[1] == 5
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest/testNest","UTF-8"))) # inode num 6
        assert retval == 0
        assert fs.inodes[0].direct_blocks[0] == 1
        assert fs.inodes[1].direct_blocks[0] == 2
        assert fs.inodes[2].direct_blocks[0] == 3
        assert fs.inodes[3].direct_blocks[0] == 4
        assert fs.inodes[1].direct_blocks[1] == 5
        assert fs.inodes[2].direct_blocks[1] == 6
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest/test/asdf","UTF-8"))) 
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest/testNest","UTF-8"))) 
        assert retval == -1
        assert fs.inodes[0].direct_blocks[0] == 1
        assert fs.inodes[1].direct_blocks[0] == 2
        assert fs.inodes[2].direct_blocks[0] == 3
        assert fs.inodes[3].direct_blocks[0] == 4
        assert fs.inodes[1].direct_blocks[1] == 5
        assert fs.inodes[2].direct_blocks[1] == 6
        assert fs.inodes[6].direct_blocks[0] == -1
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest/testDirectory","UTF-8"))) # inode num 7 
        assert retval == 0
        assert fs.inodes[0].direct_blocks[0] == 1
        assert fs.inodes[1].direct_blocks[0] == 2
        assert fs.inodes[2].direct_blocks[0] == 3
        assert fs.inodes[3].direct_blocks[0] == 4
        assert fs.inodes[1].direct_blocks[1] == 5
        assert fs.inodes[2].direct_blocks[1] == 6
        assert fs.inodes[2].direct_blocks[2] == 7
        assert fs.inodes[7].name.decode("utf-8") =="testDirectory"
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest/testDirectory","UTF-8"))) # inode num 7 
        assert fs.inodes[0].direct_blocks[0] == 1
        assert fs.inodes[1].direct_blocks[0] == 2
        assert fs.inodes[2].direct_blocks[0] == 3
        assert fs.inodes[3].direct_blocks[0] == 4
        assert fs.inodes[1].direct_blocks[1] == 5
        assert fs.inodes[2].direct_blocks[1] == 6
        assert fs.inodes[2].direct_blocks[2] == 7
        assert fs.inodes[8].name.decode("utf-8") == ""
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest/testDirectory/testNest","UTF-8"))) # inode num 8
        assert retval == 0
        assert fs.inodes[0].direct_blocks[0] == 1
        assert fs.inodes[1].direct_blocks[0] == 2
        assert fs.inodes[2].direct_blocks[0] == 3
        assert fs.inodes[3].direct_blocks[0] == 4
        assert fs.inodes[1].direct_blocks[1] == 5
        assert fs.inodes[2].direct_blocks[1] == 6
        assert fs.inodes[7].name.decode("utf-8") =="testDirectory"
        assert fs.inodes[1].name.decode("utf-8") =="testDirectory"
        assert fs.inodes[2].direct_blocks[2] == 7
        assert fs.inodes[8].name.decode("utf-8") =="testNest"
        assert fs.inodes[7].direct_blocks[0] == 8
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest/testDirectory/testDirectory","UTF-8"))) # inode num 8
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/testNest/testDirectory/testDirectory","UTF-8"))) # inode num 8
        assert retval == -1
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/tmp/tmp","UTF-8"))) # inode num 8
        assert retval == 0
        retval = libc.fs_mkdir(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/tmp/tmp","UTF-8"))) # inode num 8
        assert retval == -1