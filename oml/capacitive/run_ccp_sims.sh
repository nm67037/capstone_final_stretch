#!/bin/bash

# Array of Radii and Heights to test (Format: RADIUS_HEIGHT)
# Note: CCP chambers tend to favor wider, shorter geometries to accommodate large wafers
DIMENSIONS=("5.0_10.0" "8.0_10.0" "10.0_15.0")

# Array of Power Levels (1=Low, 2=Med, 3=High)
POWERS=(1 2 3)

# Clear out any old temporary images
rm -f temp_ccp_*.png

echo "Starting batch generation of CCP simulations..."

# Keep track of all generated image filenames
IMAGE_LIST=""

# Loop through all dimensions and powers
for dim in "${DIMENSIONS[@]}"; do
    # Split the dim string into radius and height
    IFS="_" read -r radius height <<< "$dim"
    
    for power in "${POWERS[@]}"; do
        filename="temp_ccp_r${radius}_h${height}_p${power}.png"
        
        # Call the python script with the arguments
        python3 ccp_sim.py -r "$radius" -ht "$height" -p "$power" -o "$filename"
        
        # Append the filename to our list
        IMAGE_LIST="$IMAGE_LIST $filename"
    done
done

echo "Stitching all images into a single PNG..."

# Call the python script in stitch mode, passing all the generated files
python3 ccp_sim.py --stitch $IMAGE_LIST -o Final_CCP_Presentation_Grid.png

# Clean up the temporary individual images
rm -f temp_ccp_*.png

echo "Done! Open 'Final_CCP_Presentation_Grid.png' to see the results."
