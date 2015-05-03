# check() takes longitude and latitude and returns the name of the borough
# instead of "nybb_15a/nybb.shp" need to put the path to the shapefile

drv = ogr.GetDriverByName('ESRI Shapefile') #We will load a shape file
ds_in = drv.Open("nybb_15a/nybb.shp")    #Get the contents of the shape file
lyr_in = ds_in.GetLayer(0)
idx_reg = lyr_in.GetLayerDefn().GetFieldIndex("BoroName")
geo_ref = lyr_in.GetSpatialRef()
point_ref=ogr.osr.SpatialReference()
point_ref.ImportFromEPSG(4236)
ctran=ogr.osr.CoordinateTransformation(point_ref,geo_ref)

def check(lon, lat):
    #Transform incoming longitude/latitude to the shapefile's projection
    [lon,lat,z]=ctran.TransformPoint(lon,lat)

    #Create a point
    pt = ogr.Geometry(ogr.wkbPoint)
    pt.SetPoint_2D(0, lon, lat)

    #Set up a spatial filter such that the only features we see when we
    #loop through "lyr_in" are those which overlap the point defined above
    lyr_in.SetSpatialFilter(pt)

    #Loop through the overlapped features and display the field of interest
    for feat_in in lyr_in:
        return feat_in.GetFieldAsString(idx_reg)
