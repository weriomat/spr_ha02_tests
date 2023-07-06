import ctypes
from wrappers import *


class Test_Imp:
    # Creates a file, fills it with some short text, then imports it to an existing (empty) file in the fs
    # Expected behaviour:
    #  * The operation is successful, therefor retval is 0
    #  * The test data is located in the first datablock
    #  * the filesize and the datablock size are set correctly (to the length of text in the file)
    #  * the first datablock is marked as blocked in the free list
    def test_import_simple(self):
        fs = setup(5)
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)
        filename = create_temp_file(data=SHORT_DATA)
        retval = libc.fs_import(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(filename,"utf-8")))

        assert retval == 0
        assert fs.inodes[1].direct_blocks[0] == 0 # the data should be written in the first possible block
        assert fs.free_list[0] == 0
        outstring = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value #convert the raw data block to a string
        assert outstring.decode("utf-8") == SHORT_DATA
        assert fs.data_blocks[0].size == len(SHORT_DATA)
        assert fs.inodes[1].size == len(SHORT_DATA)

        delete_temp_file()


    def test_import_bigger_file(self):
        fs = setup(5)
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)
        filename = create_temp_file(data=LONG_DATA)
        retval = libc.fs_import(ctypes.byref(fs),ctypes.c_char_p(bytes("/fil1","UTF-8")),ctypes.c_char_p(bytes(filename,"utf-8")))

        assert retval == 0
        assert fs.inodes[1].direct_blocks[0] == 0 # the data should be written in the first possible block
        assert fs.inodes[1].direct_blocks[1] == 1 # and the second block
        assert fs.free_list[0] == 0
        assert fs.free_list[1] == 0

        outstring1 = bytearray(ctypes.c_char_p(ctypes.addressof(fs.data_blocks[0].block)).value) #convert the raw data block to a string
        outstring1 = outstring1[:1024] # needed reassignment because there is no terminating 0 byte in the data block
        outstring2 = ctypes.c_char_p(ctypes.addressof(fs.data_blocks[1].block)).value #convert the raw data block to a string
        assert outstring1.decode("utf-8")+outstring2.decode("utf-8") == LONG_DATA
        delete_temp_file()


    # TODO: add test for failing operations
