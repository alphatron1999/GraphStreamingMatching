import sys
from scipy.io import mmread
import random

in_file_name = sys.argv[1]
matr = mmread(in_file_name)
out_file_name = in_file_name[:-3]+'txt'
f = open(out_file_name,'w')
rows, cols = matr.shape
f.write(str(rows)+" "+str(rows+cols)+"\n")
f.write(str(rows+cols)+" "+str(len(matr.data))+"\n")
dl = list(zip(matr.row, matr.col, matr.data))
random.shuffle(dl)
for i,j,v in dl:    
    f.write(str(i)+" "+str(rows+j)+"\n")
f.close()