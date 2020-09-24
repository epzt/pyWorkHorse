#!/usr/bin/python
#-*- coding: utf-8 -*-

import struct as st
import datetime
import numpy as np
import math

# header IDs
PD0HEADERID=0x7f7f
FIXEDLEADER=0x0000
VARIABLELEADER=0x0080
VELOCITYPROFILE=0x0100
CORRELATIONPROFILE=0x0200
INTENSITYPROFILE=0x0300
PERCENTGOODPROFILE=0x0400
STATUSPROFILE=0x0500
BOTTOMTRACK=0x0600
WAVESID=0x797f
WAVEPARAMETERSID=0x000B
WAVEPARAMETERSID=0x000C
MICROCAT=0x0800

# Constante value definition
BADVALUE=-9999
BADVELOCITY=-32768
USESINTERNALSENSORS = 15 

# Coordinate system
COORDSYSTEM = {
      0  : 'BEAM',
      8  : 'INSTRUMENT',
      16 : 'SHIP',
      24 : 'EARTH',
      4  : 'TILTS',
      2  : '3-BEAMS',
      1  : 'BEAM MAPPING',
      31 : 'Unknown', 
      }

# convenience function reused for header, length, and checksum
def __nextLittleEndianUnsignedShort(file):
   """Get next little endian unsigned short from file"""
   try:
      raw = file.read(2)
      return (raw, st.unpack('<H', raw)[0])
   except:
      return(-1,-1)
   
#----------------------------------------
#---   Class for header management    ---
#----------------------------------------
class WHHeader():
   def __init__(self):
      self._nbDataTypes = 0
      self._offsetDataTypes = []
      self._rawdata = ''

   def readWHHeader(self, index, rawEnsemble):
      # Store the raw data
      self._rawdata = rawEnsemble
      cpt = index + 1 # skip the spare byte
      nbDataTypesStr=rawEnsemble[cpt:cpt+1]
      try:
         # Store the number of data types in this ensemble
         self._nbDataTypes = st.unpack('B',nbDataTypesStr)[0]
      except:
         raise IOError('Enable to get data types number.')
      cpt = cpt + 1
      # Store the adresses offsets of each data types
      for i in range(self._nbDataTypes):
         self._offsetDataTypes.append(rawEnsemble[cpt:cpt+2])
         cpt = cpt + 2
      return(cpt)

   # Return raw data ensemble
   def getRawEnsemble(self):
      return(self._rawdata)

   # Return the binary byte number in the ensemble of the <index> data type
   def getOffSetDataTypes(self, index):
      try:
         return(st.unpack('H',self._offsetDataTypes[index])[0])
      except:
         return(BADVALUE)

   def GetNbDataTypes(self):
      return(self._nbDataTypes) # Give the variable nb of data types
      
   def printInfo(self):
      print("Nb data types: %d") % st.unpack('B',self._nbDataTypes)[0]

   def getType(self):
      return(PD0HEADERID)
      
