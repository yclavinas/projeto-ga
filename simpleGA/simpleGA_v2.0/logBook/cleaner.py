#!/usr/bin/python
import re


def cleaner(file_entrada, file_saida):

	text = open(file_entrada, 'r')

	saveFile = open(file_saida+".txt", 'a')
	for line in text:
		data = re.sub(r'^[a-z].*$', '', line, flags=re.MULTILINE)
		# data = re.sub(r'\n', '', line, flags=re.MULTILINE)
		saveFile.write(data)
		saveFile.write('\n')


cleaner('2000 Uniform,roleta,polynomialBounded', "2000_Uniform")
cleaner('2001 Uniform,roleta,polynomialBounded', "2001_Uniform")
cleaner('2002 Uniform,roleta,polynomialBounded', "2002_Uniform")
cleaner('2003 Uniform,roleta,polynomialBounded', "2003_Uniform")
cleaner('2004 Uniform,roleta,polynomialBounded', "2004_Uniform")
cleaner('2005 Uniform,roleta,polynomialBounded', "2005_Uniform")
cleaner('2006 Uniform,roleta,polynomialBounded', "2006_Uniform")
cleaner('2007 Uniform,roleta,polynomialBounded', "2007_Uniform")
cleaner('2008 Uniform,roleta,polynomialBounded', "2008_Uniform")
cleaner('2009 Uniform,roleta,polynomialBounded', "2009_Uniform")
cleaner('2010 Uniform,roleta,polynomialBounded', "2010_Uniform")

cleaner('2000 blend,roleta,polynomialBounded', "2000_blend")
cleaner('2001 blend,roleta,polynomialBounded', "2001_blend")
cleaner('2002 blend,roleta,polynomialBounded', "2002_blend")
cleaner('2003 blend,roleta,polynomialBounded', "2003_blend")
cleaner('2004 blend,roleta,polynomialBounded', "2004_blend")
cleaner('2005 blend,roleta,polynomialBounded', "2005_blend")
cleaner('2006 blend,roleta,polynomialBounded', "2006_blend")
cleaner('2007 blend,roleta,polynomialBounded', "2007_blend")
cleaner('2008 blend,roleta,polynomialBounded', "2008_blend")
cleaner('2009 blend,roleta,polynomialBounded', "2009_blend")
cleaner('2010 blend,roleta,polynomialBounded', "2010_blend")

cleaner('2000 simulatedBinary,roleta,polynomialBounded', "2000_simulatedBinary")
cleaner('2001 simulatedBinary,roleta,polynomialBounded', "2001_simulatedBinary")
cleaner('2002 simulatedBinary,roleta,polynomialBounded', "2002_simulatedBinary")
cleaner('2003 simulatedBinary,roleta,polynomialBounded', "2003_simulatedBinary")
cleaner('2004 simulatedBinary,roleta,polynomialBounded', "2004_simulatedBinary")
cleaner('2005 simulatedBinary,roleta,polynomialBounded', "2005_simulatedBinary")
cleaner('2006 simulatedBinary,roleta,polynomialBounded', "2006_simulatedBinary")
cleaner('2007 simulatedBinary,roleta,polynomialBounded', "2007_simulatedBinary")
cleaner('2008 simulatedBinary,roleta,polynomialBounded', "2008_simulatedBinary")
cleaner('2009 simulatedBinary,roleta,polynomialBounded', "2009_simulatedBinary")
cleaner('2010 simulatedBinary,roleta,polynomialBounded', "2010_simulatedBinary")

cleaner('2000 simBinBounded,roleta,polynomialBounded', "2000_simBinBounded")
cleaner('2001 simBinBounded,roleta,polynomialBounded', "2001_simBinBounded")
cleaner('2002 simBinBounded,roleta,polynomialBounded', "2002_simBinBounded")
cleaner('2003 simBinBounded,roleta,polynomialBounded', "2003_simBinBounded")
cleaner('2004 simBinBounded,roleta,polynomialBounded', "2004_simBinBounded")
cleaner('2005 simBinBounded,roleta,polynomialBounded', "2005_simBinBounded")
cleaner('2006 simBinBounded,roleta,polynomialBounded', "2006_simBinBounded")
cleaner('2007 simBinBounded,roleta,polynomialBounded', "2007_simBinBounded")
cleaner('2008 simBinBounded,roleta,polynomialBounded', "2008_simBinBounded")
cleaner('2009 simBinBounded,roleta,polynomialBounded', "2009_simBinBounded")
cleaner('2010 simBinBounded,roleta,polynomialBounded', "2010_simBinBounded")


