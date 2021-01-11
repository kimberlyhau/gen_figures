# gen_figures
Requirements and General Info for generate_fig.py
1. Plots 1 to 3 sequences.
2. To adjust dimensions of figure, change gridwidth (line 8). Font sizes must be modified separately.
3. To adjust location of figure in pdf, change the initial values in gridhor and gridvert lists (lines 9 and 10).
4. Adjust pdf size on line 26 (setPageSize).
5. Assumes csv files, intervals can span over max. 2 months.
6. Requires reportlab to be installed.


How to run:
1. Add names of input files to filenames list in main (line 124)
2. Change pdf name on line 7
