import numpy as np
import matplotlib.pyplot as plt

def find_optimal_configuration():
    print("Running optimization algorithm for maximum plasma concentration...")
    radii = [2.5, 5.0, 8.0, 10.0]  # cm
    gaps = [0.5, 1.0, 1.5, 2.0]    # cm
    powers = [1, 2, 3]             # 1=Low, 2=Med, 3=High (proxy for Watts)

    best_score = 0
    best_config = None

    for r in radii:
        for g in gaps:
            for p in powers:
                # Concentration Score ~ Power / Volume
                volume = np.pi * (r**2) * g
                # Give high power an exponential weight for plasma density
                score = (p**2) / volume 
                
                if score > best_score:
                    best_score = score
                    best_config = (r, g, p)

    opt_r, opt_g, opt_p = best_config
    print(f"Optimal Configuration Found!")
    print(f"Radius: {opt_r} cm | Gap: {opt_g} cm | Power Level: {opt_p}")
    return opt_r, opt_g, opt_p

def render_zoomed_dbd(chamber_radius, gap_height, power_choice, out_filename):
    # Set streamer count based on power
    num_streamers = 300 if power_choice == 3 else (80 if power_choice == 2 else 20)
    
    electrode_radius = chamber_radius * 0.9 
    dielectric_thickness = 0.5 # cm
    
    center_z = 0.0 # Centered at origin for easier zooming
    bottom_dielectric_z = center_z - (gap_height / 2.0)
    top_dielectric_z = center_z + (gap_height / 2.0)
    
    bottom_electrode_z = bottom_dielectric_z - dielectric_thickness
    top_electrode_z = top_dielectric_z + dielectric_thickness

    fig = plt.figure(figsize=(10, 8)) # Larger figure for poster quality
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('white')

    # --- 1. Draw Electrodes ---
    r_elec = np.linspace(0, electrode_radius, 15)
    theta_elec = np.linspace(0, 2 * np.pi, 40)
    r_elec_grid, theta_elec_grid = np.meshgrid(r_elec, theta_elec)
    x_elec = r_elec_grid * np.cos(theta_elec_grid)
    y_elec = r_elec_grid * np.sin(theta_elec_grid)
    
    ax.plot_surface(x_elec, y_elec, np.full_like(x_elec, bottom_electrode_z), 
                    color='silver', alpha=1.0, edgecolor='gray', label='Metal Electrode')
    ax.plot_surface(x_elec, y_elec, np.full_like(x_elec, top_electrode_z), 
                    color='silver', alpha=1.0, edgecolor='gray')

    # --- 2. Draw Dielectric Barriers ---
    ax.plot_surface(x_elec, y_elec, np.full_like(x_elec, bottom_dielectric_z), 
                    color='lightcyan', alpha=0.7, edgecolor='cadetblue', label='Dielectric Barrier')
    ax.plot_surface(x_elec, y_elec, np.full_like(x_elec, top_dielectric_z), 
                    color='lightcyan', alpha=0.7, edgecolor='cadetblue')

    # --- 3. Simulate High-Density DBD Streamers ---
    x_pts, y_pts, z_pts, density = [], [], [], []
    points_per_streamer = 30 # High point count for detailed rendering

    for _ in range(num_streamers):
        r = electrode_radius * 0.95 * np.sqrt(np.random.rand())
        theta = np.random.rand() * 2 * np.pi
        cx, cy = r * np.cos(theta), r * np.sin(theta)

        z_vals = np.linspace(bottom_dielectric_z, top_dielectric_z, points_per_streamer)
        x_vals = cx + np.random.normal(0, 0.02, points_per_streamer)
        y_vals = cy + np.random.normal(0, 0.02, points_per_streamer)
        d_vals = np.random.uniform(0.7, 1.0, points_per_streamer)

        x_pts.extend(x_vals)
        y_pts.extend(y_vals)
        z_pts.extend(z_vals)
        density.extend(d_vals)

    # --- THE FIX: Convert Python lists to NumPy arrays before math operations ---
    x_pts = np.array(x_pts)
    y_pts = np.array(y_pts)
    z_pts = np.array(z_pts)
    density = np.array(density)

    # Convert to arrays and plot
    norm = plt.Normalize(vmin=0.0, vmax=1.0)
    rgba_colors = plt.cm.autumn(norm(density)) # Intense gold/orange
    rgba_colors[:, 3] = density * 0.9 

    ax.scatter(x_pts, y_pts, z_pts, c=rgba_colors, s=15, edgecolors='none', label='Dense Plasma Core')

    # --- 4. Tightly Framed Formatting ---
    ax.set_title(f'Optimized DBD Generator (r={chamber_radius}cm, gap={gap_height}cm)', fontsize=16, pad=15)
    ax.set_xlabel('X (cm)')
    ax.set_ylabel('Y (cm)')
    ax.set_zlabel('Z (cm)')

    # DYNAMIC ZOOM: Lock the camera tightly around the generator bounds
    zoom_margin = 0.5
    ax.set_xlim([-(chamber_radius + zoom_margin), chamber_radius + zoom_margin])
    ax.set_ylim([-(chamber_radius + zoom_margin), chamber_radius + zoom_margin])
    
    # Z-axis zoom based strictly on electrode height
    z_bound = abs(top_electrode_z) + zoom_margin
    ax.set_zlim([-z_bound, z_bound])
    
    # Maintain physical aspect ratio even when zoomed
    ax.set_box_aspect([1, 1, (2*z_bound)/(2*(chamber_radius + zoom_margin))]) 

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper left', bbox_to_anchor=(1.05, 1))

    plt.tight_layout()
    plt.savefig(out_filename, dpi=300, bbox_inches='tight') # dpi=300 for poster quality
    print(f"\nSaved high-resolution poster image to: {out_filename}")
    plt.close()

if __name__ == "__main__":
    # 1. Run the algorithm
    opt_r, opt_g, opt_p = find_optimal_configuration()
    
    # 2. Render the winner
    output_file = "Poster_Optimized_DBD.png"
    render_zoomed_dbd(opt_r, opt_g, opt_p, output_file)
