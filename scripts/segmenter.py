################################################################
# segmenter.py
#
# Program that generate hypothesis of segmentation
#
# Author: H. Mouchere, Dec. 2018
# Copyright (c) 2018, Harold Mouchere
################################################################
import sys
import random
import itertools
import sys, getopt
from convertInkmlToImg import parse_inkml

def generateHypSeg(nbStrk, strDict = None, nb=-1, nbStrkMax=4, k=0):
    """generate segmentation hypothesis. If nb=-1, it will generate all seg.
    nbStrkMax is the maximum number of strokes of the generated hypothesis
    strDict is used if stroke ids are not numbered from 0 to nbStrk -1
    Hypothesis are generated with continuous index in the ink file (no time jump)"""

    StrokesList = range(nbStrk)
    if strDict is None:
        strDict = {}
        for i in StrokesList:
            strDict [i] = i
    AllHypMatrix = []
    if (nbStrkMax > nbStrk):
        nbStrkMax = nbStrk
    for itNbMaxOfStrkPerObj in range(nbStrkMax):
        itNbMaxOfStrkPerObj += 1
        # add all possible segments
        # AllHypMatrix.extend(itertools.combinations(StrokesList,itNbMaxOfStrkPerObj))
        # or add only seg without time jump
        for i in StrokesList:
            if i + itNbMaxOfStrkPerObj <= nbStrk:
                r = range(i, i + itNbMaxOfStrkPerObj)
                # get real id of the strokes (strings)
                seg = []
                for s in r:
                    seg.append(strDict[s])
                AllHypMatrix.append(seg)
    if nb > -1 and nb < len(AllHypMatrix):
        AllHypMatrix = random.sample(AllHypMatrix, nb)
    return AllHypMatrix

def toLG(setHyp):
    output = ""
    for i, hyp in enumerate(setHyp):
        output += "O,hyp"+str(i) +",*,1.0,"+ ",".join([str(s) for s in hyp]) + "\n"

    return output


def usage():
    print ("usage: python3 segmenter.py [-i fname][-o fname][-s N]")
    print ("     -i fname / --inkml fname  : input file name (inkml file)")
    print ("     -o fname / --output fname : output file name (LG file)")
    print ("     -s N / --str N            : if no inkmlfile is selected, run with N strokes")

def main():
    nbs = 4;
    inputInkml = ""
    outputLG = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:s:", ["inkml=", "output=", "str="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-s", "--str"):
            nbs = int(a)
            if nbs < 1:
                print ("wrong parameter value : nbs should be > 0")
                usage()
                sys.exit(2)
        elif o in ("-i", "--inkml"):
            inputInkml = a
        elif o in ("-o", "--output"):
            outputLG = a
        else:
            assert False, "unhandled option"

    if inputInkml != "":
        nbs = len(parse_inkml(inputInkml))
    hyp = generateHypSeg(nbs)
    txtLG = toLG(hyp)
    if outputLG != "":
        with open(outputLG, "w") as text_file:
            print(txtLG, file=text_file)
    else:
        print(txtLG)

if __name__ == "__main__":
    # execute only if run as a script
    main()