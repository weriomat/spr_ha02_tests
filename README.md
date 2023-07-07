# Tests for spr_ha_02

## Damit der Test test_rem funktioniert muss auch wrappers.py geupdated werden
Habe da eine recht triviale Änderung vorgenommen und angepasst, dass wenn ein data_block mit set_data_block gesetzt wird auch fs->s_block->free_blocks angepasst werden. Frage mich wieso das nicht schon da war, aber egal (denke mal wurde einfach vergessen lol)

### Documentation is miss cuz i cant be bothered