#----------------------------------------
#---    Class fixed leader  data      ---
#----------------------------------------
class WHFixedLeader():
   def __init__(self):
      self._rawdata = ''
      self.whFixedLeader = {
      'FixedLeaderID':'',
      'CPUVersion':'',
      'CPURevision':'',
      'SystemConfiguration':'',
      'SystemFlag':'',
      'LagLength':'',
      'NumberOfBeams':'',
      'NumberOfCells':'',
      'PingsPerEnsemble':'',
      'DepthCellLength':'',
      'BlanckAfterTransmit':'',
      'SignalProcessingMode':'',
      'LowCorrThreshold':'',
      'NumbersCodeRepetition':'',
      'PercentMinimumGood':'',
      'ErrorVelocityThreshold':'',
      'Minutes':'',
      'Seconds':'',
      'Hundreds':'',
      'CoordinatesTransformation':'',
      'HeadingAlignement':'',
      'HeadingBias':'',
      'SensorSource':'',
      'SensorAvailable':'',
      'Bin1Distance':'',
      'XmitPulseLength':'',
      'StartEndDepthCell':'',
      'FalseTargetThreshold':'',
      'Spare1':'',
      'TransmitLagDistance':'',
      'CPUBoardSerialNumber':'',
      'SystemBandwidth':'',
      'SystemPower':'',
      'Spare2':'',
      'InstrumentSerialNumber':'',
      'BeamAngle':'',}
   
   # Return raw data ensemble
   def getRawEnsemble(self):
      return(self._rawdata)

   def readWHFixedLeader(self, index, rawEnsemble):
      self._rawdata = rawEnsemble
      cpt = index
      self.whFixedLeader['FixedLeaderID']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whFixedLeader['CPUVersion']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['CPURevision']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['SystemConfiguration']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whFixedLeader['SystemFlag']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['LagLength']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['NumberOfBeams']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['NumberOfCells']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['PingsPerEnsemble']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whFixedLeader['DepthCellLength']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whFixedLeader['BlanckAfterTransmit']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whFixedLeader['SignalProcessingMode']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['LowCorrThreshold']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['NumbersCodeRepetition']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['PercentMinimumGood']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['ErrorVelocityThreshold']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whFixedLeader['Minutes']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['Seconds']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['Hundreds']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['CoordinatesTransformation']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['HeadingAlignement']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whFixedLeader['HeadingBias']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whFixedLeader['SensorSource']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['SensorAvailable']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['Bin1Distance']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whFixedLeader['XmitPulseLength']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whFixedLeader['StartEndDepthCell']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whFixedLeader['FalseTargetThreshold']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['Spare1']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['TransmitLagDistance']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whFixedLeader['CPUBoardSerialNumber']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whFixedLeader['SystemBandwidth']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whFixedLeader['SystemPower']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['Spare2']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whFixedLeader['InstrumentSerialNumber']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whFixedLeader['BeamAngle']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      return(cpt)
  
   def getNumberOfCells(self):
      return(st.unpack('B',self.whFixedLeader['NumberOfCells'])[0])

   def getNumberOfBeams(self):
      return(st.unpack('B',self.whFixedLeader['NumberOfBeams'])[0])

   def getUseDepthSensor(self):
      theByte = st.unpack('B',self.whFixedLeader['SensorSource'])[0]
      return(self.check_bitL2R(theByte, 5))

   def getUsePitchSensor(self):
      theByte = st.unpack('B',self.whFixedLeader['SensorSource'])[0]
      return(self.check_bitL2R(theByte, 3))

   def getCorrelationThrehold(self):
      return(st.unpack('B',self.whFixedLeader['LowCorrThreshold'])[0])

   def computedSpeedOfSound(self):
      theByte = st.unpack('B',self.whFixedLeader['SensorSource'])[0]
      return(self.check_bitL2R(theByte, 6))

   def getVerticalSize(self):
      return(st.unpack('h',self.whFixedLeader['DepthCellLength'])[0]*0.01) # in meter

   def getDis1(self):
      return(st.unpack('h',self.whFixedLeader['Bin1Distance'])[0]*0.01) # in meter

   def check_bitL2R(self, byte, bit):
      return bool(byte & (0b10000000>>bit))

   def getRDIType(self):
      theByte = st.unpack('B',self.whFixedLeader['SystemConfiguration'][1])[0]
      if theByte & 0b000:
         return('75-kHz SYSTEM')
      elif theByte & 0b001:
         return('150-kHz SYSTEM')
      elif theByte & 0b010:
         return('300-kHz SYSTEM')
      elif theByte & 0b011:
         return('500/600-kHz SYSTEM')
      elif theByte & 0b100:
         return('1000/1200-kHz SYSTEM')
      elif theByte & 0b101:
         return('2400-kHz SYSTEM')
      else:
         return('Not used')

   def getBeamAngle(self):
      theByte = st.unpack('B',self.whFixedLeader['SystemConfiguration'][0])[0]
      if theByte & 0b00:
         return(15)
      elif theByte & 0b01:
         return(20)
      elif theByte & 0b10:
         return(30)
      elif theByte & 0b111:
         return(25)
      else:
         return(st.unpack('B',self.whFixedLeader['BeamAngle'])[0])
            
   def getConcaveOrConvex(self):
      theByte = st.unpack('B',self.whFixedLeader['SystemConfiguration'][1])[0]
      if self.check_bitL2R(theByte, 3):
         return(1) # Convex
      else:
         return(1) # Concave -> SHOULD RETURN -1 BUT ACTUALY ITS HARDLY DEFINED

   # return correction angle based on beam facing sens (up or down)
   def getFacingBeam(self):
      theByte = st.unpack('B',self.whFixedLeader['SystemConfiguration'][1])[0]
      if self.check_bitL2R(theByte, 7):
         return(180) # up ward
      else:
         return(0) # down ward

   def getHeadingAlignment(self):
      return(st.unpack('h',self.whFixedLeader['HeadingAlignement'])[0]*0.01)

   def getHeadingBias(self):
      return(st.unpack('h',self.whFixedLeader['HeadingBias'])[0]*0.01)

   def getCoordinateTransformation(self):
      cs = st.unpack('B', self.whFixedLeader['CoordinatesTransformation'])[0]
      return(COORDSYSTEM[cs])
      
   def write(self):
      return('{:d},{:d},{:d},{}'.format( \
                      self.getNumberOfBeams(), \
                      self.getNumberOfCells(), \
                      st.unpack('H',self.whFixedLeader['PingsPerEnsemble'])[0], \
                      self.getCoordinateTransformation()
                      ))

   #TODO: deal here to save in numpy format
   def writeBin(self):
      return([self.whFixedLeader['NumberOfBeams'],
              self.whFixedLeader['NumberOfCells'],
              self.whFixedLeader['PingsPerEnsemble'],
              self.whFixedLeader['CoordinatesTransformation']])

   def printInfo(self):
      print("Id: {}".format(st.unpack('H',self.whFixedLeader['FixedLeaderID'])[0]))
      print("Nb cells: {}".format(self.getNumberOfCells()))
      print("Nb beams: {}".format(self.getNumberOfBeams()))
      print("Coord. Syst.: {}".format(self.getCoordinateTransformation()))

   def getType(self):
      return(FIXEDLEADER)
      
