import ctypes
from wrappers import *

libc.fs_readf.restype = ctypes.c_char_p

class Test_Readf:
    # Sets up a single file with some short data then uses the readf-function to retrieve tat data
    # Expected outcome:
    #  * returned string matches the string that was previously set
    #  * data length is correctly set
    def test_readf_simple(self):
        fs = setup(5)
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)
        fs = set_data_block_with_string(block_num=0,string_data=SHORT_DATA,parent_inode=1,parent_block_num=0,fs=fs)
        file_length = ctypes.c_int(0)
        retval = libc.fs_readf(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","utf-8")),ctypes.byref(file_length))

        assert file_length.value == len(SHORT_DATA)
        assert retval[:len(SHORT_DATA)].decode("utf-8") == SHORT_DATA

    def test_readf_long_data_consecutive_blocks(self):
        fs = setup(5)
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)
        fs = set_data_block_with_string(block_num=0,string_data=LONG_DATA[:1024],parent_inode=1,parent_block_num=0,fs=fs)
        fs = set_data_block_with_string(block_num=1,string_data=LONG_DATA[1024:],parent_inode=1,parent_block_num=1,fs=fs)
        file_length = ctypes.c_int(0)
        retval = libc.fs_readf(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","utf-8")),ctypes.byref(file_length))

        assert file_length.value == len(LONG_DATA)
        assert retval[:len(LONG_DATA)].decode("utf-8") == LONG_DATA
        
    def test_readf_long_data_unconsecutive_blocks(self):
        fs = setup(5)
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)
        fs = set_data_block_with_string(block_num=4,string_data=LONG_DATA[:1024],parent_inode=1,parent_block_num=0,fs=fs)
        fs = set_data_block_with_string(block_num=3,string_data=LONG_DATA[1024:],parent_inode=1,parent_block_num=1,fs=fs)

        file_length = ctypes.c_int(0)
        retval = libc.fs_readf(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","utf-8")),ctypes.byref(file_length))

        assert file_length.value == len(LONG_DATA)
        assert retval[:len(LONG_DATA)].decode("utf-8") == LONG_DATA
    
    def test_readf_empty_file(self):
        fs = setup(5)
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)

        file_length = ctypes.c_int(0)
        retval = libc.fs_readf(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","utf-8")),ctypes.byref(file_length))

        assert file_length.value == 0
        assert retval == None

    def test_readf_nonexisting_file(self):
        fs = setup(5)

        file_length = ctypes.c_int(0)
        retval = libc.fs_readf(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","utf-8")),ctypes.byref(file_length))

        assert file_length.value == 0
        assert retval == None
        # test wrong path
        file_length = ctypes.c_int(0)
        retval = libc.fs_readf(ctypes.byref(fs), ctypes.c_char_p(bytes("fil1","utf-8")),ctypes.byref(file_length))

        assert file_length.value == 0
        assert retval == None

    # !useless: but iam to bored to fix it -> check if BLOCK is null char
    def test_readf_NULL_in_string(self):
        fs = setup(5)
        teststring = "Hallo NULL der string soll hier aber noch weitergehen!"
        fs = set_fil(name="fil1",inode=1,parent=0,parent_block=0,fs=fs)
        fs = set_data_block_with_string(block_num=0,string_data=teststring,parent_inode=1,parent_block_num=0,fs=fs)
        file_length = ctypes.c_int(0)
        retval = libc.fs_readf(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","utf-8")),ctypes.byref(file_length))
        assert file_length.value == len(teststring)
        assert retval.decode("utf-8") == teststring
