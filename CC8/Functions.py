# # # This is Coding Challenge 8
# # Retno Septiani (April, 2022)

# # This code generates define a HeatmapGenerator from CSV file by inputting the csv file extension


# # # Activate arcpy & CSV
import os
import glob
import arcpy
import csv

arcpy.env.overwriteOutput = True  # to prevent error due to 'file already exist'

# # # Change the path here
input_directory = r"C:\Users\Wulan\Documents\Phd\Spring 2022\NRS528\coding-challenges\CC8"
if not os.path.exists(os.path.join(input_directory, "output")):
    os.mkdir(os.path.join(input_directory, "output"))
if not os.path.exists(os.path.join(input_directory, "temp_files")):
    os.mkdir(os.path.join(input_directory, "temp_files"))
arcpy.env.workspace = input_directory
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

# defining the species list
def HeatmapGenerator(fileextension):
    species = []
    fileavailable = glob.glob(fileextension)
    for files in fileavailable:
        if arcpy.Exists(files):
            print('File available: ' + str(files))
            with open(str(files)) as speciesdata_csv:
                next(speciesdata_csv)  # skipping the first line
                for row in csv.reader(speciesdata_csv):
                    if row[4] not in species:
                        species.append(row[4])
            print("specieses available: " + str(species))

        # # 2. converting csv into a shp file
            for data in fileavailable:
                for i in species:
                    in_Table = str(data)
                    x_coords = "decimallongitude"
                    y_coords = "decimallatitude"
                    z_coords = ""
                    out_Layer = i
                    saved_Layer = str(i) + '.shp'
                    spRef = arcpy.SpatialReference(4326)  # # setting the spatial reference where 4326 == WGS 1984
                    # # system is creating the shp file
                    lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
                    # # saving the shp file
                    arcpy.CopyFeatures_management(lyr, os.path.join(input_directory, 'temp_files', saved_Layer))

                    # # # # 3. defining the extent
                os.chdir(os.path.join(input_directory, "temp_files"))# same as env.workspace
                arcpy.env.workspace = os.path.join(input_directory, "temp_files")
                for i in species:
                    if arcpy.Exists(str(i) + '.shp'):
                        print("CSV file converted successfully!")
                    desc = arcpy.Describe(str(i) + '.shp')
                    XMin = desc.extent.XMin
                    XMax = desc.extent.XMax
                    YMin = desc.extent.YMin
                    YMax = desc.extent.YMax
                    print("Extent:" "\nXMin = " + str(XMin) + "\nXMax = " + str(XMax) +
                          "\nYMin = " + str(YMin) + "\nYMax = " + str(YMax))
                    # # # 4. Creating Fishnet shp file
                    outFeatureClass = str(i) + "_Fishnet.shp"  # Name of output fishnet

                    # setting the fishnet area
                    originCoordinate = str(XMin) + " " + str(YMin)
                    yAxisCoordinate = str(XMin) + " " + str(YMin + 1)
                    cellSizeWidth = "5"  # # # i am using 5 x 5
                    cellSizeHeight = "5"
                    numRows = ""
                    numColumns = ""
                    oppositeCorner = str(XMax) + " " + str(YMax)
                    labels = "NO_LABELS"
                    templateExtent = "#"
                    geometryType = "POLYGON"

                    # system is generating the fishnet file
                    arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                                                   cellSizeWidth, cellSizeHeight, numRows, numColumns,
                                                   oppositeCorner, labels, templateExtent, geometryType)
                    if arcpy.Exists(outFeatureClass):
                        print("Created Fishnet file successfully!")

                    # # # 5. Joining the two shp file (fishnet and species coordinate)
                    target_features = str(i) + "_Fishnet.shp"
                    join_features = str(i) + '.shp'
                    out_heatmap = str(i) + "_heatmap.shp"
                    join_operation = "JOIN_ONE_TO_ONE"
                    join_type = "KEEP_ALL"
                    field_mapping = ""
                    match_option = "INTERSECT"
                    search_radius: str = ""
                    distance_field_name = ""

                    heatmap = arcpy.SpatialJoin_analysis(target_features, join_features, out_heatmap,
                                               join_operation, join_type, field_mapping, match_option,
                                               search_radius, distance_field_name)
                    arcpy.CopyFeatures_management(heatmap, os.path.join(input_directory, 'output', out_heatmap))
                    if arcpy.Exists(out_heatmap):
                        print("Created Heatmap file successfully!")
                arcpy.Delete_management(os.path.join(input_directory, "temp_files"))
        else:
            print('Dataset Not Found')

HeatmapGenerator('*.csv')