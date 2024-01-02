# Audiolib TODO

Overview of the TODOS for audiolib.

### General Todo

- [ ] Write README.md
- [ ] Try to write plotting functionalities as pyplot wrappers
- [ ] Split functionalities in different modules
  (audiolib.plotting, audiolib.signal_processing, audiolib.utils, etc.)
    - [ ] First step: Change structure to "src-layout". This makes an
          installation of the package necessary to run it, but the plan
          is to develop a "portable" subpackage or "portable" repository.
          Use of src is recommended for the following reasons:
          https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/#src-layout-vs-flat-layout
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

### Done ✓

- [x] Create TODO.md  
