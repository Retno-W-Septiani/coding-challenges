# # # Activate arcpy
import arcpy
import csv

arcpy.env.overwriteOutput = True  # to prevent error due to 'file already exist'

# # # Change the path here
arcpy.env.workspace = r"C:\Users\Wulan\Documents\Phd\Spring 2022\NRS528\coding-challenges\CC5"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

# # # 1. Inputting species names into a list
file = open("2specieses.csv", "r")  # # # If you wanna change the csv data
csv_reader = csv.reader(file)

# defining the species list
species = []
with open("2specieses.csv") as speciesdata_csv:
    next(speciesdata_csv)  # skipping the first line

    for row in csv.reader(speciesdata_csv):
        if row[4] not in species:
            species.append(row[4])
print("specieses available: " + str(species))

# I am still trying to figure out how to put the species list into the arcpy automation code
# # # 2. converting csv into a shp file
for i in species:
    in_Table = "2specieses.csv"  # # # I really wanna automate this one so we don't need to change it, but still trying
    x_coords = "decimallongitude"
    y_coords = "decimallatitude"
    z_coords = ""
    out_Layer = i
    saved_Layer = str(i) + '.shp'
    spRef = arcpy.SpatialReference(4326)  # # setting the spatial reference where 4326 == WGS 1984
    # # system is creating the shp file
    lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
    # # saving the shp file
    arcpy.CopyFeatures_management(lyr, saved_Layer)
    if arcpy.Exists(saved_Layer):
        print("CSV file converted successfully!")
    # # # # 3. defining the extent
    desc = arcpy.Describe(saved_Layer)
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
    out_feature_class = str(i) + "_heatmap.shp"
    join_operation = "JOIN_ONE_TO_ONE"
    join_type = "KEEP_ALL"
    field_mapping = ""
    match_option = "INTERSECT"
    search_radius: str = ""
    distance_field_name = ""

    arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                               join_operation, join_type, field_mapping, match_option,
                               search_radius, distance_field_name)

    if arcpy.Exists(out_feature_class):
        print("Created Heatmap file successfully!")
        # print("Deleting intermediate files")
        # arcpy.Delete_management(target_features)
        # arcpy.Delete_management(join_features)
    #
    #
