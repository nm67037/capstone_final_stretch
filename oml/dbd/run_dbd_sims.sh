#!/bin/bash

# Array of Radii and GAP HEIGHTS to test (Format: RADIUS_GAP)
# Note: DBDs require very small gaps compared to vacuum chambers!
DIMENSIONS=("5.0_0.5" "5.0_1.5" "8.0_2.0")

# Array of Power Levels (1=Low, 2=Med, 3=High)
POWERS=(1 2 3)

# Clear out any old temporary images
rm -f temp_dbd_*.png

echo "Starting batch generation of DBD simulations..."

# Keep track of all generated image filenames
IMAGE_LIST=""

# Loop through all dimensions and powers
for dim in "${DIMENSIONS[@]}"; do
    # Split the dim string into radius and gap height
    IFS="_" read -r radius height <<< "$dim"
    
    for power in "${POWERS[@]}"; do
        filename="temp_dbd_r${radius}_gap${height}_p${power}.png"
        
        # Call the python script with the arguments
        python3 dbd_sim.py -r "$radius" -ht "$height" -p "$power" -o "$filename"
        
        # Append the filename to our list
        IMAGE_LIST="$IMAGE_LIST $filename"
    done
done

echo "Stitching all images into a single PNG..."

# Call the python script in stitch mode, passing all the generated files
python3 dbd_sim.py --stitch $IMAGE_LIST -o Final_DBD_Presentation_Grid.png

# Clean up the temporary individual images
rm -f temp_dbd_*.png

echo "Done! Open 'Final_DBD_Presentation_Grid.png' to see the results."
