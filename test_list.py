import ctypes
from wrappers import *

class Test_List:
    def test_list_one_dir(self):
        fs = setup(5)
        fs = set_dir(name="newDir",inode=1,parent=0,parent_block=0,fs=fs)
        libc.fs_list.restype = ctypes.c_char_p
        retval = libc.fs_list(ctypes.byref(fs), ctypes.c_char_p(bytes("/","UTF-8")))
        assert retval.decode("utf-8") == "DIR newDir\n"

    def test_list_one_file(self):
        fs = setup(5)
        fs = set_fil(name="newFil",inode=1,parent=0,parent_block=0,fs=fs)
        libc.fs_list.restype = ctypes.c_char_p
        retval = libc.fs_list(ctypes.byref(fs), ctypes.c_char_p(bytes("/","UTF-8")))
        assert retval.decode("utf-8") == "FIL newFil\n"

    def test_list_dir_nested(self):
        fs = setup(5)
        fs = set_dir(name="newDir",inode=1,parent=0,parent_block=0,fs=fs)
        fs = set_dir(name="nestedDir",inode=2,parent=1,parent_block=0,fs=fs)
        libc.fs_list.restype = ctypes.c_char_p
        retval = libc.fs_list(ctypes.byref(fs), ctypes.c_char_p(bytes("/newDir","UTF-8")))
        assert retval.decode("utf-8") == "DIR nestedDir\n"

    def test_list_multiple_files(self):
        fs = setup(10)
        fs = set_dir(name="Dir1",inode=1,parent=0,parent_block=0,fs=fs)
        fs = set_dir(name="Dir2",inode=2,parent=0,parent_block=1,fs=fs)
        fs = set_dir(name="Dir3",inode=3,parent=0,parent_block=2,fs=fs)
        fs = set_fil(name="Fil1",inode=4,parent=0,parent_block=3,fs=fs)
        fs = set_fil(name="Fil2",inode=5,parent=0,parent_block=4,fs=fs)

        libc.fs_list.restype = ctypes.c_char_p
        retval = libc.fs_list(ctypes.byref(fs), ctypes.c_char_p(bytes("/","UTF-8")))
        assert retval.decode("utf-8") == "DIR Dir1\nDIR Dir2\nDIR Dir3\nFIL Fil1\nFIL Fil2\n"
    def test_list_nested_complex(self):
        fs = setup(10)
        fs = set_dir(name="tmp",inode=1,parent=0,parent_block=0,fs=fs) # 1 -> /tmp
        fs = set_dir(name="parent",inode=2,parent=1,parent_block=0,fs=fs) # 2 -> /tmp/parent
        libc.fs_list.restype = ctypes.c_char_p
        retval = libc.fs_list(ctypes.byref(fs), ctypes.c_char_p(bytes("/tmp","UTF-8")))
        assert retval.decode("utf-8") == "DIR parent\n"
        fs = set_dir(name="par",inode=3,parent=1,parent_block=1,fs=fs) # 3 /tmp/par
        retval = libc.fs_list(ctypes.byref(fs), ctypes.c_char_p(bytes("/tmp","UTF-8")))
        assert retval.decode("utf-8") == "DIR parent\nDIR par\n"
        fs = set_dir(name="test",inode=4,parent=3,parent_block=0,fs=fs) # /tmp/par/test
        fs = set_fil(name="test",inode=5,parent=3,parent_block=1,fs=fs) # /tmp/par/test
        retval = libc.fs_list(ctypes.byref(fs), ctypes.c_char_p(bytes("/tmp/par","UTF-8")))
        assert retval.decode("utf-8") == "DIR test\nFIL test\n"
    def test_list_nested_multiple(self):
        fs = setup(10)
        fs = set_dir(name="parent",inode=1,parent=0,parent_block=0,fs=fs)
        fs = set_dir(name="parent",inode=2,parent=1,parent_block=0,fs=fs)
        libc.fs_list.restype = ctypes.c_char_p
        retval = libc.fs_list(ctypes.byref(fs), ctypes.c_char_p(bytes("/parent","UTF-8")))
        assert retval.decode("utf-8") == "DIR parent\n"
        fs = set_dir(name="par",inode=3,parent=1,parent_block=1,fs=fs)
        fs = set_fil(name="par",inode=4,parent=1,parent_block=2,fs=fs)
        retval = libc.fs_list(ctypes.byref(fs), ctypes.c_char_p(bytes("/parent","UTF-8")))
        assert retval.decode("utf-8") == "DIR parent\nDIR par\nFIL par\n"
        fs = set_fil(name="parent",inode=5,parent=1,parent_block=3,fs=fs)
        fs = set_dir(name="idk",inode=6,parent=1,parent_block=4,fs=fs)
        retval = libc.fs_list(ctypes.byref(fs), ctypes.c_char_p(bytes("/parent","UTF-8")))
        assert retval.decode("utf-8") == "DIR parent\nDIR par\nFIL par\nFIL parent\nDIR idk\n"
