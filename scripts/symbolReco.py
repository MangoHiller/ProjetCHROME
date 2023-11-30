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
from convertInkmlToImg import parse_inkml,get_traces_data, getStrokesFromLG, convert_to_imgs, parseLG
from skimage.io import imsave
from classification.SymbolClassifier import SymbolClassifier

import numpy as np
from PIL import Image
import scipy.ndimage as ndimage


def usage():
    print ("usage: python3 symbolReco.py [-s] [-o fname][-w weigthFile] inkmlfile lgFile ")
    print ("     inkmlfile  : input inkml file name ")
    print ("     lgFile     : input LG file name")
    print ("     -o fname / --output fname : output file name (LG file)")
    print ("     -w fname / --weight fname : weight file name (nn pytorch file)")
    print ("     -s         : save hyp images")

"""
take an hypothesis (from LG = list of stroke index)
, select the corresponding strokes (from allTraces) and 
return the probability of being each symbol as a dictionnary {class_0 : score_0 ; ... class_i : score_i } 
Keep only the classes with a score higher than a threshold
"""

def CreateImageFromTraces(traces):
    im = convert_to_imgs(traces, 28)
    im = np.lib.pad(im, (2, 2), 'constant', constant_values=255)
    im = ndimage.gaussian_filter(im, sigma=(.5, .5), order=0)
    
    return Image.fromarray(im)


def computeClProb(alltraces, hyp, min_threshol, saveIm = False):
    #im = convert_to_imgs(get_traces_data(alltraces, hyp[1]), 28)
    im = CreateImageFromTraces(get_traces_data(alltraces, hyp[1]))
    if saveIm:
        imsave(hyp[0] + '.png', im)
    # create the list of possible classes (maybe connected to your classifier ???)
    classes = list("abcdefghijklmnoprstuvwxyzABCEFXYZ0123456789+-=(){}") # one character classes
    classes.extend(["div", "int", "sum", "pi", "gt", "geq","lt","leq"]) # add some other
    ##### call your classifier and fill the results ! #####
    symbol_classifier = SymbolClassifier()
    top_p, top_class = symbol_classifier.classify_symbol_img([im])

    result = {}
    for prob, class_idx in zip(top_p[0], top_class[0]):
        if prob > min_threshol:
            symbol = symbol_classifier.class_to_str(class_idx)
            result[symbol] = prob
    
    return result

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "so:w:", ["output=", "weight="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    if len(args) != 2:
        print("Not enough parameters")
        usage()
        sys.exit(2)
    inputInkml = args[0]
    inputLG = args[1]
    saveimg = False
    outputLG = ""
    weightFile = "myweight.nn"

    for o, a in opts:
        if o in ("-s"):
            saveimg = True
        elif o in ("-o", "--output"):
            outputLG = a
        elif o in ("-w", "--weight"):
            weightFile = a
        else:
            usage()
            assert False, "unhandled option"

    traces = parse_inkml(inputInkml)
    hyplist = open(inputLG, 'r').readlines()
    hyplist = parseLG(hyplist)
    output = ""
    for h in hyplist:
        # for each hypo, call the classifier and keep only slected classes (only the best or more)
        prob_dict = computeClProb(traces, h, 0.05, saveimg)
        #rewrite the new LG
        for cl, prob in prob_dict.items():
            output += "O,"+ h[0]+","+cl+","+str(prob)+","+",".join([str(s) for s in h[1]]) + "\n"
    if outputLG != "":
        with open(outputLG, "w") as text_file:
            print(output, file=text_file)
    else:
        print(output)


if __name__ == "__main__":
    # execute only if run as a script
    main()