#----------------------------------------
#--- Class variable leader  data      ---
#----------------------------------------
class WHVariableLeader():
   def __init__(self):
            # Return raw data ensemble
      self._rawdata = ''
      self.whVariableLeader = {
      'VariableLeaderID':'',
      'EnsembleNumber':'',
      'RTCYear':'',
      'RTCMonth':'',
      'RTCDay':'',
      'RTCHour':'',
      'RTCMinute':'',
      'RTCSecond':'',
      'RTCHundreds':'',
      'EnsembleMSB':'',
      'BitResult':'',
      'SpeedOfSound':'',
      'DepthOfTransducer':'',
      'Heading':'',
      'Pitch':'',
      'Roll':'',
      'Salinity':'',
      'Temperature':'',
      'MPTMinute':'',
      'MPTSecond':'',
      'MPTHundreds':'',
      'HeadingStdev':'',
      'PithStdev':'',
      'RollStdev':'',
      'ADCChannel0':'',
      'ADCChannel1':'',
      'ADCChannel2':'',
      'ADCChannel3':'',
      'ADCChannel4':'',
      'ADCChannel5':'',
      'ADCChannel6':'',
      'ADCChannel7':'',
      'ErrorStatus':'',
      'Reserved':'',
      'Pressure':'',
      'PressureVariance':'',
      'Spare':'',
      'Y2KRTCentury':'',
      'Y2KRTCYear':'',
      'Y2KRTCMonth':'',
      'Y2KRTCDay':'',
      'Y2KRTCHour':'',
      'Y2KRTCMinute':'',
      'Y2KRTCSecond':'',
      'Y2KRTCHundreds':'',}
      
   def readWHVariableLeader(self, index, rawEnsemble):
      self._rawdata = rawEnsemble
      cpt = index
      self.whVariableLeader['VariableLeaderID']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whVariableLeader['EnsembleNumber']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whVariableLeader['RTCYear']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['RTCMonth']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['RTCDay']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['RTCHour']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['RTCMinute']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['RTCSecond']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['RTCHundreds']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['EnsembleMSB']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['BitResult']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whVariableLeader['SpeedOfSound']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whVariableLeader['DepthOfTransducer']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whVariableLeader['Heading']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whVariableLeader['Pitch']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whVariableLeader['Roll']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whVariableLeader['Salinity']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whVariableLeader['Temperature']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whVariableLeader['MPTMinute']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['MPTSecond']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['MPTHundreds']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['HeadingStdev']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['PithStdev']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['RollStdev']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['ADCChannel0']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['ADCChannel1']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['ADCChannel2']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['ADCChannel3']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['ADCChannel4']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['ADCChannel5']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['ADCChannel6']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['ADCChannel7']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['ErrorStatus']=rawEnsemble[cpt:cpt+4]
      cpt = cpt + 4
      self.whVariableLeader['Reserved']=rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      self.whVariableLeader['Pressure']=rawEnsemble[cpt:cpt+4]
      cpt = cpt + 4
      self.whVariableLeader['PressureVariance']=rawEnsemble[cpt:cpt+4]
      cpt = cpt + 4
      self.whVariableLeader['Spare']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['Y2KRTCentury']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['Y2KRTCYear']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['Y2KRTCMonth']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['Y2KRTCDay']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['Y2KRTCHour']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['Y2KRTCMinute']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['Y2KRTCSecond']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      self.whVariableLeader['Y2KRTCHundreds']=rawEnsemble[cpt:cpt+1]
      cpt = cpt + 1
      return(cpt)
   
   # Return raw data ensemble
   def getRawEnsemble(self):
      return(self._rawdata)

   def getElementNumber(self):
      enb = st.unpack('H',self.whVariableLeader['EnsembleNumber'])[0]
      msb = st.unpack('B',self.whVariableLeader['EnsembleMSB'])[0]
      return ((65535 * msb) + enb)

   def getHeading(self):
      return(st.unpack('H',self.whVariableLeader['Heading'])[0]*0.01)

   def getPitch(self):
      return(st.unpack('h',self.whVariableLeader['Pitch'])[0]*0.01)

   def getRoll(self):
      return(st.unpack('h',self.whVariableLeader['Roll'])[0]*0.01)

   def getTemperature(self):
      return(st.unpack('h',self.whVariableLeader['Temperature'])[0]*0.01)

   def getDepthSensor(self):
      # Depth is store in decimeter, it is output in meter here
      return(st.unpack('h',self.whVariableLeader['DepthOfTransducer'])[0]*0.1)

   def getSpeedOfSound(self):
      return(st.unpack('h',self.whVariableLeader['SpeedOfSound'])[0])

   def getSalinity(self):
      return(st.unpack('h',self.whVariableLeader['Salinity'])[0])

   def getStartTime(self):
      hour = st.unpack('B',self.whVariableLeader['RTCHour'])[0]
      minute = st.unpack('B',self.whVariableLeader['RTCMinute'])[0]
      second = st.unpack('B',self.whVariableLeader['RTCSecond'])[0]
      sdec = st.unpack('B',self.whVariableLeader['RTCHundreds'])[0]
      return('{:02d}:{:02d}:{:02d}.{:02d}'.format(hour,minute,second,sdec))
      
   def getTime(self):
      hour = st.unpack('B',self.whVariableLeader['Y2KRTCHour'])[0]
      minute = st.unpack('B',self.whVariableLeader['Y2KRTCMinute'])[0]
      second = st.unpack('B',self.whVariableLeader['Y2KRTCSecond'])[0]
      sdec = st.unpack('B',self.whVariableLeader['Y2KRTCHundreds'])[0]
      return('{:02d}:{:02d}:{:02d}.{:02d}'.format(hour,minute,second,sdec))
   
   def getStartDate(self):
      year = st.unpack('B',self.whVariableLeader['RTCYear'])[0]
      month = st.unpack('B',self.whVariableLeader['RTCMonth'])[0]
      day = st.unpack('B',self.whVariableLeader['RTCDay'])[0]
      return('{:02d}-{:02d}-{:02d}'.format(year,month,day))
         
   def getDate(self):
      year = st.unpack('B',self.whVariableLeader['Y2KRTCYear'])[0]
      month = st.unpack('B',self.whVariableLeader['Y2KRTCMonth'])[0]
      day = st.unpack('B',self.whVariableLeader['Y2KRTCDay'])[0]
      return('{:02d}-{:02d}-{:02d}'.format(year,month,day))
   
   def getStartDateTime(self):
      try:
         datetime_str = '{} {}'.format(self.getStartDate(), self.getStartTime())
         return datetime.datetime.strptime(datetime_str, "%y-%m-%d %H:%M:%S.%f")
      except ValueError:
         msg = "Given Datetime ({0}) not valid! Expected format, 'yy-mm-dd hh:mm:ss.ss'!".format(datetime_str)
         raise IOError(msg)
         
   def getDateTime(self):
      try:
         datetime_str = '{} {}'.format(self.getDate(), self.getTime())
         return datetime.datetime.strptime(datetime_str, "%y-%m-%d %H:%M:%S.%f")
      except ValueError:
         msg = "Given Datetime ({0}) not valid! Expected format, 'yy-mm-dd hh:mm:ss.ss'!".format(datetime_str)
         raise IOError(msg)
         
   def write(self):
      return('{:d},{},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},'.format( \
                      self.getElementNumber(), \
                      self.getStartDateTime(), \
                      self.getHeading(), \
                      self.getPitch(), \
                      self.getRoll(), \
                      st.unpack('h',self.whVariableLeader['Salinity'])[0], \
                      self.getTemperature(), \
                      st.unpack('I',self.whVariableLeader['Pressure'])[0]))

   # TODO: deal here to save in numpy format
   def writeBin(self):
         return([self.whVariableLeader['EnsembleNumber'],
         self.whVariableLeader['EnsembleMSB'],
         self.whVariableLeader['RTCYear'],
         self.whVariableLeader['RTCMonth'],
         self.whVariableLeader['RTCDay'],
         self.whVariableLeader['Y2KRTCHour'],
         self.whVariableLeader['Y2KRTCMinute'],
         self.whVariableLeader['Y2KRTCSecond'],
         self.whVariableLeader['Y2KRTCHundreds'],
         self.whVariableLeader['Heading'],
         self.whVariableLeader['Pitch'],
         self.whVariableLeader['Roll'],
         self.whVariableLeader['Salinity'],
         self.whVariableLeader['Temperature'],
         self.whVariableLeader['Pressure']]
         )

   def printInfo(self):
      print("Id: {}".format(st.unpack('H',self.whVariableLeader['VariableLeaderID'])[0]))
      print("Num: {}".format(self.getElementNumber()))
      print("Heading: {:.1f}".format(self.getHeading()))
      print("Salinity: {:.1f}".format(st.unpack('H',self.whVariableLeader['Salinity'])[0]))
      print("Temperature: {:.2f}".format(self.getTemperature()))
      print("Sound speed: {}".format(st.unpack('H',self.whVariableLeader['SpeedOfSound'])[0]))
      print(self.getStartDateTime())
