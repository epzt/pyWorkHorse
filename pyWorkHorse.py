#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
import struct as st
import argparse as ap
import datetime

from utils.pyGeneralClass import *

# convenience function reused for header, length, and checksum
def __nextLittleEndianUnsignedShort(file):
   """Get next little endian unsigned short from file"""
   raw = file.read(2)
   return (raw, st.unpack('<H', raw)[0])

# factored for readability
def __computeChecksum(header, length, ensemble):
   """Compute a checksum from header, length, and ensemble"""
   cs = 0
   for byte in header:
      cs += byte
   for byte in length:
      cs += byte
   for byte in ensemble:
      cs += byte
   return cs & 0xffff

#----------------------------------------
#-  Date validation for input parameter -
#----------------------------------------
def valid_datetime_type(arg_datetime_str):
   """custom argparse type for user datetime values given from the command line"""
   try:
      return datetime.datetime.strptime(arg_datetime_str, "%d-%m-%Y %H:%M:%S.%f")
   except ValueError:
      msg = "Given Datetime ({0}) not valid! Expected format, 'dd-mm-YYYY hh:mm:ss.ss'!".format(arg_datetime_str)
      raise ap.ArgumentTypeError(msg)

#----------------------------------------
#---           MAIN                   ---
#----------------------------------------
def main():
   # Parameters management
   parser = ap.ArgumentParser()
   parser.add_argument('-i', '-infile',
                        dest='infile', 
                        required=True,
                        help="ADCP file to read")
   parser.add_argument('-o', '-outfile',
                        dest='outfile', 
                        required=False,
                        default='./export-ADCP.txt',
                        help="ADCP file to write. Default is <export-ADCP.txt>")
   parser.add_argument('-s', '--start-datetime',
                        dest='start_datetime',
                        type=valid_datetime_type,
                        default=None,
                        required=False,
                        help='start datetime in format "dd-mm-YYYY hh:mm:ss.ss"')
   parser.add_argument('-e', '--end-datetime',
                        dest='end_datetime',
                        type=valid_datetime_type,
                        default=None,
                        required=False,
                        help='end datetime in format "dd-mm-YYYY hh:mm:ss.ss"')
   parser.add_argument("-c", "--count",
                        dest='count',
                        type=int,
                        default=-1,
                        help="Number of element to read")
   parser.add_argument("-size", "--size",
                        dest='size',
                        type=int,
                        default=0,
                        required=False,
                        help='split output file every <size> kilo bytes. Default=0 (not split)')
   parser.add_argument("-sys", "--system",
                        dest='coordinatesystem',
                        default='BEAM',
                        required=False,
                        help='Coordinate system for velocities. Default: BEAM. Valid values: BEAM, INSTRUMENT, EARTH')
   parser.add_argument("-b", "--binary",
                        dest='binary',
                        type=bool,
                        default=False,
                        help="Outputs in binary format for numpy use")
   parser.add_argument("-d", "--data",
                        dest='data',
                        default='VEL,INT,PG,CORR',
                        help="Data output: Default: VEL,INT,PG,CORR. VEL: velocity, INT: intensity, PG: percent good, \
                        CORR: correlation. Choose a combination of data separated by a comma.")
   args = parser.parse_args()
   
   # Test validity of date time if given
   if args.start_datetime != None and args.end_datetime != None:
      if args.start_datetime > args.end_datetime:
         msg = "Start date can not be after end date !"
         raise ap.ArgumentTypeError(msg)
         
   if args.start_datetime == None and args.end_datetime != None:
      msg = "End date is given but start date is not given\n\tYou should provide both dates"
      raise ap.ArgumentTypeError(msg)
      
   # Test validity of ADCP file name
   if not os.path.isfile(args.infile):
      raise IOError('%s is not a valid file ADCP file name' % args.infile)
   # Opening the ADCP file
   try:
      infile = open(args.infile,'rb')
   except:
      raise IOError('Unable to open file {}'.format(args.infile))
   # Set default name of output file if needed
   if args.outfile == './export-ADCP.txt':
            args.outfile = './export-{}.{}'.format(args.infile.split('.')[0],'txt')
   # Test and open output file
   try:
      if args.binary:
            outfile = open(args.outfile, 'wb')
      else:
            outfile = open(args.outfile,'w')
   except:
      raise IOError('Unable to create file {}'.format(args.outfile))

   # Test validity of coordinate system
   if (args.coordinatesystem != 'BEAM') & (args.coordinatesystem != 'INSTRUMENT') & (args.coordinatesystem != 'EARTH'):
      msg = 'Invalid coordinate system ({}). Valid value: BEAM, INSTRUMENT, EARTH'.format(args.coordinatesystem)
      raise ap.ArgumentTypeError(msg)
   coordSystem = args.coordinatesystem

   # End of argument management

   # Variable initiatilization
   # Number of element written
   elementCount = 0
   # Control of the file size
   outfileSize = 0
   # Control of the file number (in case of multiple files)
   fileCount = 0

   # Retreive first element of interest, i.e. wave or current
   firstCurrents, firstWaves = getFirstWavesCurrentsID(infile)
   
   # get the starting point by throwing out unfound headers
   # and selecting the minumum
   firstEnsemble = min(filter(lambda x: x >= 0,(firstWaves,firstCurrents)))

   #seeks to the first occurence of a waves or currents data
   infile.seek(firstEnsemble-2)

   # Get file information: file size
   #fileSize = os.stat(args.infile).st_size

   # Read header ID
   rawHeader, header = __nextLittleEndianUnsignedShort(infile)
   # loop through raw data
   while (header == WAVESID) or (header == PD0HEADERID):
      # print statistics
      #sys.stdout.write("{:2.1}%\r".format(str((infile.tell()/fileSize)*100.0)))
      #sys.stdout.flush()

      # get ensemble length
      rawLength, length = __nextLittleEndianUnsignedShort(infile)

      # TODO: deal with wave data also
      # actually just jump to next ensemble
      if header == WAVESID:
         print("Wave data found\n")
         infile.seek(length+2,1)
         continue

      # read up to the checksum
      rawEnsemble = infile.read(length-4)

      # Read the current ensemble and get the data
      re = readEnsemble(rawEnsemble)
      re.readEnsembleData()
     
      nbDataTypes = re.getEnsembleItem(0).GetNbDataTypes()
      if nbDataTypes > 100:
         raise IOError('Incorrect number of data types ({})'.format(nbDataTypes))

      # Manage actions
      if args.end_datetime != None and args.start_datetime != None:
         if re.getEnsembleItem(2).getStartDateTime() > args.start_datetime and re.getEnsembleItem(2).getStartDateTime() < args.end_datetime :
            if args.count != -1:
               if elementCount < args.count:
                  # both dates and a count
                  outfile.write('{}'.format(re.write(coordSystem)))
                  elementCount = elementCount + 1
                  if args.size > 0:
                     outfileSize = outfile.tell()
               else:
                  break
            else:
               # both dates only
               outfile.write('{}'.format(re.write(coordSystem)))
         # Stop just after end date
         if re.getEnsembleItem(2).getStartDateTime() > args.end_datetime:
            break
      else:
         if args.start_datetime != None:
            if re.getEnsembleItem(2).getStartDateTime() > args.start_datetime:
               if args.count != -1:
                  if elementCount < args.count:
                     # only start date and a count
                     outfile.write('{}'.format(re.write(coordSystem)))
                     elementCount = elementCount + 1
                     if args.size > 0:
                        outfileSize = outfile.tell()
                  else:
                     break
               else:
                  # only start date
                  outfile.write('{}'.format(re.write(coordSystem)))
         else:
            if args.count != -1:
                  if elementCount < args.count:
                     # only count
                     outfile.write('{}'.format(re.write(coordSystem)))
                     elementCount = elementCount + 1
                     if args.size > 0:
                        outfileSize = outfile.tell()
                  else:
                     break
            else:
               # Total file
               outfile.write('{}'.format(re.write(coordSystem)))
               if args.size > 0:
                  outfileSize = outfile.tell()

      # get checksum
      rawChecksum, checksum = __nextLittleEndianUnsignedShort(infile)

      computedChecksum = __computeChecksum(rawHeader, rawLength, rawEnsemble)

      if checksum != computedChecksum:
         print('Position:{}\tSize to read:{}'.format(hex(infile.tell()),length))
         print('Checksum error\nChecksum:{}\tComputed:{}'.format(checksum,computedChecksum))
         outfile.write('Checksum error::{}'.format(checksum))
         #raise IOError('Checksum error\nChecksum:{}\tComputed:{}'.format(checksum,computedChecksum))
 	
      # TODO: Manage output file size here
      if outfileSize >= (args.size*1000) and args.size > 0:
        outfile.close()
        try:
           outfile = open('{}{}.{}'.format(args.outfile.split('.')[0],fileCount+1,args.outfile.split('.')[1]),'w')
           fileCount += 1
        except:
           raise IOError('Unable to create file {}{}'.format(args.outfile,fileCount+1)) 
      
      try:
         rawHeader, header = __nextLittleEndianUnsignedShort(infile)
      except st.error:
         break
         
   infile.close()
   outfile.close()

  
if __name__== "__main__":
  main()	            

