// Import required modules
import fs from 'fs';
import { execSync } from 'child_process';

// Set the base name for the zip file
const baseName = 'generated_images';
let zipFile = `${baseName}.zip`;
let counter = 1;

// Check if the zip file already exists and increment the counter if it does
while (fs.existsSync(zipFile)) {
    zipFile = `${baseName}_${counter}.zip`;
    counter++;
}

// Create the zip file with the generated images
execSync(`zip -r "${zipFile}" generated_images/`);

console.log(`Zipped files into: ${zipFile}`);

// Check if the images folder exists before attempting to delete
const imagesPath = 'generated_images/';
if (fs.existsSync(imagesPath)) {
    // Delete all images in the folder
    fs.rmSync(imagesPath, { recursive: true, force: true });
    console.log(`Deleted all images in: ${imagesPath}`);
} else {
    console.log(`No images found in: ${imagesPath}`);
}