#      print(self.getDateTime())

   def getType(self):
      return(VARIABLELEADER)
      
#----------------------------------------
#---        Class velocity           ---
#----------------------------------------
class WHVelocity():
   def __init__(self):
      self._rawdata  = ''
      self.velocityID = 0
      self.cellVelocity = {
      'ID':[],
      'VEL1':[],
      'VEL2':[],
      'VEL3':[],
      'VEL4':[],}
      
   def readWHVelocity(self, nbCell, index, rawEnsemble):
      self._rawdata = rawEnsemble
      cpt = index
      self.velocityID = rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      for i in range(nbCell):
         self.cellVelocity['ID'].append(i+1)
         self.cellVelocity['VEL1'].append(rawEnsemble[cpt:cpt+2])
         cpt = cpt + 2
         self.cellVelocity['VEL2'].append(rawEnsemble[cpt:cpt+2])
         cpt = cpt + 2
         self.cellVelocity['VEL3'].append(rawEnsemble[cpt:cpt+2])
         cpt = cpt + 2
         self.cellVelocity['VEL4'].append(rawEnsemble[cpt:cpt+2])
         cpt = cpt + 2
      return(cpt)

   # Return raw data ensemble
   def getRawEnsemble(self):
      return(self._rawdata)

   def getCellVelocity(self,i,j):
      try:
         if st.unpack('h',self.cellVelocity['VEL{}'.format(i)][j])[0] != BADVELOCITY:
            return(st.unpack('h',self.cellVelocity['VEL{}'.format(i)][j])[0]*0.001) # get velocity in m.s-1
         else:
            return(BADVELOCITY)
      except:
         raise('An error occured getting velocity value')

   def write(self):
      retValue=''
      for i in range(len(self.cellVelocity['ID'])):
         if self.getCellVelocity(1,i) != BADVELOCITY:
            retValue = retValue + '{:.3f},'.format(self.getCellVelocity(1,i))
         else:
            retValue = retValue + "Nan,"
         if self.getCellVelocity(2,i) != BADVELOCITY:
            retValue = retValue + '{:.3f},'.format(self.getCellVelocity(2,i))
         else:
            retValue = retValue + "Nan,"
         if self.getCellVelocity(3,i) != BADVELOCITY:
            retValue = retValue + '{:.3f},'.format(self.getCellVelocity(3,i))
         else:
            retValue = retValue + "Nan,"
         if self.getCellVelocity(4,i) != BADVELOCITY:
            retValue = retValue + '{:.3f},'.format(self.getCellVelocity(4,i))
         else:
            retValue = retValue + "Nan,"
      return(retValue)

   def writeBin(self):
      return(self._rawdata)
      
   def getType(self):
      return(VELOCITYPROFILE)

