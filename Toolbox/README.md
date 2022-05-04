# This is Hydrology Bundle Toolbox
<<<<<<< HEAD
### In this Hydrology Bundle Toolbox, a DEM file will be the only input to generate four hydrology products which are : watershed boundary (shapefile), river streamline (shapefile), flow length (tif), and river distance (tif)
### Multiple steps are needed to delineate or generate watersheds boundary using Arc-GIS,  such as:
1. Fill (Spatial Analyst)
2. Flow Direction (Spatial Analyst) , using Fill output as an input
3. Flow Accumulation (Spatial Analyst), using flow direction output as an input
4. Basin (Spatial Analyst), to generate the watershed delineation

### Though, other product may use the same steps to generate different hydrology output, such as generating River Network:
1. Stream Order (Spatial Analyst), using Flow Accumulation output as an input
2. Con (Spatial Analyst), to set up specific conditions for the stream neatworks to be shown (e.g only streamline value > 5 are shown)
3. Stream to Feature , to generate the shapefile of the stream networks

### Flow length, to weight and determine the upstream and downstream area of a stream networks:
1. Flow Length (Spatial Analyst), using flow direction output as an input
2. Copy Raster , to generate the TIF file

### Lastly, River Euclidean Distance for flood risk analysis purpose:
1. Euclidean Distance, using Stream Features as an input
2. Copy Raster , to generate the TIF file

### Overall, with this Hydrology Bundle Toolbox, we do not need to go back and forth to the toolbox and get confused to select the input

### The results are shown below:
=======
## The result is here
>>>>>>> 1667e7f39b461c48af9b4da7a828cc12dcfe2036
<p align="center" width="100%">
    <img width="150%" src="https://github.com/Retno-W-Septiani/coding-challenges/blob/main/Toolbox/Result.jpg">
</p>

