import os
wd = os.getcwd()

fname = "QMHBS-Hasselman_postman.txt"

while open(fname, mode = 'r') as f:
    codes = file.readlines()

print codes