#----------------------------------------
#---        Class correlation           ---
#----------------------------------------
class WHCorrelation():
   def __init__(self):
      self._rawdata = ''
      self.correlationID = 0
      self.cellCorrelation = {
      'ID':[],
      'COR1':[],
      'COR2':[],
      'COR3':[],
      'COR4':[],}
      
   def readWHCorrelation(self, nbCell, index, rawEnsemble):
      self._rawdata = rawEnsemble
      cpt = index
      self.correlationID = rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      for i in range(nbCell):
         self.cellCorrelation['ID'].append(i+1)
         self.cellCorrelation['COR1'].append(rawEnsemble[cpt:cpt+1])
         cpt = cpt + 1
         self.cellCorrelation['COR2'].append(rawEnsemble[cpt:cpt+1])
         cpt = cpt + 1
         self.cellCorrelation['COR3'].append(rawEnsemble[cpt:cpt+1])
         cpt = cpt + 1
         self.cellCorrelation['COR4'].append(rawEnsemble[cpt:cpt+1])
         cpt = cpt + 1
      return(cpt)

   # Return raw data ensemble
   def getRawEnsemble(self):
      return(self._rawdata)

   def getCorrelationBeam(self, numCell):
      return([st.unpack('B',self.cellCorrelation['COR1'][numCell])[0],
              st.unpack('B',self.cellCorrelation['COR2'][numCell])[0],
              st.unpack('B',self.cellCorrelation['COR3'][numCell])[0],
              st.unpack('B',self.cellCorrelation['COR4'][numCell])[0]])

   def write(self):
      retValue=''
      for i in range(len(self.cellCorrelation['ID'])):
         retValue = retValue + '{:.2f},{:.2f},{:.2f},{:.2f},'.format \
                           (st.unpack('B',self.cellCorrelation['COR1'][i])[0], \
                           st.unpack('B',self.cellCorrelation['COR2'][i])[0], \
                           st.unpack('B',self.cellCorrelation['COR3'][i])[0], \
                           st.unpack('B',self.cellCorrelation['COR4'][i])[0])
      return(retValue)

   # TODO: deal here to save in numpy format
   def writeBin(self):
      return(self._rawdata)

   def getType(self):
      return(CORRELATIONPROFILE)

#----------------------------------------
#---        Class intensity           ---
#----------------------------------------
class WHIntensity():
   def __init__(self):
      self._rawdata = ''
      self.intensityID = 0
      self.cellIntensity = {
      'ID':[],
      'INT1':[],
      'INT2':[],
      'INT3':[],
      'INT4':[],}
      
   def readWHIntensity(self, nbCell, index, rawEnsemble):
      self._rawdata = rawEnsemble
      cpt = index
      self.intensityID = rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      for i in range(nbCell):
         self.cellIntensity['ID'].append(i+1)
         self.cellIntensity['INT1'].append(rawEnsemble[cpt:cpt+1])
         cpt = cpt + 1
         self.cellIntensity['INT2'].append(rawEnsemble[cpt:cpt+1])
         cpt = cpt + 1
         self.cellIntensity['INT3'].append(rawEnsemble[cpt:cpt+1])
         cpt = cpt + 1
         self.cellIntensity['INT4'].append(rawEnsemble[cpt:cpt+1])
         cpt = cpt + 1
      return(cpt)

   # Return raw data ensemble
   def getRawEnsemble(self):
      return(self._rawdata)

   def write(self):
      retValue=''
      # Conversion of the stored intensity internal value to dB 
      # K is a factor dependant on electronic component, it is estimated by ration of a
      # scale factor given by RDI (0.45 dB) and temperature, here fixed at 10°c (for convenience)
      k = 0.045  # 0.45 / 10.0
      for i in range(len(self.cellIntensity['ID'])):
         retValue = retValue + '{:.2f},{:.2f},{:.2f},{:.2f},'.format \
                           (10 * np.log10(10**(k*(st.unpack('B',self.cellIntensity['INT1'][i])[0])/10)), \
                           10 * np.log10(10**(k*(st.unpack('B',self.cellIntensity['INT2'][i])[0])/10)), \
                           10 * np.log10(10**(k*(st.unpack('B',self.cellIntensity['INT3'][i])[0])/10)), \
                           10 * np.log10(10**(k*(st.unpack('B',self.cellIntensity['INT4'][i])[0])/10)) )
      return(retValue)

   # TODO: deal here to save in numpy format
   def writeBin(self):
      return(self._rawdata)
      
   def getType(self):
      return(INTENSITYPROFILE)

