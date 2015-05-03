#!/usr/bin/python

import sys
import re
import ogr

# Reading in shapefiles
shapefile = ogr.GetDriverByName('ESRI Shapefile') 
borders = shapefile.Open("/Users/denisstukal/Dropbox/2015_SPRING/Big_Data/Final_project/nybb_15a/nybb.shp")    
layer = borders.GetLayer(0)
boroColumn = layer.GetLayerDefn().GetFieldIndex("BoroName")
geo_ref = layer.GetSpatialRef()
point_ref=ogr.osr.SpatialReference()
point_ref.ImportFromEPSG(4236)
ctran=ogr.osr.CoordinateTransformation(point_ref,geo_ref)

# Defining the function for geolocation
def check(long, latit):
    # Project longitude/latitude from the argument
    [lon,lat,z]=ctran.TransformPoint(long,latit)

    #Create a point
    point = ogr.Geometry(ogr.wkbPoint)
    point.SetPoint_2D(0, lon, lat)

    #Spatial filter such that the only features we see when we
    layer.SetSpatialFilter(point)

    #Loop over the overlapped features
    for features in layer:
        return features.GetFieldAsString(boroColumn)


currentCommonKey = None
currentRest = None

for line in sys.stdin:
    (common, rest) = line.strip().split("\t")
    common = re.sub(r'\(|\[|\)|\]|\'|\"', '', common)
    rest = re.sub(r'\(|\[|\)|\]|\'|\"', '', rest)
    rest = rest.split(",")
    # Block for the first input
    if currentCommonKey == None:
        currentCommonKey = common
        currentRest = rest
        continue
    # Block for all inputs after the 1st one
    else:
        # If the input is the same as the previous one, merge and print
        if common == currentCommonKey:
            # Check the order for merging
            if (re.search(r'Trips', currentRest[0]) and re.search(r'Fares', rest[0])):
                # Get coordinates 
                pickup_long = float(currentRest[4])
                pickup_lat = float(currentRest[5])
                drop_long = float(currentRest[6])
                drop_lat = float(currentRest[7])
                # Use coordinates for geolocation, if not geolocated, get 'error'
                if check(pickup_long, pickup_lat):
                	pick_boro = check(pickup_long, pickup_lat)
                else:
                	pick_boro = 'error'
                if check(drop_long, drop_lat):
                	drop_boro = check(drop_long, drop_lat)
                else:
                	drop_boro = 'error'
            	
            	# Produce the string to print it out
                currentRestString = str(currentRest[1:]) + ', ' + pick_boro + ', ' + drop_boro
                restString = str(rest[1:])
                stringToPrint = "%s, %s, %s" % (common, currentRestString, restString)
                # Remove [(]) from the string
                stringToPrintClean = re.sub(r'\(|\[|\)|\]|\'|\"', '', stringToPrint)
                print stringToPrintClean
            elif (re.search(r'Trips', rest[0]) and re.search(r'Fares', currentRest[0])):
                currentRestString = str(currentRest[1:])
                pickup_long = float(rest[4])
                pickup_lat = float(rest[5])
                drop_long = float(rest[6])
                drop_lat = float(rest[7])
                if check(pickup_long, pickup_lat):
                	pick_boro = check(pickup_long, pickup_lat)
                else:
                	pick_boro = 'error'
                if check(drop_long, drop_lat):
                	drop_boro = check(drop_long, drop_lat)
                else:
                	drop_boro = 'error'
                
                restString = str(rest[1:]) + ', ' + pick_boro + ', ' + drop_boro
                stringToPrint = "%s, %s, %s" % (common, restString, currentRestString)
                stringToPrintClean = re.sub(r'\(|\[|\)|\]|\'|\"', '', stringToPrint)
                print stringToPrintClean
            else:
                continue
        # Otherwise, reassign currentCommonKey and currentRest
        else:
            currentCommonKey = common
            currentRest = rest
