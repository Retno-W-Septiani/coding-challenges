# Coding Challenge 7

## Using the script from CC5, coding challenge 7 used OS and Glob to clean up the product files from the script. Temporary and Output files directory were created using OS then filtering out trash and final output using  arcpy.CopyFeatures_management to move the file to the right directory based on its criteria. 
## Glob was used to list CSV files in the directory, that way we can generate heatmap from multiple directory by using one script file as long as the CSV Tables are identical.
