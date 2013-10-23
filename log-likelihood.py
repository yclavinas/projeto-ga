f = open('jma_cat_2000_2012_Mth2.5_formatted.dat', 'r')
print f

minimo = 328.8847
maximo = 0

print 'Longitude Latitude Year  M  D Mag    Depth  H  M  S'
for line in f:
        print line
        data = str.split(line)
        print data[0]
        print data[1]
        raw_input("Press Enter to continue...")


f.close(f)