#----------------------------------------
#---     Class percent good           ---
#----------------------------------------
class WHPercentGood():
   def __init__(self):
      self._rawdata =''
      self.percentGoodID = 0
      self.cellPercentGood = {
      'ID':[],
      'PG1':[],
      'PG2':[],
      'PG3':[],
      'PG4':[],}
      
   def readWHPercentGood(self, nbCell, index, rawEnsemble):
      self._rawdata = rawEnsemble
      cpt = index
      self.percentGoodID = rawEnsemble[cpt:cpt+2]
      cpt = cpt + 2
      for i in range(nbCell):
         self.cellPercentGood['ID'].append(i+1)
         self.cellPercentGood['PG1'].append(rawEnsemble[cpt:cpt+1])
         cpt = cpt + 1
         self.cellPercentGood['PG2'].append(rawEnsemble[cpt:cpt+1])
         cpt = cpt + 1
         self.cellPercentGood['PG3'].append(rawEnsemble[cpt:cpt+1])
         cpt = cpt + 1
         self.cellPercentGood['PG4'].append(rawEnsemble[cpt:cpt+1])
         cpt = cpt + 1
      return(cpt)

   # Return raw data ensemble
   def getRawEnsemble(self):
      return(self._rawdata)

   def write(self):
      retValue=''
      for i in range(len(self.cellPercentGood['ID'])):
         retValue = retValue + '{:3.1f},{:3.1f},{:3.1f},{:3.1f},'.format \
                           (st.unpack('b',self.cellPercentGood['PG1'][i])[0], \
                           st.unpack('b',self.cellPercentGood['PG2'][i])[0], \
                           st.unpack('b',self.cellPercentGood['PG3'][i])[0], \
                           st.unpack('b',self.cellPercentGood['PG4'][i])[0])
      return(retValue)

   # TODO: deal here to save in numpy format
   def writeBin(self):
      return(self._rawdata)

   def getType(self):
      return(PERCENTGOODPROFILE)

