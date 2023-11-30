#!/bin/bash


if [ $# -lt 2 ]
then
	echo "generate the list of existing LG files with ground-thruth "
	echo "Copyright (c) H. Mouchere, 2018"
	echo ""
	echo "Usage: processAll <ground-truthdir> <output_lg_dir>"
	echo ""
fi

GTDIR=$1
OUTDIR=$2

if ! [ -d $OUTDIR ] 
then
	echo $OUTDIR "should exist"
	exit 2
fi

if ! [ -d $GTDIR ] 
then
	echo $GTDIR "should exist"
	exit 2
fi

for file in $OUTDIR/*.lg
do
	BNAME=`basename $file .lg`
	echo $file $GTDIR/$BNAME.lg
done
