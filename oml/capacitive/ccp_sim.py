import numpy as np
import matplotlib.pyplot as plt
import argparse
import math
import matplotlib.image as mpimg

def render_ccp_chamber(chamber_radius, chamber_height, power_choice, out_filename):
    # Set diffusion parameters based on power choice for a CCP (flatter, parallel-plate plasma)
    if power_choice == 1:
        decay_r, decay_z = 5.0, 20.0
        power_label = "Low Power"
    elif power_choice == 3:
        decay_r, decay_z = 0.2, 1.5
        power_label = "High Power"
    else:
        decay_r, decay_z = 1.5, 6.0
        power_label = "Medium Power"

    # Define the Parallel Plate Electrodes
    electrode_radius = chamber_radius * 0.9 # Slightly smaller than the chamber walls
    bottom_electrode_z = chamber_height * 0.15
    top_electrode_z = chamber_height * 0.85

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('white')

    # --- 1. Draw the Chamber Walls ---
    z_cyl = np.linspace(0, chamber_height, 30)
    theta_cyl = np.linspace(0, 2 * np.pi, 30)
    theta_grid, z_grid = np.meshgrid(theta_cyl, z_cyl)
    x_cyl = chamber_radius * np.cos(theta_grid)
    y_cyl = chamber_radius * np.sin(theta_grid)
    ax.plot_surface(x_cyl, y_cyl, z_grid, alpha=0.05, color='gray', edgecolor='lightgray')

    # --- 2. Draw the Electrodes (Parallel Plates) ---
    r_elec = np.linspace(0, electrode_radius, 10)
    theta_elec = np.linspace(0, 2 * np.pi, 30)
    r_elec_grid, theta_elec_grid = np.meshgrid(r_elec, theta_elec)
    x_elec = r_elec_grid * np.cos(theta_elec_grid)
    y_elec = r_elec_grid * np.sin(theta_elec_grid)
    
    # Bottom Grounded Chuck
    ax.plot_surface(x_elec, y_elec, np.full_like(x_elec, bottom_electrode_z), 
                    color='silver', alpha=0.9, edgecolor='gray', label='Grounded Chuck')
    # Top Powered Electrode
    ax.plot_surface(x_elec, y_elec, np.full_like(x_elec, top_electrode_z), 
                    color='silver', alpha=0.9, edgecolor='gray', label='Powered Electrode')

    # --- 3. Simulate CCP Volumetric Plasma Density ---
    num_points = 8000
    
    # Gas generates mostly between the two electrodes
    r_pts = chamber_radius * np.sqrt(np.random.rand(num_points)) 
    theta_pts = np.random.rand(num_points) * 2 * np.pi
    
    # Confine random points strictly between the plates, with a little padding for the dark space (sheath)
    z_pts = np.random.uniform(bottom_electrode_z + 0.5, top_electrode_z - 0.5, num_points)

    x_pts = r_pts * np.cos(theta_pts)
    y_pts = r_pts * np.sin(theta_pts)

    # Normalize based on the gap between electrodes, not the whole chamber
    gap_center = (top_electrode_z + bottom_electrode_z) / 2.0
    gap_height = top_electrode_z - bottom_electrode_z
    
    r_norm = r_pts / electrode_radius
    z_norm = (z_pts - gap_center) / (gap_height / 2.0)
    
    density = np.exp(-decay_r * r_norm**2 - decay_z * z_norm**2) 
    mask = density > 0.05
    x_pts, y_pts, z_pts, density = x_pts[mask], y_pts[mask], z_pts[mask], density[mask]

    norm = plt.Normalize(vmin=0.0, vmax=1.0)
    # Using 'Purples' to differentiate CCP visually from the blue ICP in presentations
    rgba_colors = plt.cm.Purples(norm(density)) 
    rgba_colors[:, 3] = norm(density) * 0.7 

    ax.scatter(x_pts, y_pts, z_pts, c=rgba_colors, s=15, edgecolors='none', label='Plasma')

    # --- 4. Draw Flanges ---
    theta_flange = np.linspace(0, 2 * np.pi, 50)
    x_flange = (chamber_radius + 1) * np.cos(theta_flange)
    y_flange = (chamber_radius + 1) * np.sin(theta_flange)
    ax.plot(x_flange, y_flange, np.zeros_like(x_flange), color='dimgray', linewidth=2)
    ax.plot(x_flange, y_flange, np.full_like(x_flange, chamber_height), color='dimgray', linewidth=2)

    # --- 5. Formatting ---
    ax.set_title(f'CCP: r={chamber_radius}cm, h={chamber_height}cm ({power_label})', fontsize=12, pad=10)
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
    parser = argparse.ArgumentParser(description="CCP Vacuum Chamber Generator")
    parser.add_argument('-r', '--radius', type=float, help='Chamber radius (cm)')
    parser.add_argument('-ht', '--height', type=float, help='Chamber height (cm)')
    parser.add_argument('-p', '--power', type=int, choices=[1, 2, 3], help='Power level (1=Low, 2=Med, 3=High)')
    parser.add_argument('-o', '--out', type=str, help='Output filename')
    parser.add_argument('--stitch', nargs='+', help='List of images to stitch together')
    
    args = parser.parse_args()

    if args.stitch:
        stitch_images(args.stitch, args.out)
    elif args.radius and args.height and args.power and args.out:
        print(f"Generating CCP r={args.radius}, h={args.height}, Power={args.power} -> {args.out}")
        render_ccp_chamber(args.radius, args.height, args.power, args.out)
    else:
        print("Please provide --radius, --height, --power, and --out, OR provide --stitch [files].")
