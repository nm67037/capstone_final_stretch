#!/bin/bash

# Array of Radii and Heights to test (Format: RADIUS_HEIGHT)
DIMENSIONS=("2.5_10.0" "5.0_20.0" "8.0_15.0")

# Array of Power Levels (1=Low, 2=Med, 3=High)
POWERS=(1 2 3)

# Clear out any old temporary images
rm -f temp_sim_*.png

echo "Starting batch generation of plasma simulations..."

# Keep track of all generated image filenames
IMAGE_LIST=""

# Loop through all dimensions and powers
for dim in "${DIMENSIONS[@]}"; do
    # Split the dim string into radius and height
    IFS="_" read -r radius height <<< "$dim"
    
    for power in "${POWERS[@]}"; do
        filename="temp_sim_r${radius}_h${height}_p${power}.png"
        
        # Call the python script with the arguments
        python3 icp_sim.py -r "$radius" -ht "$height" -p "$power" -o "$filename"
        
        # Append the filename to our list
        IMAGE_LIST="$IMAGE_LIST $filename"
    done
done

echo "Stitching all images into a single PNG..."

# Call the python script in stitch mode, passing all the generated files
python3 icp_sim.py --stitch $IMAGE_LIST -o Final_Presentation_Grid.png

# Clean up the temporary individual images
rm -f temp_sim_*.png

echo "Done! Open 'Final_Presentation_Grid.png' to see the results."
