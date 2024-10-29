# Set the base name for the zip file
base_name="generated_images"
zip_file="${base_name}.zip"
counter=1

# Check if the zip file already exists and increment the counter if it does
while [[ -e "$zip_file" ]]; do
    zip_file="${base_name}_${counter}.zip"
    ((counter++))
done

# Create the zip file with the generated images
zip -r "$zip_file" generated_images/

# Delete the images after zipping
rm -rf generated_images/*
