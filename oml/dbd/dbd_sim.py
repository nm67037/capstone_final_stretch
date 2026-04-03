import numpy as np
import matplotlib.pyplot as plt
import argparse
import math
import matplotlib.image as mpimg

def render_dbd_chamber(chamber_radius, gap_height, power_choice, out_filename):
    # Determine the number of micro-discharges (streamers) based on power
    if power_choice == 1:
        num_streamers = 20
        power_label = "Low Power"
    elif power_choice == 3:
        num_streamers = 300
        power_label = "High Power"
    else:
        num_streamers = 80
        power_label = "Medium Power"

    # Define the Geometry
    electrode_radius = chamber_radius * 0.9 
    dielectric_thickness = 1.0 # 1cm thick glass barriers
    
    # Calculate Z-positions
    center_z = 15.0 # Center the gap in the middle of our 30cm viewing window
    bottom_dielectric_z = center_z - (gap_height / 2.0)
    top_dielectric_z = center_z + (gap_height / 2.0)
    
    bottom_electrode_z = bottom_dielectric_z - dielectric_thickness
    top_electrode_z = top_dielectric_z + dielectric_thickness

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('white')

    # --- 1. Draw the Electrodes (Metal) ---
    r_elec = np.linspace(0, electrode_radius, 10)
    theta_elec = np.linspace(0, 2 * np.pi, 30)
    r_elec_grid, theta_elec_grid = np.meshgrid(r_elec, theta_elec)
    x_elec = r_elec_grid * np.cos(theta_elec_grid)
    y_elec = r_elec_grid * np.sin(theta_elec_grid)
    
    ax.plot_surface(x_elec, y_elec, np.full_like(x_elec, bottom_electrode_z), 
                    color='silver', alpha=1.0, label='Metal Electrode')
    ax.plot_surface(x_elec, y_elec, np.full_like(x_elec, top_electrode_z), 
                    color='silver', alpha=1.0)

    # --- 2. Draw the Dielectric Barriers (Glass/Quartz) ---
    ax.plot_surface(x_elec, y_elec, np.full_like(x_elec, bottom_dielectric_z), 
                    color='lightcyan', alpha=0.6, edgecolor='cadetblue', label='Dielectric Barrier')
    ax.plot_surface(x_elec, y_elec, np.full_like(x_elec, top_dielectric_z), 
                    color='lightcyan', alpha=0.6, edgecolor='cadetblue')

    # --- 3. Simulate DBD Micro-Discharge Streamers ---
    x_pts, y_pts, z_pts, density = [], [], [], []
    points_per_streamer = max(10, int(gap_height * 10)) # Scale points with gap size

    for _ in range(num_streamers):
        # Pick a random spot for the streamer to strike
        r = electrode_radius * 0.95 * np.sqrt(np.random.rand())
        theta = np.random.rand() * 2 * np.pi
        cx = r * np.cos(theta)
        cy = r * np.sin(theta)

        # Generate a vertical pillar of points (the lightning bolt)
        z_vals = np.linspace(bottom_dielectric_z, top_dielectric_z, points_per_streamer)
        
        # Add a tiny bit of horizontal jitter so they look like fuzzy electrical arcs
        x_vals = cx + np.random.normal(0, 0.05, points_per_streamer)
        y_vals = cy + np.random.normal(0, 0.05, points_per_streamer)
        
        # Make the core of the streamer hotter (denser) than the edges
        d_vals = np.random.uniform(0.6, 1.0, points_per_streamer)

        x_pts.extend(x_vals)
        y_pts.extend(y_vals)
        z_pts.extend(z_vals)
        density.extend(d_vals)

    x_pts, y_pts, z_pts, density = np.array(x_pts), np.array(y_pts), np.array(z_pts), np.array(density)

    # Color map for the hot filamentary streamers
    norm = plt.Normalize(vmin=0.0, vmax=1.0)
    rgba_colors = plt.cm.autumn(norm(density)) # Yellow/Orange/Red theme
    rgba_colors[:, 3] = density * 0.8 # Transparency based on density

    if num_streamers > 0:
        ax.scatter(x_pts, y_pts, z_pts, c=rgba_colors, s=10, edgecolors='none', label='Micro-Discharges')

    # --- 4. Formatting ---
    ax.set_title(f'DBD: r={chamber_radius}cm, gap={gap_height}cm ({power_label})', fontsize=12, pad=10)
    ax.set_xlabel('X (cm)')
    ax.set_ylabel('Y (cm)')
    ax.set_zlabel('Z (cm)')

    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([0, 30])
    ax.set_box_aspect([1, 1, 30/(2*10)]) 

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    # Filter legend
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper right', fontsize='small')

    plt.tight_layout()
    plt.savefig(out_filename, dpi=150, bbox_inches='tight')
    plt.close(fig) 

def stitch_images(image_files, out_filename):
    n = len(image_files)
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 6, rows * 6))
    axes = axes.flatten() if n > 1 else [axes]

    for i, ax in enumerate(axes):
        if i < n:
            img = mpimg.imread(image_files[i])
            ax.imshow(img)
        ax.axis('off')

    plt.tight_layout()
    plt.savefig(out_filename, dpi=200, bbox_inches='tight', facecolor='white')
    print(f"\nSuccessfully generated master image: {out_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DBD Vacuum Chamber Generator")
    parser.add_argument('-r', '--radius', type=float, help='Electrode radius (cm)')
    parser.add_argument('-ht', '--height', type=float, help='Dielectric Gap distance (cm)')
    parser.add_argument('-p', '--power', type=int, choices=[1, 2, 3], help='Power level (1=Low, 2=Med, 3=High)')
    parser.add_argument('-o', '--out', type=str, help='Output filename')
    parser.add_argument('--stitch', nargs='+', help='List of images to stitch together')
    
    args = parser.parse_args()

    if args.stitch:
        stitch_images(args.stitch, args.out)
    elif args.radius and args.height and args.power and args.out:
        print(f"Generating DBD r={args.radius}, gap={args.height}, Power={args.power} -> {args.out}")
        render_dbd_chamber(args.radius, args.height, args.power, args.out)
    else:
        print("Please provide --radius, --height, --power, and --out, OR provide --stitch [files].")
