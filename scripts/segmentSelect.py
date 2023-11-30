################################################################
# segmentSelect.py
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
from convertInkmlToImg import parse_inkml,get_traces_data, getStrokesFromLG, convert_to_imgs, parseLG
from skimage.io import imsave


def usage():
    print ("usage: python3 [-o fname] [-s] segmentSelect.py inkmlfile lgFile ")
    print ("     inkmlfile  : input inkml file name ")
    print ("     lgFile     : input LG file name")
    print ("     -o fname / --output fname : output file name (LG file)")
    print ("     -s         : save hyp images")

"""
take an hypothesis (from LG = list of stroke index), select the corresponding strokes (from allTraces) and 
return the probability of being a good segmentation [0:1]  
"""
def computeProbSeg(alltraces, hyp, saveIm = False):
    im = convert_to_imgs(get_traces_data(alltraces, hyp[1]), 28)
    if saveIm:
        imsave(hyp[0] + '.png', im)
    ##### call your classifier ! #####
    return random.random()

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "so:", ["output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    if len(args) < 2:
        print("Not enough parameters")
        usage()
        sys.exit(2)
    inputInkml = args[0]
    inputLG = args[1]
    saveimg = False
    outputLG = ""
    for o, a in opts:
        if o in ("-s"):
            saveimg = True
        elif o in ("-o", "--output"):
            outputLG = a
        else:
            usage()
            assert False, "unhandled option"
    traces = parse_inkml(inputInkml)
    hyplist = open(inputLG, 'r').readlines()
    hyplist = parseLG(hyplist)
    output = ""
    for h in hyplist:
        prob = computeProbSeg(traces, h, saveimg)
        #### select your threshold
        if prob > 0.2:
            output += "O,"+ h[0]+",*,"+str(prob)+","+",".join([str(s) for s in h[1]]) + "\n"
    if outputLG != "":
        with open(outputLG, "w") as text_file:
            print(output, file=text_file)
    else:
        print(output)


if __name__ == "__main__":
    # execute only if run as a script
    main()