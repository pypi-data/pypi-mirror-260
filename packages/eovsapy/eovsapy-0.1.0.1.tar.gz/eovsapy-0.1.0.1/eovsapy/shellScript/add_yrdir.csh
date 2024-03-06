#! /bin/csh

# Adds a directory for next year to pipeline output directories

#/data1/IFDB
#/data1/UFDB
#/data1/UDBTXT
#/data1/eovsa/fits/UDB
#/data1/eovsa/fits/XSP

setenv yrstr `date --date="1 year" +%Y`

set ext = "$yrstr"

mkdir /data1/IFDB/$ext
mkdir /data1/UFDB/$ext
mkdir /data1/UDBTXT/$ext
mkdir /data1/eovsa/fits/UDB/$ext
mkdir /data1/eovsa/fits/XSP/$ext

