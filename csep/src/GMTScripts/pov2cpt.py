#!/usr/bin/env python

############################################################################
#    Copyright (C) 2007 by Danijel Schorlemmer                             #
#    ds@usc.edu                                                            #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

import sys
import getopt
from math import floor
import re

def main():
  # Set defaults
  fMin = 0
  fMax = 1
  bExtent = False
  bFlip = False
  bInteger = False
  bOutput2Standard = True
  vNaNColor = [0, 0, 0]
  bNaNColor = False
  sCptFilename = ''
  # Read commandline arguments
  sCmdParams = sys.argv[1:]
  opts, args = getopt.gnu_getopt(sCmdParams, 'a:b:efhil:n:o:', ['min=', 'max=', 'extend', 'flip', 'help', 'integer', 'length=', 'nan=', 'output='])
  for option, parameter in opts:
    if option == '-a' or option == '--min':
      fMin = float(parameter)
    if option == '-b' or option == '--max':
      fMax = float(parameter)
    if option == '-e' or option == '--extend':
      bExtent = True
    if option == '-f' or option == '--flip':
      bFlip = True
    if option == '-i' or option == '--integer':
      bInteger = True
    if option == '-n' or option == '--nan':
      bNaNColor = True
      vRGB = re.split(r'/', parameter)
      if vRGB:
        vNaNColor[0] = float(vRGB[0])
        vNaNColor[1] = float(vRGB[1])
        vNaNColor[2] = float(vRGB[2])
    if option == '-o' or option == '--output':
      bOutput2Standard = False
      sCptFilename = parameter
    if option == '-h' or option == '--help':
      print 'Convert PovRay-colorbars (exported from GIMP) to cpt-files for GMT'
      print 'Version 1.0 [07.04.2008]'
      print 'Usage: pov2cpt.py [OPTION] povray-file'
      print '   -a, --min=<value>        minimum value on colorbar (default = 0)'
      print '   -b, --max=<value>        maximum value on colorbar (default = 1)'
      print '   -e, --extent             extent colorbar (F/B values)'
      print '   -f, --flip               flip colorbar'
      print '   -h, --help               print this information'
      print '   -i, --integer            output color values as integer'
      print '   -n, --nan=<r/g/b>        defines the N-entry at the end of a cpt-file'
      print '   -o, --output=<filename>  output to file instead of stdout'
      sys.exit()
  sPovRayFilename = args[0]
  mColormap = ReadPovRay(sPovRayFilename)
  if bFlip:
    mColormap = Flip(mColormap)
  mCpt = Scale(mColormap, fMin, fMax)
  mCpt = PrepareForWriting(mCpt)
  WriteCpt(bOutput2Standard, sCptFilename, mCpt, bExtent, bNaNColor, vNaNColor, bInteger)

# ---

def Scale(mColormap, fMin, fMax):

  fDiff = fMax - fMin
  nLen = len(mColormap[0])
  for nCnt in range(0, nLen):
    mColormap[0][nCnt] = fMin + (float(mColormap[0][nCnt]) * fDiff)
  return mColormap

# ---

def PrepareForWriting(mCpt):

  mColormap = [[], [], [], [], [], [], [], []]
  nLen = len(mCpt[0])
  for nCnt in range(0, nLen-1):
    mColormap[0].append(mCpt[0][nCnt])
    mColormap[1].append(mCpt[1][nCnt])
    mColormap[2].append(mCpt[2][nCnt])
    mColormap[3].append(mCpt[3][nCnt])
    mColormap[4].append(mCpt[0][nCnt+1])
    mColormap[5].append(mCpt[1][nCnt+1])
    mColormap[6].append(mCpt[2][nCnt+1])
    mColormap[7].append(mCpt[3][nCnt+1])
  return mColormap

# ---

def Flip(mColormap):

  mColormap[0].reverse()
  mColormap[0] = [1.0 - float(item) for item in mColormap[0]]
  mColormap[1].reverse()
  mColormap[2].reverse()
  mColormap[3].reverse()
  return mColormap

# ---

def IsUsed(sLine):

  if ((sLine[0] == "/") or (sLine[0] == "c") or (sLine[0] == "}")):
    return False
  else:
    return True

