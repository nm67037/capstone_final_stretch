import numpy as np
import matplotlib.pyplot as plt

def main():
    print("=== ICP Vacuum Chamber & Plasma Simulator ===")
    
    # Prompt user for inputs
    try:
        chamber_radius = float(input("Enter the chamber radius in cm (e.g., 5.0): "))
        chamber_height = float(input("Enter the chamber height in cm (e.g., 20.0): "))
    except ValueError:
        print("Invalid input. Defaulting to r=5.0, h=20.0")
        chamber_radius = 5.0
        chamber_height = 20.0

    # Dynamically scale coil parameters
    coil_radius = chamber_radius + 0.5
    coil_turns = max(3, int(chamber_height / 3))
    coil_start_z = chamber_height * 0.15
    coil_end_z = chamber_height * 0.85

    print(f"\nRendering chamber with Radius: {chamber_radius}cm, Height: {chamber_height}cm...")
    print("Calculating volumetric plasma density mapping...")

    # Set up the figure and 3D axis
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('white')

    # --- 1. Draw the Vacuum Chamber (Wireframe to see inside) ---
    z_cyl = np.linspace(0, chamber_height, 30)
    theta_cyl = np.linspace(0, 2 * np.pi, 30)
    theta_grid, z_grid = np.meshgrid(theta_cyl, z_cyl)
    x_cyl = chamber_radius * np.cos(theta_grid)
    y_cyl = chamber_radius * np.sin(theta_grid)

    ax.plot_surface(x_cyl, y_cyl, z_grid, alpha=0.05, color='gray', edgecolor='lightgray')

    # --- 2. Simulate Volumetric Plasma Density ---
    num_points = 8000
    
    r_pts = chamber_radius * np.sqrt(np.random.rand(num_points)) 
    theta_pts = np.random.rand(num_points) * 2 * np.pi
    z_pts = np.random.rand(num_points) * chamber_height

    x_pts = r_pts * np.cos(theta_pts)
    y_pts = r_pts * np.sin(theta_pts)

    r_norm = r_pts / chamber_radius
    z_norm = (z_pts - (chamber_height / 2)) / (chamber_height / 2)
    
    #mess with this line below:
    density = np.exp(-10.0 * r_norm**2 - 15.0 * z_norm**2) 

    mask = density > 0.05
    x_pts, y_pts, z_pts, density = x_pts[mask], y_pts[mask], z_pts[mask], density[mask]

    # --- THE FIX: Calculate RGBA colors manually to avoid the alpha array bug ---
    # Normalize density values between 0 and 1
    norm = plt.Normalize(vmin=density.min(), vmax=density.max())
    
    # Get the RGB base colors from the 'Blues' colormap
    rgba_colors = plt.cm.Blues(norm(density))
    
    # Modify the Alpha (transparency) channel (index 3) based on density
    rgba_colors[:, 3] = norm(density) * 0.7 

    # Plot the plasma using the custom RGBA array
    plasma_scatter = ax.scatter(x_pts, y_pts, z_pts, c=rgba_colors, s=25, edgecolors='none', label='Plasma')

    # Add a colorbar using a ScalarMappable since we passed raw colors to scatter
    sm = plt.cm.ScalarMappable(cmap='Blues', norm=norm)
    sm.set_array([]) 
    cbar = fig.colorbar(sm, ax=ax, pad=0.1, shrink=0.6)
    cbar.set_label('Relative Plasma Density', rotation=270, labelpad=15)

    # --- 3. Draw the RF Coil (Helix) ---
    t = np.linspace(0, coil_turns * 2 * np.pi, 1000)
    z_coil = np.linspace(coil_start_z, coil_end_z, 1000)
    x_coil = coil_radius * np.cos(t)
    y_coil = coil_radius * np.sin(t)
    ax.plot(x_coil, y_coil, z_coil, color='#b87333', linewidth=4, label='RF Induction Coil')

    # --- 4. Draw Top and Bottom Flanges ---
    theta_flange = np.linspace(0, 2 * np.pi, 50)
    x_flange = (chamber_radius + 1) * np.cos(theta_flange)
    y_flange = (chamber_radius + 1) * np.sin(theta_flange)
    ax.plot(x_flange, y_flange, np.zeros_like(x_flange), color='gray', linewidth=3)
    ax.plot(x_flange, y_flange, np.full_like(x_flange, chamber_height), color='gray', linewidth=3)

    # --- Formatting and Aesthetics ---
    ax.set_title(f'ICP Chamber with Plasma Density (r={chamber_radius}cm, h={chamber_height}cm)', fontsize=14, pad=20)
    ax.set_xlabel('X Axis (cm)')
    ax.set_ylabel('Y Axis (cm)')
    ax.set_zlabel('Z Axis (cm)')

    ax.set_box_aspect([1, 1, chamber_height/(2*chamber_radius)]) 

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    # Add this near the bottom of your script to lock the visual scale
    ax.set_xlim([-15, 15])
    ax.set_ylim([-15, 15])
    ax.set_zlim([0, 30])

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper right')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
