import ctypes
from wrappers import *

class Test_Writef:
    # writes a small chunk of data (smaller than 1 block) to an already existing file
    def test_writef_simple(self):
        fs = setup(5)
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)
        assert fs.s_block[0].free_blocks == 5
        assert fs.s_block[0].num_blocks == 5
        teststring = "I am a little test"
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(teststring,"utf-8")))
        assert retval == 18 # the number of bytes written
        assert fs.inodes[1].direct_blocks[0] == 0 # the data should be written in the first possible block
        assert fs.free_list[0] == 0
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == teststring
        assert fs.data_blocks[0].size == 18
        assert fs.s_block[0].free_blocks == 4
        assert fs.s_block[0].num_blocks == 5

    # Try to write to a nonexisting file. Should return -1 and not touch any blocks
    def test_writef_file_not_found(self):
        fs = setup(5)
        teststring = "I am a little test"
        assert fs.s_block[0].free_blocks == 5
        assert fs.s_block[0].num_blocks == 5
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(teststring,"utf-8")))
        assert retval == -1 # returns
        assert fs.inodes[1].direct_blocks[0] == -1 # there is no file at inodes[1], thus its direct blocks are not changed
        assert fs.free_list[0] == 1 # free list is at default value because that block isnt touched
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value # should be an empty block
        assert outstring.decode("utf-8") == ""
        assert fs.s_block[0].free_blocks == 5
        assert fs.s_block[0].num_blocks == 5
        # added check to see if nested works (-> dir does not exist)
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/fil1","UTF-8")),ctypes.c_char_p(bytes(teststring,"utf-8")))
        assert retval == -1 # returns
        assert fs.s_block[0].free_blocks == 5
        assert fs.s_block[0].num_blocks == 5
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
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 5
        set_data_block_with_string(block_num=0, string_data="I am a test", parent_inode=1,parent_block_num=0,fs=fs)
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 4
        teststring = "I am a little test"
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil2","UTF-8")),ctypes.c_char_p(bytes(teststring,"utf-8")))
        assert retval == 18 # the number of bytes written
        assert fs.inodes[2].direct_blocks[0] == 1 # the data should be written in the first possible block which in this case is block 1
        assert fs.free_list[0] == 0
        assert fs.free_list[1] == 0
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 3
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[1].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == teststring

    # test append to 1 block
    def test_writef_append(self):
        fs = setup(5)
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 5
        teststring1 = "I am already here"
        set_data_block_with_string(block_num=0, string_data=teststring1, parent_inode=1,parent_block_num=0,fs=fs)
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 4
        teststring2 = "And I will be added"
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(teststring2,"utf-8")))
        assert retval == 19 # the number of bytes written
        assert fs.inodes[1].direct_blocks[0] == 0   # the data should be appended to the previously used block
        assert fs.inodes[1].direct_blocks[1] == -1  # so the second block should not be used
        assert fs.free_list[0] == 0                 # This is also represented in the free list
        assert fs.free_list[1] == 1
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 4
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == teststring1+teststring2

    # test to check if handeling of appending string (of size bigger than 1 block) fails
    def test_writef_append_more_than_BLOCK_SIZE(self):
        fs = setup(5)
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)
        fs = set_fil(name="fil2",inode=2,parent=0,parent_block=0,fs=fs)
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 5
        set_data_block_with_string(block_num=0, string_data="I am a test", parent_inode=1,parent_block_num=0,fs=fs)
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 4
        teststring = "And am already here"
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil2","UTF-8")),ctypes.c_char_p(bytes(teststring,"utf-8")))
        assert retval == 19
        assert fs.inodes[1].direct_blocks[0] == 0   # the data should be appended to the previously used block
        assert fs.inodes[1].direct_blocks[1] == -1  # so the second block should not be used
        assert fs.free_list[0] == 0                 # This is also represented in the free list
        assert fs.free_list[1] == 0
        assert fs.free_list[2] == 1
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 3
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[1].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == teststring
        teststring1 = LONG_DATA
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil2","UTF-8")),ctypes.c_char_p(bytes(teststring1,"utf-8")))
        assert retval == 1200 # the number of bytes written
        assert fs.inodes[2].direct_blocks[0] == 1 # the data should be written in the first possible block which in this case is block 1
        assert fs.inodes[2].direct_blocks[1] == 2
        assert fs.inodes[2].direct_blocks[2] == -1
        assert fs.inodes[2].direct_blocks[3] == -1
        assert fs.free_list[0] == 0
        assert fs.free_list[1] == 0
        assert fs.free_list[2] == 0
        assert fs.free_list[3] == 1
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 2
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == "I am a test"
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[1].block)).value #convert the raw data block to a string
        tmp = BLOCK_SIZE - len(teststring)
        assert outstring[:1024].decode("utf-8") == teststring+LONG_DATA[:tmp]
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[2].block)).value #convert the raw data block to a string
        assert outstring[:1024].decode("utf-8") == LONG_DATA[tmp:]
        assert fs.inodes[1].size == 11
        assert fs.inodes[2].size == 1219
        assert fs.data_blocks[0].size == 11
        assert fs.data_blocks[1].size == 1024
        assert fs.data_blocks[2].size == 195
        assert fs.data_blocks[3].size == 0

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

    # test to check what happens when data to write is empty
    def test_writef_no_data(self):
        fs = setup(5)
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)
        teststring = ""
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(teststring,"utf-8")))
        assert retval == 0 # the number of bytes written
        assert fs.inodes[1].direct_blocks[0] == -1   # the data should be appended to the previously used block
        assert fs.inodes[1].direct_blocks[1] == -1  # so the second block should not be used
        assert fs.free_list[0] == 1                 # This is also represented in the free list
        assert fs.free_list[1] == 1
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 5
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == ""
    
    # check writef for multiple writes
    def test_writef_multiple_writes(self):
        fs = setup(5)
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)
        teststring = "Hallo "
        teststring1 = "Welt "
        teststring2 = "Schoener "
        teststring3 = "TAG "
        teststring4 = "HEUTE!"
        teststring5 = ""
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(teststring,"utf-8")))
        assert retval == len(teststring) # the number of bytes written
        assert fs.inodes[1].direct_blocks[0] == 0   # the data should be appended to the previously used block
        assert fs.inodes[1].direct_blocks[1] == -1  # so the second block should not be used
        assert fs.free_list[0] == 0                 # This is also represented in the free list
        assert fs.free_list[1] == 1
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 4
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == teststring
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(teststring1,"utf-8")))
        assert retval == len(teststring1) # the number of bytes written
        assert fs.inodes[1].direct_blocks[0] == 0   # the data should be appended to the previously used block
        assert fs.inodes[1].direct_blocks[1] == -1  # so the second block should not be used
        assert fs.free_list[0] == 0                 # This is also represented in the free list
        assert fs.free_list[1] == 1
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 4
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == teststring + teststring1
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(teststring2,"utf-8")))
        assert retval == len(teststring2) # the number of bytes written
        assert fs.inodes[1].direct_blocks[0] == 0   # the data should be appended to the previously used block
        assert fs.inodes[1].direct_blocks[1] == -1  # so the second block should not be used
        assert fs.free_list[0] == 0                 # This is also represented in the free list
        assert fs.free_list[1] == 1
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 4
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == teststring + teststring1 + teststring2
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(teststring3,"utf-8")))
        assert retval == len(teststring3) # the number of bytes written
        assert fs.inodes[1].direct_blocks[0] == 0   # the data should be appended to the previously used block
        assert fs.inodes[1].direct_blocks[1] == -1  # so the second block should not be used
        assert fs.free_list[0] == 0                 # This is also represented in the free list
        assert fs.free_list[1] == 1
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 4
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == teststring + teststring1 + teststring2 + teststring3
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(teststring4,"utf-8")))
        assert retval == len(teststring4) # the number of bytes written
        assert fs.inodes[1].direct_blocks[0] == 0   # the data should be appended to the previously used block
        assert fs.inodes[1].direct_blocks[1] == -1  # so the second block should not be used
        assert fs.free_list[0] == 0                 # This is also represented in the free list
        assert fs.free_list[1] == 1
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 4
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == teststring + teststring1 + teststring2 + teststring3 + teststring4
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(teststring5,"utf-8")))
        assert retval == len(teststring5) # the number of bytes written
        assert fs.inodes[1].direct_blocks[0] == 0   # the data should be appended to the previously used block
        assert fs.inodes[1].direct_blocks[1] == -1  # so the second block should not be used
        assert fs.free_list[0] == 0                 # This is also represented in the free list
        assert fs.free_list[1] == 1
        assert fs.s_block[0].num_blocks == 5
        assert fs.s_block[0].free_blocks == 4
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == teststring + teststring1 + teststring2 + teststring3 + teststring4 + teststring5

    def test_writef_wrong_input(self):
        fs = setup(5)
        retval = libc.fs_writef(ctypes.byref(fs), None, None) 
        assert retval == -1
        retval = libc.fs_writef(None, None, None)
        assert retval == -1
        retval = libc.fs_writef(None, ctypes.c_char_p(bytes("/testDirectory","UTF-8")), None) # inode num 8
        assert retval == -1
        retval = libc.fs_writef(None, ctypes.c_char_p(bytes("/testDirectory","UTF-8")), ctypes.c_char_p(bytes("Hallo","utf-8"))) # inode num 8
        assert retval == -1
        retval = libc.fs_writef(None, None, ctypes.c_char_p(bytes("Hallo","utf-8"))) # inode num 8
        assert retval == -1
        retval = libc.fs_writef(ctypes.byref(fs), None, ctypes.c_char_p(bytes("Hallo","utf-8"))) # inode num 8
        assert retval == -1