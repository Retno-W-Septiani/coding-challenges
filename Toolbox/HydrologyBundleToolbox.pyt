# # # This is Hydrology Bundle Toolbox for Toolbox Challenge
# # # by Retno Wulan Septiani, April 2022

# # In this Hydrology Bundle Toolbox, a DEM file will be the only input to generate four hydrology products
# which are : watershed boundary (shapefile), river streamline (shapefile), flow length (tif), and river distance (tif)

import arcpy
import os

arcpy.env.overwriteOutput = True
input_directory = r"C:\Users\Wulan\Documents\Phd\Spring 2022\NRS528\coding-challenges\Toolbox\DEMdata"

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Hydrology Bundle Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [HydrologyBundleToolbox]

class HydrologyBundleToolbox(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Hydrology Bundle Toolbox"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_DEM = arcpy.Parameter(name="input_DEM",
                                     displayName="Input DEM",
                                     datatype="DERasterDataset",
                                     parameterType="Required",  # Required
                                     direction="Input",  # Input DEM
                                     )
        # input_DEM.value = "DEMRI.tif"  # This is a default value that can be over-ridden in the toolbox
        params.append(input_DEM)

        output_river = arcpy.Parameter(name="output_river",
                                 displayName="Output River",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",  # Required
                                 direction="Output",  # Output
                                 )
        # output_river.value = "river.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(output_river)

        output_watershed = arcpy.Parameter(name="outputwatershed",
                                 displayName="Output Watershed",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",  # Required
                                 direction="Output",  # Output
                                 )
        # output_watershed.value = "watershed.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(output_watershed)

        output_flowlength = arcpy.Parameter(name="outputflowlength",
                                 displayName="Output Flow Length",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required
                                 direction="Output",  # Output
                                 )
        # output.value = "flow_length.tif"  # This is a default value that can be over-ridden in the toolbox
        params.append(output_flowlength)

        output_riverdistance = arcpy.Parameter(name="outputriverdistance",
                                 displayName="Output Euclidean Distance",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required
                                 direction="Output",  # Output
                                 )
        # output.value = "river_distance.tif"  # This is a default value that can be over-ridden in the toolbox
        params.append(output_riverdistance)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_DEM = parameters[0].valueAsText
        output_river = parameters[1].valueAsText
        output_watershed = parameters[2].valueAsText
        output_flowlength = parameters[3].valueAsText
        output_riverdistance = parameters[4].valueAsText

        # # # Setting up the environment and temporary folder
        if not os.path.exists(os.path.join(input_directory, "temp_files")):
            os.mkdir(os.path.join(input_directory, "temp_files"))
        arcpy.env.workspace = input_directory
        arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

        # # Fill (Spatial Analyst): Fills sinks in a surface raster to remove small imperfections in the data,
        # it locates and generates sinks
        output_fill = input_directory + '/' + 'temp_files/fill'
        fill = arcpy.sa.Fill(input_DEM, None); fill.save(output_fill)

        # # Flow direction (Spatial Analyst): Creates a raster of flow direction from each cell to its
        # down-slope neighbors
        output_direction = input_directory + '/' + 'temp_files/flow_dir'
        flow_direction = arcpy.sa.FlowDirection(output_fill, "NORMAL", None, "D8"); flow_direction.save(output_direction)

        # # Flow Accumulation (Spatial Analyst): The result of Flow Accumulation is a raster of accumulated
        # flow to each cell,nas determined by accumulating the weight for all cells that flow into each downslope cell
        output_accumulation = input_directory + '/' + 'temp_files/flow_acc'
        flow_accumulation = arcpy.sa.FlowAccumulation(output_direction, None, "FLOAT", "D8"); flow_accumulation.save(output_accumulation)

        # # Stream Order (Spatial Analyst): Assigns a numeric order to segments of a raster representing
        # branches of a linear network
        output_streamOrder = input_directory + '/' + 'temp_files/stream_order'
        streamOrder = arcpy.sa.StreamOrder(output_accumulation, output_direction, "STRAHLER"); streamOrder.save(output_streamOrder)


        # # Con (Spatial Analyst): Performs a conditional if/else evaluation on each of the input
        # cells of an input raster
        output_streamCondition = input_directory + '/' + 'temp_files/stream_con'
        streamCondition = arcpy.sa.Con(output_streamOrder, output_fill, None, "VALUE > 5");streamCondition.save(output_streamCondition)


        # # Stream to Feature (Spatial Analyst): Converts a raster representing a linear network to features
        # representing the linear network
        streamFeature = output_river
        arcpy.sa.StreamToFeature(output_streamCondition, output_direction, streamFeature, "SIMPLIFY")

        # # Flow Length (Spatial Analyst): Calculates the upstream or downstream distance, or weighted distance, along the
        # flow path for each cell
        output_Flowlength = input_directory + '/' + 'temp_files/_flow_len'
        flowLength = arcpy.sa.FlowLength(output_direction, "DOWNSTREAM", None); flowLength.save(output_Flowlength)


        # # Basin (Spatial Analyst): Creates a raster delineating all drainage basins (generate watersheds boundaries)
        output_watersheds = input_directory + '/' + 'temp_files/watersheds'
        basin = arcpy.sa.Basin(output_direction); basin.save(output_watersheds)

        # # Raster to Polygon conversion
        # # Generating watershed boundary as a shapefile
        watershedFeature = output_watershed
        arcpy.conversion.RasterToPolygon(output_watersheds,
                                         watershedFeature,
                                         "SIMPLIFY", "Value", "SINGLE_OUTER_PART", None)

        # # Generating Euclidean Distance of the river networks for flood risk analysis purpose
        riverDistance = input_directory + '/' + 'temp_files/RiverDistance'
        euclidean_RiverDistance = arcpy.sa.EucDistance(streamFeature + '.shp', None, 0.0028572222245084, None, "PLANAR", None,
                                                   None);euclidean_RiverDistance.save(riverDistance)

        # # Extracting River Distance and Flowlength into TIF files
        arcpy.CopyRaster_management(riverDistance, output_riverdistance)
        arcpy.CopyRaster_management(output_Flowlength,
                                    output_flowlength)

        arcpy.Delete_management(os.path.join(input_directory, "temp_files"))
        return



# def main():
#     tool = HydrologyBundleToolbox()  # # i.e. what you have called your tool class: class Clippy(object):
#     tool.execute(tool.getParameterInfo(), None)
#
# if __name__ == '__main__':
#     main()