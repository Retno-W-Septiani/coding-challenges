# # # This is Hydrology Bundle Toolbox for Toolbox Challenge
# # # by Retno Wulan Septiani, April 2022

# # In this Hydrology Bundle Toolbox, a DEM file will be the only input to generate four hydrology products
# which are : watershed boundary (shapefile), river streamline (shapefile), flow length (tif), and river distance (tif)

import arcpy
import os

arcpy.env.overwriteOutput = True
input_directory = r"C:\Users\Wulan\Documents\Phd\Spring 2022\NRS528\coding-challenges\Toolbox\DEMdata"
if not os.path.exists(os.path.join(input_directory, "output")):
    os.mkdir(os.path.join(input_directory, "output"))
if not os.path.exists(os.path.join(input_directory, "temp_files")):
    os.mkdir(os.path.join(input_directory, "temp_files"))
arcpy.env.workspace = input_directory
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

path = arcpy.env.workspace
list_DEM = arcpy.ListRasters("*", "TIF")
DEM_noExt = [os.path.splitext(x)[0] for x in list_DEM]
print('available DEM files: ' + str(list_DEM))
print('variables: ' + str(DEM_noExt))

for i in list_DEM:
    input_raster = str(i)
    output_fill = input_directory + '/' + 'temp_files/fill'
    fill = arcpy.sa.Fill(input_raster, None); fill.save(output_fill)


    output_direction = input_directory + '/' + 'temp_files/flow_dir'
    flow_direction = arcpy.sa.FlowDirection(output_fill, "NORMAL", None, "D8"); flow_direction.save(output_direction)

    output_accumulation = input_directory + '/' + 'temp_files/flow_acc'
    flow_accumulation = arcpy.sa.FlowAccumulation(output_direction, None, "FLOAT", "D8"); flow_accumulation.save(output_accumulation)

    output_streamOrder = input_directory + '/' + 'temp_files/stream_order'
    streamOrder = arcpy.sa.StreamOrder(output_accumulation, output_direction, "STRAHLER"); streamOrder.save(output_streamOrder)

    output_streamCondition = input_directory + '/' + 'temp_files/stream_con'
    streamCondition = arcpy.sa.Con(output_streamOrder, output_fill, None, "VALUE > 5");streamCondition.save(output_streamCondition)

    streamFeature = input_directory + '/' + 'output/' + str(DEM_noExt) + '_streamline'
    arcpy.sa.StreamToFeature(output_streamCondition, output_direction, streamFeature, "SIMPLIFY")

    output_Flowlength = input_directory + '/' + 'temp_files/_flow_len'
    flowLength = arcpy.sa.FlowLength(output_direction, "DOWNSTREAM", None); flowLength.save(output_Flowlength)

    output_watersheds = input_directory + '/' + 'temp_files/watersheds'
    basin = arcpy.sa.Basin(output_direction); basin.save(output_watersheds)

    watershedFeature = input_directory + '/' + 'output/' + str(DEM_noExt) + '_watersheds'
    arcpy.conversion.RasterToPolygon(output_watersheds,
                                     watershedFeature,
                                     "SIMPLIFY", "Value", "SINGLE_OUTER_PART", None)

    riverDistance = input_directory + '/' + 'temp_files/RiverDistance'
    euclidean_RiverDistance = arcpy.sa.EucDistance(streamFeature + '.shp', None, 0.0028572222245084, None, "PLANAR", None,
                                               None);euclidean_RiverDistance.save(riverDistance)
    arcpy.CopyRaster_management(riverDistance, input_directory + '/' + 'output/' + str(DEM_noExt) + '_riverdistance.tif')
    arcpy.CopyRaster_management(output_Flowlength,
                                input_directory + '/' + 'output/' + str(DEM_noExt) + '_Flowlength.tif')

arcpy.Delete_management(os.path.join(input_directory, "temp_files"))