# ---

def ConvertLine(sLine):

  vLine = [sLine[2:9], sLine[23:30], sLine[33:40], sLine[43:50]]
  vLine[1] = float(vLine[1]) * 255;
  vLine[2] = float(vLine[2]) * 255;
  vLine[3] = float(vLine[3]) * 255;
  return vLine

# ---

def ReadPovRay(sFilename):

  mData = [[], [], [], []]
  sPreviousLine = ''
  ftInput = file(sFilename, "r")
  for sLine in ftInput.readlines():
    if IsUsed(sLine):
      if (sLine != sPreviousLine):
        vDataLine = ConvertLine(sLine)
        mData[0].append(vDataLine[0])
        mData[1].append(vDataLine[1])
        mData[2].append(vDataLine[2])
        mData[3].append(vDataLine[3])
        sPreviousLine = sLine
  return mData

# ---

def WriteCpt(bOutput2Standard, sFilename, mCpt, bExtent, bNaNColor, vNaNColor, bInteger):

  if bOutput2Standard:
    ftOutput = sys.stdout
  else:
    ftOutput = file(sFilename, "w")
  nLen = len(mCpt[0])
  if bInteger:
    for nCnt in range(0, nLen):
      for nItem in range(1, 4):
        mCpt[nItem][nCnt] = int(mCpt[nItem][nCnt])
      for nItem in range(5, 8):
        mCpt[nItem][nCnt] = int(mCpt[nItem][nCnt])
  sColorBottom = str(mCpt[1][0]) + '\t' + str(mCpt[2][0]) + '\t' + str(mCpt[3][0])
  sColorTop    = str(mCpt[5][nLen-1]) + '\t' + str(mCpt[6][nLen-1]) + '\t' + str(mCpt[7][nLen-1])
  for nCnt in range(0, nLen):
    sLine = str(mCpt[0][nCnt]) + '\t' + str(mCpt[1][nCnt]) + '\t' + str(mCpt[2][nCnt]) + '\t' + str(mCpt[3][nCnt]) + '\t' + str(mCpt[4][nCnt]) + '\t' + str(mCpt[5][nCnt]) + '\t' + str(mCpt[6][nCnt]) + '\t' + str(mCpt[7][nCnt])
    ftOutput.write(sLine + '\n')
  if bExtent:
    ftOutput.write('F\t' + sColorTop + '\n')
    ftOutput.write('B\t' + sColorBottom + '\n')
  else:
    ftOutput.write('F\t-\t-\t-\n')
    ftOutput.write('B\t-\t-\t-\n')
  if bNaNColor:
    if bInteger:
      sLine = 'N\t' + str(int(vNaNColor[0])) + '\t' + str(int(vNaNColor[1])) + '\t' + str(int(vNaNColor[2])) + '\n'
    else:
      sLine = 'N\t' + str(vNaNColor[0]) + '\t' + str(vNaNColor[1]) + '\t' + str(vNaNColor[2]) + '\n'
  else:
    sLine = 'N\t-\t-\t-\n'
  ftOutput.write(sLine)

main()


# PovRay-export example

#/* color_map file created by the GIMP */
#/* http://www.gimp.org/               */
#color_map {
#	[0.000000 color rgbt <0.128028, 0.725490, 0.128028, 0.000000>]
#	[0.168005 color rgbt <0.564014, 0.862745, 0.564014, 0.000000>]
#	[0.333333 color rgbt <1.000000, 1.000000, 1.000000, 0.000000>]
#	[0.333333 color rgbt <1.000000, 1.000000, 1.000000, 0.000000>]
#	[0.500678 color rgbt <0.996078, 0.904645, 0.538908, 0.000000>]
#	[0.668022 color rgbt <0.992157, 0.809289, 0.077816, 0.000000>]
#	[0.668022 color rgbt <0.992157, 0.809289, 0.077816, 0.000000>]
#	[0.834011 color rgbt <0.970588, 0.449304, 0.174595, 0.000000>]
#	[1.000000 color rgbt <0.949020, 0.089319, 0.271374, 0.000000>]
#} /* color_map */
