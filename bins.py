# Author: Thomas Goff
# Filename: oohw11
# Class: COMS 6100
# Professor John Wallin
# Middle Tennessee State University
# This script is an object oriented take on Dr Wallin's HW11 
import numpy as np
import matplotlib.pyplot as plt
import os

class asteroid:
  def __init__(self):
    self.peri = 0.0 # perihelion
    self.incl = 0.0 # inclinction
    self.e = 0.0 # eccentricity
    self.a = 0.0

  def calca(self):
    self.a = self.peri / (1 - self.e) # calculate a

  def setVals(self,p,i,e):
    self.peri = p
    self.incl = i
    self.e = e
  # if you needed to print.. 
  def printData(self):
    print self.peri
    print self.incl
    print self.e
    print self.a

def grabPage():
  cmd = "wget -O rawData.txt http://www.minorplanetcenter.net/iau/MPCORB/MPCORB.DAT"
  os.system(cmd)

def getData():
  f = open("rawData.txt","r")
  lines = []
  for l in f:
    lines.append(l.strip())
  f.close()
  return lines

def parseData(raw):
  catch = "---"
  newList = []
  lineCount = 0
  for l in raw:
    testIndex = l.find(catch)
    if testIndex != -1:
      dataIndex = lineCount
    lineCount+=1
  dataIndex = dataIndex + 1
  for i in range(dataIndex, len(raw)):
    newList.append(raw[i].split())
  aList = [asteroid() for i in range(len(newList))]
  index = 0
  for roid in aList:
    temp = newList[index]
    if len(newList[index]) != 0: 
      roid.setVals(float(temp[5]),float(temp[7]),float(temp[8]))
      roid.calca()
    index+=1
  return aList

# function to generate histogram

def myhist(cleanData, title, xlabel, n, lower, upper, index):
  newList = []
  newList2 = []
  fileName = title + ".png"
  binSize = (upper - lower) / n
  bins = [0] * n # array to hold different bins
  x = np.linspace(lower, upper, n)
  if index == 'p':
    for obj in cleanData:
      newList2.append(obj.peri)
  elif index == 'e':
    for obj in cleanData:
      newList2.append(obj.e)
  elif index == 'incl':
    for obj in cleanData:
      newList2.append(obj.incl)
  else:
    for obj in cleanData:
      newList2.append(obj.a)
  lowest = newList2[0]
  # bin the data appropriately
  xnext = lower
  #for i in range(0, n):
  #  xprev = xnext
  #  x.append(xprev)
  #  xnext = xprev + binSize

  for i in range(0, len(newList2)):
  # check if double is in range that we want
    j = float(newList2[i]) / binSize
    test = float(newList2[i])
    if test < lowest:# find the lowest
      lowest = test
    if j < n and j > -1:
      j = int(j)
      bins[int(j)] = bins[int(j)] + 1 # incremement the bin counter
  # find the lowest value in the list to adjust x displays 
  for e in newList2:
    if float(e) < upper and float(e) > lower:
      newList.append(e)
  # plot with my algorithm using plot command

  plt.gcf().clear() # clear the plot to use hist function in pyplot
  plt.hist(newList, n)
  plt.title(title)
  plt.xlabel(xlabel)
  plt.savefig("Histogram " + title)
  plt.gcf().clear() # get ready for another
  plt.plot(x,bins)
  plt.savefig(title)
def main():
  grabPage()
  mydata = getData()
  plotData = parseData(mydata)
  myhist(plotData, "Perihelion Distance" , "AU", 10, 0, 50, "peri")
  myhist(plotData, "Inclination", "degrees", 10, -30, 30, "incl")
  myhist(plotData, "Orbital Eccentricity", "elongation",10,  0, 1.1, "e")
  myhist(plotData, "Semi-major axis", "degrees", 10,  0, 50, "a")
main()
