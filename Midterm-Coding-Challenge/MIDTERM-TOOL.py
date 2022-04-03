# # # This is MIDTERM-TOOL Coding Challenge
# # # Retno Septiani (Wulan), March 2022

# # # In this code, I tried to generate coverage area of the public facilities using thiessen polygon
# # # I downloaded the Rhode Island Hospital and Fire Station data from https://www.rigis.org/

# # Each Thiessen polygon defines an area of influence around its sample point,
# # so that any location inside the polygon is closer to that point than any of the other sample points

# # In hydrology, Thiessen polygon is used to calculate the influence of rainfal stations in a watershed

import arcpy
import os
import csv

arcpy.env.overwriteOutput = True  # to prevent error due to 'file already exist'

# # # Change the path here
arcpy.env.workspace = r"C:\Users\Wulan\Documents\Phd\Spring 2022\NRS528\coding-challenges\Midterm-Coding-Challenge"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

# # Defining csv files in the directory
# # There are two CSV files containing the facility, and both files has been adjusted to have the same column
path = arcpy.env.workspace
all_files = os.listdir(arcpy.env.workspace)
csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))
csv_noExt = [os.path.splitext(x)[0] for x in csv_files]
print('available csv files: ' + str(csv_files))
print('variables: ' + str(csv_noExt))

# # opening csv files
for i in csv_files:
    file = open(i, "r")
    variable = os.path.splitext(i)[0]
    csv_reader = csv.reader(file)
    # # #  converting csv into a shp file
    in_Table = i
    x_coords = "x"
    y_coords = "y"
    z_coords = ""
    out_Layer = variable
    saved_Layer = str(variable) + '.shp'
    spRef = arcpy.SpatialReference(4326)  # # setting the spatial reference where 4326 == WGS 1984
    # # system is creating the shp file
    lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
    # # saving the shp file
    arcpy.CopyFeatures_management(lyr, saved_Layer)
    if arcpy.Exists(saved_Layer):
        print("CSV files converted successfully!")

    # # Now that the CSV Have been converted to Shapefiles, Thiessen Polygons will be generated
    # # based on the location of each facility
    inFeatures = str(variable) + '.shp'
    outFeatureClass = str(variable) + 'thiessen.shp'
    outFields = "ALL"
    # # Thiessen polygon generating tools
    arcpy.CreateThiessenPolygons_analysis(inFeatures, outFeatureClass, outFields)
    if arcpy.Exists(outFeatureClass):
        print("Thiessen Polygons generated successfully!")

    # # The Polygons are created without boundaries
    # # This section clips the polygon using Rhode Island Boundary
    arcpy.Clip_analysis(str(variable) + 'thiessen.shp', 'Municipalities__1989_.shp', str(variable) + 'coverage.shp')
    if arcpy.Exists(str(variable) + 'coverage.shp'):
        print("Facilities Coverage generated successfully!")

    # # To find out about the 'area' of the coverage, it needs to be calculated
    # # But first, add a new field named 'area' in the attribute tables
    inFeatures = str(variable) + 'coverage.shp'
    fieldName1 = "area"
    fieldPrecision = 10
    fieldScale = 2
    expression = '!shape.geodesicArea@Squaremiles!'  # # Calculate geometry with square mile as the unit
    arcpy.management.AddField(inFeatures, fieldName1, 'DOUBLE', fieldPrecision, fieldScale)
    arcpy.CalculateField_management(inFeatures, fieldName1, expression, "PYTHON3")
    if arcpy.Exists(fieldName1):
        print("Area field added in the attribute tables")
        print("Calculating the area.....")

    # # Pulling out the information of Facility name and it's area of coverage from attribute tables
    inFeatures = str(variable) + 'coverage.shp'
    fieldName1 = "area"
    fields = ['FACNAME', 'area']
    with arcpy.da.SearchCursor(inFeatures, fields) as cursor:
        print(str(variable) + 'area of coverage:')
        for row in cursor:
            print(row)
