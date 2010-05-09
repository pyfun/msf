import csv
import numpy as np

areader = csv.reader(open('Table.txt'),delimiter='\t')
areader.next()
data = [[row[0],row[1].strip(),row[11],row[13],row[14],row[3],
         row[7],row[16]] for row in areader
        if (not row[2].startswith('--'))]


                                                
