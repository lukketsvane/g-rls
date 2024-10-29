#!/bin/bash

# Define the directory to zip and the base name for the zip file
DIR="generated_images"
BASE_NAME="generated_images"
ZIP_FILE="${BASE_NAME}.zip"
COUNT=1

# Check if the zip file already exists and increment the number if it does
while [[ -e $ZIP_FILE ]]; do
    ZIP_FILE="${BASE_NAME}_${COUNT}.zip"
    COUNT=$((COUNT + 1))
done

# Create the zip file
zip -r "$ZIP_FILE" "$DIR"

echo "Zipped folder '$DIR' into '$ZIP_FILE'"

# Delete the images in the directory after zipping
rm -rf "$DIR/*"

echo "Deleted all images in '$DIR'"
