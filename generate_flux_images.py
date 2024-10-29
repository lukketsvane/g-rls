import Replicate from "replicate";
import fetch from "node-fetch";
import fs from "fs";
import path from "path";
import dotenv from "dotenv";
import readline from "readline";

dotenv.config();

// Initialize Replicate client with API key
const replicate = new Replicate({
    auth: process.env.REPLICATE_API_TOKEN,
});

// Function to generate images in both portrait and landscape for each prompt
async function generateImage(prompt, index) {
    try {
        // Define aspect ratios for portrait and landscape
        const aspectRatios = [
            { ratio: "9:12", name: "portrait" }, // Wider portrait
            { ratio: "12:9", name: "landscape" }  // Wider landscape
        ];

        // Loop through each aspect ratio to generate images
        for (const { ratio, name } of aspectRatios) {
            // Run the model with the specified aspect ratio
            const output = await replicate.run("black-forest-labs/flux-schnell", {
                input: { prompt, safety_checker: false, aspect_ratio: ratio },
            });

            // Check if an image URL was returned
            const imageUrl = output ? output[0] : null;
            if (!imageUrl) {
                console.error(`No URL generated for prompt: "${prompt}"`);
                return;
            }

            console.log(`Generated Image URL for prompt "${prompt}" (${name}):`, imageUrl);

            // Fetch the image from the URL
            const response = await fetch(imageUrl);
            const buffer = await response.arrayBuffer();

            // Create a unique filename using prompt snippet, index, timestamp, and aspect ratio
            const timestamp = Date.now();
            const promptSnippet = prompt.slice(0, 15).replace(/\s+/g, "_"); // First 15 characters
            const filePath = path.join(
                process.cwd(),
                "generated_images",
                `${promptSnippet}_${index + 1}_${timestamp}_${name}.jpg`
            );
            fs.writeFileSync(filePath, Buffer.from(buffer));

            console.log(`Image saved to: ${filePath}`);
        }
    } catch (error) {
        console.error(`Error generating images for prompt "${prompt}":`, error);
    }
}

// Function to read prompts from a text file and generate images
async function processPrompts() {
    const fileStream = fs.createReadStream("prompts.txt");
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity,
    });

    let index = 0;
    for await (const line of rl) {
        const prompt = line.trim();
        if (prompt) {
            await generateImage(prompt, index);
            index++;
        }
    }

    console.log("All images generated and saved.");
}

// Run the process
processPrompts();
