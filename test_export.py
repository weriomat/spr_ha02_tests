import ctypes
from wrappers import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class Test_Exp:
    # Exports the content of a file in the fs to a new file
    # Expected behaviour:
    #  * The operation is successful, therefore retval is 0
    #  * The exported file contains the same data as the original file
    def test_export_file(self):
        fs = setup(5)
        fs = set_fil(name="fil1", inode=1, parent=0, parent_block=0, fs=fs)
        filename = create_temp_file(data=SHORT_DATA)
        retval = libc.fs_import(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")), ctypes.c_char_p(bytes(filename,"utf-8")))
        assert retval == 0

        exported_filename = os.path.join(SCRIPT_DIR, "exported_file.txt")
        retval = libc.fs_export(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")), ctypes.c_char_p(bytes(exported_filename,"utf-8")))
        assert retval == 0

        original_data = read_temp_file(filename)
        exported_data = read_temp_file(exported_filename)
        assert original_data == exported_data

        delete_temp_file(filename)
        delete_temp_file(exported_filename)

    # Exports a non-existing file
    # Expected behaviour:
    #  * The operation fails, therefore retval is -1
    def test_export_non_existing_file(self):
        fs = setup(5)
        retval = libc.fs_export(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")), ctypes.c_char_p(bytes("exported_file.txt","utf-8")))
        assert retval == -1

    # Exports a file from a non-existing directory
    # Expected behaviour:
    #  * The operation fails, therefore retval is -1
    def test_export_file_from_non_existing_directory(self):
        fs = setup(5)
        fs = set_fil(name="fil1", inode=1, parent=0, parent_block=0, fs=fs)
        retval = libc.fs_export(ctypes.byref(fs), ctypes.c_char_p(bytes("/non_existing_dir/fil1","UTF-8")), ctypes.c_char_p(bytes("exported_file.txt","utf-8")))
        assert retval == -1

    # Exports a file from a directory that is not a file
    # Expected behaviour:
    #  * The operation fails, therefore retval is -1
    def test_export_file_from_directory(self):
        fs = setup(5)
        fs = set_dir(name="dir1", inode=1, parent=0, parent_block=0, fs=fs)
        retval = libc.fs_export(ctypes.byref(fs), ctypes.c_char_p(bytes("/dir1","UTF-8")), ctypes.c_char_p(bytes("exported_file.txt","utf-8")))
        assert retval == -1

    # Exports a file that is empty
    # Expected behaviour:
    #  * The operation is successful, therefore retval is 0
    #  * The exported file is also empty
    def test_export_empty_file(self):
        fs = setup(5)
        fs = set_fil(name="fil1", inode=1, parent=0, parent_block=0, fs=fs)
        filename = create_temp_file(data="")
        retval = libc.fs_import(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")), ctypes.c_char_p(bytes(filename,"utf-8")))
        assert retval == 0

        exported_filename = os.path.join(SCRIPT_DIR, "exported_file.txt")
        retval = libc.fs_export(ctypes.byref(fs), ctypes.c_char_p(bytes("/fil1","UTF-8")), ctypes.c_char_p(bytes(exported_filename,"utf-8")))
        assert retval == 0

        exported_data = open(exported_filename, "rb").read() # Read the exported file as bytes
        exported_data = exported_data[:0] # needed reassignment because there is no terminating 0 byte in the data block
        assert exported_data == b""

        delete_temp_file(filename)
        delete_temp_file(exported_filename)