#----------------------------------------
#---  Class read Ensemble             ---
# return the different data types     ---
#----------------------------------------
class readEnsemble():
   def __init__(self, _rawEnsemble):
      self.rawEnsemble = _rawEnsemble
      self.h = WHHeader()
      self.fh = WHFixedLeader()
      self.vh = WHVariableLeader()
      self.v = WHVelocity()
      self.corr = WHCorrelation()
      self.inty = WHIntensity()
      self.pg = WHPercentGood()
      self.ensembleList = []

   def readEnsembleData(self):
      index = 0
      self.ensembleList = []
      nbCells = 0
      # Read header part
      index = self.h.readWHHeader(0, self.rawEnsemble)
      self.ensembleList.append(self.h)
      # loop over number data types read in the header
      # and read the various ensemble
      for i in range(self.h.GetNbDataTypes()):
         # Read fixed header
         if st.unpack('<H', self.rawEnsemble[self.h.getOffSetDataTypes(i)-4:self.h.getOffSetDataTypes(i)-2])[0] == FIXEDLEADER:
            index = self.fh.readWHFixedLeader(self.h.getOffSetDataTypes(i)-4, self.rawEnsemble)
            # Get the number of cells for this ensemble
            nbCells = self.fh.getNumberOfCells()
            self.ensembleList.append(self.fh)
            # Read variable header
         elif st.unpack('<H', self.rawEnsemble[self.h.getOffSetDataTypes(i)-4:self.h.getOffSetDataTypes(i)-2])[0] == VARIABLELEADER: 
            index = self.vh.readWHVariableLeader(self.h.getOffSetDataTypes(i)-4, self.rawEnsemble)
            self.ensembleList.append(self.vh)
         # Read velocity
         elif st.unpack('<H', self.rawEnsemble[self.h.getOffSetDataTypes(i)-4:self.h.getOffSetDataTypes(i)-2])[0] == VELOCITYPROFILE:
            index = self.v.readWHVelocity(nbCells, self.h.getOffSetDataTypes(i)-4, self.rawEnsemble)
            self.ensembleList.append(self.v)
         # Read correlation data
         elif st.unpack('<H', self.rawEnsemble[self.h.getOffSetDataTypes(i)-4:self.h.getOffSetDataTypes(i)-2])[0] == CORRELATIONPROFILE:
            index = self.corr.readWHCorrelation(nbCells, self.h.getOffSetDataTypes(i)-4, self.rawEnsemble)
            self.ensembleList.append(self.corr)
         #Read Intensity data
         elif st.unpack('<H', self.rawEnsemble[self.h.getOffSetDataTypes(i)-4:self.h.getOffSetDataTypes(i)-2])[0] == INTENSITYPROFILE:
            index = self.inty.readWHIntensity(nbCells, self.h.getOffSetDataTypes(i)-4, self.rawEnsemble)
            self.ensembleList.append(self.inty)
         # Read Percent Good data
         elif st.unpack('<H', self.rawEnsemble[self.h.getOffSetDataTypes(i)-4:self.h.getOffSetDataTypes(i)-2])[0] == PERCENTGOODPROFILE:
            index = self.pg.readWHPercentGood(nbCells, self.h.getOffSetDataTypes(i)-4, self.rawEnsemble)
            self.ensembleList.append(self.pg)
      return

   def getEnsembleItem(self,num):
      assert num <= len(self.ensembleList)
      return(self.ensembleList[num])
   
   # Return true speed of sound corrected from temperature, salinity and depth from Urick (1983)
   def getSpeedOfSound(self,T,S,D):
      return(1449.2+4.6*T-0.055*(T*T)+0.00029*(T*T*T)+(1.34-0.01*T)*(S-35)+0.016*D)

   # Corrected the velocity taking int account speed of sound
   def getCorrectedVelocity(self, beam, cell):
      C = self.getSpeedOfSound(self.vh.getTemperature(),self.vh.getSalinity(),self.vh.getDepthSensor())
      CA = self.vh.getSpeedOfSound()
      if self.v.getCellVelocity(beam,cell) != BADVELOCITY:
         return(self.v.getCellVelocity(beam,cell)*(C/CA))
      else:
         return(BADVELOCITY)

   # Compute depth corrected by speed of sound
   def getCorrectedCellDepth(self):
      k = [] # correction factors at each cells
      C = [] # speed of sound at each cells
      newCellDepth = [] # new cell depths
      # Speed of sound at transducer (C0)
      C.append(self.getSpeedOfSound(self.vh.getTemperature(),self.vh.getSalinity(),self.vh.getDepthSensor()))
      CA = self.vh.getSpeedOfSound() # Stored speed of sound
      firstPass = True
      for n in range(self.fh.getNumberOfCells()):
         if self.fh.getFacingBeam() == 180:
            centerCellDepth = self.vh.getDepthSensor() - self.fh.getDis1() - n*self.fh.getVerticalSize()
         else:
            centerCellDepth = self.vh.getDepthSensor() + self.fh.getDis1() + n*self.fh.getVerticalSize()

         C.append((self.getSpeedOfSound(self.vh.getTemperature(),self.vh.getSalinity(),centerCellDepth) + C[n]) * 0.5)
         k.append(np.sqrt(1+(1-(np.square(C[n]/C[0]))*np.square(np.tan(np.deg2rad(self.fh.getBeamAngle()))))))

         if firstPass:
            newCellDepth.append(self.fh.getDis1()*k[n]*(C[n]/CA))
            firstPass = False
         else:
            newCellDepth.append((k[n]*(C[n]/CA)*self.fh.getVerticalSize())+newCellDepth[n-1])
      return(newCellDepth)

   # Perform correlation test to tag beams velocity good or bad for the current cell
   # Return number of valid velocity beams and the list of corrected velocities
   def correlationTest(self, cell):
      nValidVelocities = self.fh.getNumberOfBeams()
      velocitiesList = []
      # correlation test
      corrValues = self.corr.getCorrelationBeam(cell)
      for b in range(nValidVelocities):
         if (corrValues[b] < self.fh.getCorrelationThrehold()) or (self.getCorrectedVelocity(b+1,cell) == BADVELOCITY):
            nValidVelocities -= 1
            velocitiesList.append(BADVELOCITY)
         else:
            velocitiesList.append(self.getCorrectedVelocity(b+1,cell))
      return(nValidVelocities,velocitiesList)

   # Compute de 4 beams solution of the velocity
   def getFourBeamSolution(self,a,b,c,d,currentCellVels):
      newVels = [0]*4
      newVels[0] = c*a*(currentCellVels[0]-currentCellVels[1])
      newVels[1] = c*a*(currentCellVels[3]-currentCellVels[2])
      newVels[2] = b*(currentCellVels[0]+currentCellVels[1]+currentCellVels[2]+currentCellVels[3])
      newVels[3] = d*(currentCellVels[0]+currentCellVels[1]-currentCellVels[2]-currentCellVels[3])
      return(newVels)

   # Compute de 3 beams solution of the velocity
   def getThreeBeamSolution(self,a,b,c,d,currentCellVels):
      newVels = [0]*4
      badVelID = currentCellVels.index(BADVELOCITY)
      if badVelID == 0:  # Beam 1 off
         newVels[0] = c*a*(currentCellVels[3]+currentCellVels[3]-2*currentCellVels[1])
         newVels[1] = c*a*(currentCellVels[3]-currentCellVels[2])
         newVels[2] = 2*b*(currentCellVels[3]+currentCellVels[2])
         newVels[3] = 0
         return(newVels)
      if badVelID == 1:  # Beam 2 off
         newVels[0] = -1*c*a*(currentCellVels[3]+currentCellVels[3])
         newVels[1] = c*a*(currentCellVels[3]-currentCellVels[2])
         newVels[2] = 2*b*(currentCellVels[3]+currentCellVels[2])
         newVels[3] = 0
         return(newVels)
      if badVelID == 2:  # Beam 3 off
         newVels[0] = c*a*(currentCellVels[0]-currentCellVels[1])
         newVels[1] = c*a*(2*currentCellVels[3]-currentCellVels[0]-currentCellVels[1])
         newVels[2] = 2*b*(currentCellVels[0]+currentCellVels[1])
         newVels[3] = 0
         return(newVels)
      if badVelID == 3:  # Beam 4 off
         newVels[0] = c*a*(currentCellVels[0]-currentCellVels[1])
         newVels[1] = c*a*(-2*currentCellVels[2]+currentCellVels[0]+currentCellVels[1])
         newVels[2] = 2*b*(currentCellVels[0]+currentCellVels[1])
         newVels[3] = 0
         return(newVels)

   # Transforme beam coordinates to XYZ coordinates
   def BeamToXYZ(self):
      # TODO: we need to deal also with 3 beams solutions
      theta = self.fh.getBeamAngle() # Get beam angle
      c = self.fh.getConcaveOrConvex() # 1: convex beams; -1: concave beams
      a = 1.0 / (2.0*np.sin(math.radians(theta)))
      b = 1.0 / (4.0*np.cos(math.radians(theta)))
      d = a / np.sqrt(2)
      vels = np.zeros((self.fh.getNumberOfBeams(), self.fh.getNumberOfCells()))
      for i in range(self.fh.getNumberOfCells()):
         nValidVel, currentCellVels = self.correlationTest(i)
         if nValidVel == 4:
            """
            vels[0,i] = c*a*(self.getCorrectedVelocity(1,i)-self.getCorrectedVelocity(2,i))
            vels[1,i] = c*a*(self.getCorrectedVelocity(4,i)-self.getCorrectedVelocity(3,i))
            vels[2,i] = b*(self.getCorrectedVelocity(1,i)+self.getCorrectedVelocity(2,i)+self.getCorrectedVelocity(3,i)+self.getCorrectedVelocity(4,i))
            vels[3,i] = d*(self.getCorrectedVelocity(1,i)+self.getCorrectedVelocity(2,i)-self.getCorrectedVelocity(3,i)-self.getCorrectedVelocity(4,i))
            """
            newVels = self.getFourBeamSolution(a,b,c,d,currentCellVels)
            vels[0,i] = newVels[0]
            vels[1,i] = newVels[1]
            vels[2,i] = newVels[2]
            vels[3,i] = newVels[3]
         if nValidVel == 3:
            newVels = self.getThreeBeamSolution(a,b,c,d,currentCellVels)
            vels[0,i] = newVels[0]
            vels[1,i] = newVels[1]
            vels[2,i] = newVels[2]
            vels[3,i] = newVels[3]
      return(vels)

   # Transform beam coordinates to East, Noth and Up coordinates
   def BeamToENU(self):
      XYZVels = self.BeamToXYZ() # Get XYZ coords from beams
      if self.fh.getUsePitchSensor(): # Internal sensors
         P = np.arctan(np.tan(self.vh.getPitch())*np.cos(self.vh.getRoll()))
      else:
         P = self.vh.getPitch()
      SH = np.sin(math.radians(self.vh.getHeading()+self.fh.getHeadingAlignment()))
      CH = np.cos(math.radians(self.vh.getHeading()+self.fh.getHeadingAlignment()))
      SP = np.sin(math.radians(P))
      CP = np.cos(math.radians(P))
      SR = np.sin(math.radians(self.vh.getRoll()+self.fh.getFacingBeam()))
      CR = np.cos(math.radians(self.vh.getRoll()+self.fh.getFacingBeam()))
      M = np.matrix([[(CH*CR)+(SH*SP*SR),  SH*CP, (CH*SR)-(SH*SP*CR), 0],
                    [(-SH*CR)+(CH*SP*SR), CH*CP, (-SH*SR)-(CH*SP*CR), 0],
                    [-CP*SR             , SP   , CP*CR  , 0],
                    [0                  ,0     ,0       , 1]])
      ENUVels = np.dot(XYZVels.transpose(), M)
      return(ENUVels.transpose())

   # Return the velocities based on the required coordinate system
   def write(self,coordinates):
      retValue = ""
      l = len(self.ensembleList)
      # Skip the header store at 0
      retValue += '{}'.format(self.ensembleList[1].write())
      for i in range(2,l-1):
         if self.ensembleList[i].getType() == VELOCITYPROFILE:
            if coordinates == COORDSYSTEM[8]: # Instrument
               xyzCoords = self.BeamToXYZ() # array (4 x nbCells)
               for j in range(self.fh.getNumberOfCells()):
                  retValue += ',{:.5f},{:.5f},{:.5f},{:.5f}'.format(xyzCoords[0,j],xyzCoords[1,j],xyzCoords[2,j],xyzCoords[3,j])
            elif coordinates == COORDSYSTEM[24]: # Earth
               ENUCoords = self.BeamToENU() # array (nbCells x 4)
               for j in range(self.fh.getNumberOfCells()):
                  retValue += ',{:.5f},{:.5f},{:.5f},{:.5f}'.format(ENUCoords[0,j],ENUCoords[1,j],ENUCoords[2,j],ENUCoords[3,j])
            else:
               retValue += ',{}'.format(self.ensembleList[i].write()) # Beams
         else:
            retValue += ',{}'.format(self.ensembleList[i].write())
      retValue += ',{}\n'.format(self.ensembleList[l-1].write())
      return(retValue)

#----------------------------------------
#---Return first occurence of elements---
#----------------------------------------
def getFirstWavesCurrentsID(infile):
   firstWaves=-1
   firstCurrents=-1
   
   # Try to find first occurence of waves element
   while(True):
      raw, value = __nextLittleEndianUnsignedShort(infile)
      if raw == st.pack('<H',PD0HEADERID):
         break
   firstCurrents = infile.tell()
      
   infile.seek(0)
   
   # Try to find first occurence of waves element
   while(infile.read(2) != WAVESID):
      raw, value = __nextLittleEndianUnsignedShort(infile)
      if raw == st.pack('<H',WAVESID):
         break
   firstWaves = infile.tell()
         
   # bail if neither waves nor currents found
   if (firstWaves < 0) and (firstCurrents < 0):
      raise IOError('Neither waves nor currents header found')
         
   return(firstCurrents,firstWaves)

            