# # # This is Coding Challenge 9
# # # By Retno Wulan Septiani (April, 2022)

# # In this coding challenge, cursor function is utilized to modify some information in the attribute table

import arcpy

arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"C:\Users\Wulan\Documents\Phd\Spring 2022\NRS528\coding-challenges\CC9"  # # Change the path here

input_shp = r'C:\Users\Wulan\Documents\Phd\Spring 2022\NRS528\coding-challenges\CC9\CC9Data\RI_Forest_Health_Works_Project%3A_Points_All_Invasives.shp'
field = ['photo']  # # I manually typed the field just to be more specific

# # Creating a list of the feature classes under the chosen field
photoAvailability = []
with arcpy.da.SearchCursor(input_shp, field) as cursor:
    for row in cursor:
        if row[0] not in photoAvailability:
            photoAvailability.append(row[0])
print(photoAvailability)

# # Answer for Question 1
# # Counting the number of each photo availability (for either yes and no)
availabilityCount = {}
with arcpy.da.SearchCursor(input_shp, field) as cursor:
    for row in cursor:
        availability = row[0]
        for i in photoAvailability:
            if i == availability:
                if i not in availabilityCount.keys():
                    availabilityCount[i] = 1
                else:
                    availabilityCount[i] += 1
print(availabilityCount)


# # Answer for Question 2
field2 = ['Species']
species = []

with arcpy.da.SearchCursor(input_shp, field2) as cursor:
    for row in cursor:
        if row[0] not in species:
            if row[0] != ' ':
                species.append(row[0])
print('There are ' + str(len(species)) + ' species recorded')



# # Answer for Question 3
# # First for ones with photos
expression = arcpy.AddFieldDelimiters(input_shp, 'photo') + " = 'y'"
try:
    # # Selecting the layer by attribute, in this case is for ones with photo
    input2 = arcpy.SelectLayerByAttribute_management(input_shp, 'NEW_SELECTION', expression)
    # # Generating shapefile from selected attributes
    arcpy.CopyFeatures_management(input2, 'RecordsWithPhotos.shp')
except:
   print(arcpy.GetMessages())
if arcpy.Exists('RecordsWithPhotos.shp'):
    print("A Shapefile of records with photos has been generated")

# # for ones without photos
expression2 = arcpy.AddFieldDelimiters(input_shp, 'photo') + " = ' '"
try:
    # # Selecting the layer by attribute, in this case is for ones without photo
    input2 = arcpy.SelectLayerByAttribute_management(input_shp, 'NEW_SELECTION', expression2)
    # # Generating shapefile from selected attributes
    arcpy.CopyFeatures_management(input2, 'RecordsWithoutPhotos.shp')
except:
   print(arcpy.GetMessages())
if arcpy.Exists('RecordsWithoutPhotos.shp'):
    print("A Shapefile of records without photos has been generated")

