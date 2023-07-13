# Tests for spr_ha_02

## Capability: test_mkdir, test_mkfile, test_list, test_rem, test_complex, test_import, text_export, test_readf, test_writef
If u find other edge cases just msg and we will work it out

## test_MkdirMkfile/ test_MkfileRmWriteRead contains test cases we do not have to cover -> if u have errors dont msg me just read description

## TODO: test_import, test_export, maybe add tests for NULL inputs but i cant be bothered lol

## Damit der Test test_rem funktioniert muss auch wrappers.py geupdated werden
Habe da eine recht triviale Änderung vorgenommen und angepasst, dass wenn ein data_block mit set_data_block gesetzt wird auch fs->s_block->free_blocks angepasst werden. Frage mich wieso das nicht schon da war, aber egal (denke mal wurde einfach vergessen lol)

### Documentation is missing cuz i cant be bothered
