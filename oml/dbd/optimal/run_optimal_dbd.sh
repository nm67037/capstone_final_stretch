#!/bin/bash

echo "Initiating DBD Optimization Sequence..."

# Clean up any old poster files
rm -f Poster_Optimized_DBD.png

# Run the python script (which runs the algorithm and generates the image)
python3 optimal_dbd.py

echo "Process Complete! Your poster image is ready."
