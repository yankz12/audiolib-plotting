# Audiolib TODO

Overview of the TODOS for audiolib.

### General Todo

- [ ] Start object-orientated architecture
- [ ] Find a solution for portable version (w/o pip installation)
- [ ] Try to write plotting functionalities as pyplot wrappers
- [ ] Write pytest routine

### File-specific Todo

audiolib.py:
- [ ] Write parser for wav data type to numpy.dtype

### In Progress

### Done ✓

- [x] Implement functionalities:
  - [x] get_ir_from_rawdata
  - [x] plot_rfft_ir: Maybe delete because get_ir_from_rfft and plot_frequency exist? Using those by on their own improves readability
- [x] Fix MKFUNC for yscale around 0
  - [x] Apply yscale after fixing
- [x] Split functionalities in different modules
  (audiolib.plotting, audiolib.signal_processing, audiolib.utils, etc.)
    - [x] First step: Change structure to "src-layout". This makes an
          installation of the package necessary to run it, but the plan
          is to develop a "portable" subpackage or "portable" repository.
          Use of src is recommended for the following reasons:
          https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/#src-layout-vs-flat-layout
- [x] Write README.md
- [x] Create TODO.md  
