import arcpy
import os
import csv

arcpy.env.overwriteOutput = True  # to prevent error due to 'file already exist'

# # # Change the path here
arcpy.env.workspace = r"C:\Users\Wulan\Documents\Phd\Spring 2022\NRS528\coding-challenges\Midterm-Coding-Challenge"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)
# #
# # Defining csv files
path = arcpy.env.workspace
all_files = os.listdir(arcpy.env.workspace)
csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))
csv_noExt = [os.path.splitext(x)[0] for x in csv_files]
print('available csv files: ' + str(csv_files))
print('variables: ' + str(csv_noExt))

# opening csv files
for i in csv_files:
    file = open(i, "r")
    csv_reader = csv.reader(file)
    # # #  converting csv into a shp file
    in_Table = i
    x_coords = "x"
    y_coords = "y"
    z_coords = ""
    for variables in csv_noExt:
        out_Layer = variables
        saved_Layer = str(variables) + '.shp'
        spRef = arcpy.SpatialReference(4326)  # # setting the spatial reference where 4326 == WGS 1984
        # # system is creating the shp file
        lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
        # # saving the shp file
        arcpy.CopyFeatures_management(lyr, saved_Layer)
if arcpy.Exists(saved_Layer):
    print("CSV files converted successfully!")

for variables in csv_noExt:
    inFeatures = str(variables) + '.shp'
    outFeatureClass = str(variables) + 'thiessen.shp'
    outFields = "ALL"

    # Execute CreateThiessenPolygons
    arcpy.CreateThiessenPolygons_analysis(inFeatures, outFeatureClass, outFields)

    arcpy.Clip_analysis(str(variables) + 'thiessen.shp', 'Municipalities__1989_.shp', str(variables) + 'coverage.shp')

for variables in csv_noExt:
    inFeatures = str(variables) + 'coverage.shp'
    fieldName1 = "area"
    fieldPrecision = 10
    fieldScale = 2
    expression = '!shape.geodesicArea@Squaremiles!'
    arcpy.management.AddField(inFeatures, fieldName1, 'DOUBLE', fieldPrecision, fieldScale)
    arcpy.CalculateField_management(inFeatures, fieldName1, expression, "PYTHON3")

for variables in csv_noExt:
    inFeatures = str(variables) + 'coverage.shp'
    fieldName1 = "area"
    fields = ['FACNAME', 'area']
    with arcpy.da.SearchCursor(inFeatures, fields) as cursor:
        for row in cursor:
            print(row)  # # # the firestation didn't get printed