import ctypes
from wrappers import *

class Test_Writef:
    # writes a small chunk of data (smaller than 1 block) to an already existing file
    def test_writef_simple(self):
        fs = setup(5)
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)
        teststring = "I am a little test"
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(teststring,"utf-8")))
        assert retval == 18 # the number of bytes written
        assert fs.inodes[1].direct_blocks[0] == 0 # the data should be written in the first possible block
        assert fs.free_list[0] == 0
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == teststring
        assert fs.data_blocks[0].size == 18

    # Try to write to a nonexisting file. Should return -1 and not touch any blocks
    def test_writef_file_not_found(self):
        fs = setup(5)
        teststring = "I am a little test"
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(teststring,"utf-8")))
        assert retval == -1 # returns
        assert fs.inodes[1].direct_blocks[0] == -1 # there is no file at inodes[1], thus its direct blocks are not changed
        assert fs.free_list[0] == 1 # free list is at default value because that block isnt touched
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value # should be an empty block
        assert outstring.decode("utf-8") == ""

    # First block already blocked, has to write in second block
    # File 1 addresses 1 Block already, file 2 has to use the next block
    def test_writef_second_block(self):
        fs = setup(5)
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)
        fs = set_fil(name="fil2",inode=2,parent=0,parent_block=0,fs=fs)

        set_data_block_with_string(block_num=0, string_data="I am a test", parent_inode=1,parent_block_num=0,fs=fs)

        teststring = "I am a little test"
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil2","UTF-8")),ctypes.c_char_p(bytes(teststring,"utf-8")))
        assert retval == 18 # the number of bytes written
        assert fs.inodes[2].direct_blocks[0] == 1 # the data should be written in the first possible block which in this case is block 1
        assert fs.free_list[0] == 0
        assert fs.free_list[1] == 0
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[1].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == teststring

    def test_writef_append(self):
        fs = setup(5)
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)
        teststring1 = "I am already here"
        set_data_block_with_string(block_num=0, string_data=teststring1, parent_inode=1,parent_block_num=0,fs=fs)

        teststring2 = "And I will be added"
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(teststring2,"utf-8")))
        assert retval == 19 # the number of bytes written
        assert fs.inodes[1].direct_blocks[0] == 0   # the data should be appended to the previously used block
        assert fs.inodes[1].direct_blocks[1] == -1  # so the second block should not be used
        assert fs.free_list[0] == 0                 # This is also represented in the free list
        assert fs.free_list[1] == 1
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == teststring1+teststring2

    # in this test you need two blocks to store all the data
    def test_writef_long_data(self):
        fs = setup(5)
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)

        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(LONG_DATA,"utf-8")))
        assert retval == len(LONG_DATA)# the number of bytes written
        assert fs.inodes[1].direct_blocks[0] == 0   # the data should be written to block 0 and 1
        assert fs.inodes[1].direct_blocks[1] == 1
        assert fs.free_list[0] == 0                 # This is also represented in the free list
        assert fs.free_list[1] == 0
        outstring1 = bytearray(ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value) #convert the raw data block to a string
        outstring1 = outstring1[:1024] # needed reassignment because there is no terminating 0 byte in the data block
        outstring2 = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[1].block)).value #convert the raw data block to a string
        assert outstring1.decode("utf-8")+outstring2.decode("utf-8") == LONG_DATA


