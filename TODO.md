# Audiolib TODO

Overview of the TODOS for audiolib.

### General Todo

- [ ] Try to write plotting functionalities as pyplot wrappers
- [ ] Split functionalities in different modules
  (audiolib.plotting, audiolib.signal_processing, audiolib.utils, etc.)
- [ ] Write pytest routine

### File-specific Todo

audiolib.py:
- [ ] Fix MKFUNC for yscale around 0
  - [ ] Apply yscale after fixing
- [ ] Implement functionalities:
  - [ ] get_ir_from_rawdata
  - [ ] plot_rfft_ir: Maybe delete because get_ir_from_rfft and plot_frequency exist? Using those by on their own improves readability
  - [ ] get_ir_from_rawdata
- [ ] Write parser for wav data type to numpy.dtype


### In Progress

- [ ] Work on Github Repo [JIRA-345]  

### Done ✓

- [x] Create my first TODO.md  