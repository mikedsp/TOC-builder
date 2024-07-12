# TOC-builder
Python program that builds a table of contents for a PDF file that does not have a table of contents

The file, create_toc.py, is a Python program designed to be run from the command line. The program creates a table of contents text file called, refined_table_of_contents.txt, for an input file called 2025 PFS QPP NPRM -14828.pdf. Both files must be in the same folder. 

This program was designed to help analyze Federal Regulations that are released in PDF form without a table of contents. 

The program did not get every section header in the input file correct, but it got the large majority of the headers and pages correct. 

The program, create_toc_in_csv.py, outputs the table of contents into a .csv file with the section header in the first column and the page number in the second column. It doesn’t get every header and page number correct, but gets the large majority correct. 

For instructions on how to run the python programs, see README.docx.
