'''
Small command line utily for plotting functions using matplotlib
'''

import sys
import matplotlib.pyplot as plt
from math import *

def printHelp():
  msg = '''
    Usage:
      --help for help
      interval=(x,y) to set axis interval
      function=def=sin(x),label=sin to add a function
      text=something to show text on graph
      setvar:y=5 to set the value of a variable
    Examples:
      plotfunction.py function=def=sin(x),label=sinus function=def=cos(x),label=cosinus interval=(0,2*pi) text=exemple
      plotfunction.py setvar:y=2 interval=(-10,10) function=def=x**y
      plotfunction.py setvar:armor=20 "setvar:multiplier=(lambda armor:1-((0.052*armor)/(0.9+0.048*armor)))"
                      interval=(0,1000) "text=Comparision between desolator and mkb for 20 armor"
                      function=label=raw,def=x*multiplier(armor) function=label=deso,def=x*multiplier(armor-6)
                      function=label=raw,def=x*multiplier(armor)+0.75*100*0.75
  '''

def parseArg(arg):
  helpMarker = '--help'
  intervalMarker = 'interval='
  functionMarker = 'function='
  textMarker = 'text='
  setvarMarker = 'setvar:'
  if arg == helpMarker:
    printHelp()
    return 2, None
  elif arg.startswith(intervalMarker):
    arg = arg[len(intervalMarker):]
    return 0, eval(arg)
  elif arg.startswith(functionMarker):
    arg = arg[len(functionMarker):].split(',')
    fstring = ''
    label = ' '
    fstringMarker = 'def='
    labelMarker = 'label='
    for tok in arg:
      if tok.startswith(fstringMarker):
        fstring = tok[len(fstringMarker):]
      elif tok.startswith(labelMarker):
        label = tok[len(labelMarker):]
      else:
        exit('Invalid token in function definition: {}'.format(tok))
    return 1, (fstring, label)
  elif arg.startswith(textMarker):
    plt.text(0, 0, arg[len(textMarker):])
    return 3, None
  elif arg.startswith(setvarMarker):
    [tok0, tok1] = arg[len(setvarMarker):].split('=')
    exec('{} = {}'.format(tok0, tok1), globals())
    return 4, None
  else:
    exit('Invalid parameter: {}'.format(arg))


def parseArgs(args):
  lr = (0, 100)
  fs = []
  for arg in args:
    tip, res = parseArg(arg)
    if tip == 0:
      lr = res
    elif tip == 1:
      fs.append(res)
  return lr, fs

def main():
  lr, fs = parseArgs(sys.argv[1:])
  l, r = lr
  step = (r - l) / 100
  n = len(fs)
  fres = [[] for i in range(n)]
  for f in fs:
    fres.append([])
  xaxis = []
  while l <= r:
    xaxis.append(l)
    for idx in range(n):
      x = l
      fres[idx].append(eval(fs[idx][0]))
    l += step
  handles = []
  for idx in range(n):
    handle, = plt.plot(xaxis, fres[idx], label = fs[idx][1])
    handles.append(handle)
  plt.legend(handles = handles)
  plt.show()

if __name__ == '__main__':
  main()
