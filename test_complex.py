import ctypes
import hashlib
from wrappers import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class Test_Complex:

    # Creates a file then deletes it. The inode should be set to "free" again
    def test_complex_create_and_delete_easy(self):
        fs = setup(5)
        libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8")))
        retval = libc.fs_rm(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].n_type == 3, "The inode should be set as 'free'==3"
        assert fs.inodes[0].direct_blocks[0] == -1, "The parent node should not point to the file anymore"

    # Creates a file, puts data in it then deletes it. The inode should be set to "free" again
    def test_complex_create_write_delete(self):
        fs = setup(5)
        libc.fs_mkfile(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8")))
        fs = set_data_block_with_string(block_num = 0, string_data=SHORT_DATA,parent_inode = 1,parent_block_num = 0, fs=fs)
        retval = libc.fs_rm(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory","UTF-8")))
        assert retval == 0
        assert fs.inodes[1].n_type == 3, "The inode should be set as 'free'==3"
        assert fs.inodes[0].direct_blocks[0] == -1, "The parent node should not point to the file anymore"
        assert fs.free_list[0] == 1, "The free list needs to be updated when a file that holds data is removed"

    # Imports a picture file and exports it with a different name
    def test_complex_import_export_picture(self):
        fs = setup(20)
        fs = set_dir(name="testDirectory", inode=1, parent=0, parent_block=0, fs=fs)
        fs = set_fil(name="file1", inode=2, parent=1, parent_block=0, fs=fs)

        # Import the file
        import_filename = os.path.join(SCRIPT_DIR, "success.jpg")
        retval = libc.fs_import(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/file1","UTF-8")), ctypes.c_char_p(bytes(import_filename,"utf-8")))
        assert retval == 0

        # Export the file with a different name
        export_filename = os.path.join(SCRIPT_DIR, "exported_file.jpg")
        retval = libc.fs_export(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/file1","UTF-8")), ctypes.c_char_p(bytes(export_filename,"utf-8")))
        assert retval == 0

        # Verify that the exported file exists
        assert os.path.exists(export_filename)

        # Verify that the exported file is still the same as the imported file
        import_file_hash = hashlib.md5(open(import_filename, "rb").read()).hexdigest()
        export_file_hash = hashlib.md5(open(export_filename, "rb").read()).hexdigest()
        assert import_file_hash == export_file_hash, "The exported file and the imported original file are not identical"

    # Imports a file, appends data to it, and exports it with a different name
    def test_complex_import_append_export_rename(self):
        fs = setup(20)
        fs = set_dir(name="testDirectory", inode=1, parent=0, parent_block=0, fs=fs)
        fs = set_fil(name="file1", inode=2, parent=1, parent_block=0, fs=fs)

        # Import the file
        import_filename = os.path.join(SCRIPT_DIR, "import.txt")
        retval = libc.fs_import(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/file1","UTF-8")), ctypes.c_char_p(bytes(import_filename,"utf-8")))
        assert retval == 0

        # Append data to the imported file
        append_data = "Alles tip top!"
        retval = libc.fs_writef(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/file1","UTF-8")), ctypes.c_char_p(bytes(append_data, "utf-8")))
        assert retval == len(append_data)

        # Export the file with a different name
        export_filename = os.path.join(SCRIPT_DIR, "exported_file.txt") # wird bei mir lokal nicht in /tests gespeichert sondern eins drüber ¯\_(ツ)_/¯
        retval = libc.fs_export(ctypes.byref(fs), ctypes.c_char_p(bytes("/testDirectory/file1","UTF-8")), ctypes.c_char_p(bytes(export_filename,"utf-8")))
        assert retval == 0

        # Verify that the exported file exists
        assert os.path.exists(export_filename)

# TODO: Maybe think of more tests
