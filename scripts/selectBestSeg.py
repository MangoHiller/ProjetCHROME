################################################################
# symbolReco.py
#
# Program that select hypothesis of segmentation
#
# Author: H. Mouchere, Dec. 2018
# Copyright (c) 2018, Harold Mouchere
################################################################
import sys
import random
import itertools
import sys, getopt
from convertInkmlToImg import parse_inkml,get_traces_data, getStrokesFromLG, convert_to_imgs
from skimage.io import imsave


def usage():
    print ("usage: python3 selectBestSeg.py  [-o fname] lgFile ")
    print ("     lgFile     : input LG file name")
    print ("     -o fname / --output fname : output file name (LG file)")

"""
take a set of hypothesis (from LG = list of list of stroke indexes), select one coherent segmentation (each stroke is 
used only once) with a greedy sub-optimal algorithm 
"""

def parseLGscore(LG):
    sym = []
    for lg in LG:
        # Remove whitespace and split by ","
        lg = lg.replace(" ", "").replace('\n', '').split(',')
        #print(lg)
        if lg[0] != "O": continue
        # Select symbol id and associated stroke id (only integers)
        sym.append({'id' : lg[1], 'cl' : lg[2], 'sc' : float(lg[3]), 'strk' : set( lg[4:]) })
    return sym


def selectBestSeg(LGlist):
    # sort by decreasing score
    LGlist.sort(key= lambda x : -x['sc'])
    setStr =  set()
    bestLG = []
    while (len(LGlist) > 0):
        besthyp = LGlist.pop()
        bestLG.append(besthyp)
        setStr = setStr | besthyp['strk'] #union of stroke lists
        LGlist = list(filter(lambda x: x['strk'].isdisjoint(setStr) , LGlist)) # remove impossible hypothesis
        print(LGlist)
    return bestLG

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:", ["output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    if len(args) != 1:
        print("Not enough parameters")
        usage()
        sys.exit(2)
    inputLG = args[0]
    outputLG = ""

    for o, a in opts:
        if o in ("-o", "--output"):
            outputLG = a
        else:
            usage()
            assert False, "unhandled option"


    hyplist = open(inputLG, 'r').readlines()
    hypset = parseLGscore(hyplist)
    print(hypset)
    bestLG = selectBestSeg(hypset)
    print("Best : " + str(bestLG))
    output = ""
    for symb in bestLG:
        output += "O," + symb['id'] + "," + symb['cl'] + "," + str(symb['sc']) + "," + ",".join([str(s) for s in symb['strk']]) + "\n"

    if outputLG != "":
        with open(outputLG, "w") as text_file:
            print(output, file=text_file)
    else:
        print(output)


if __name__ == "__main__":
    # execute only if run as a script
    main()