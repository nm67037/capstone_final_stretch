import numpy as np
import matplotlib.pyplot as plt

# Set up the figure and 3D axis
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('white')

# --- Parameters ---
chamber_radius = 5.0
chamber_height = 20.0
coil_radius = 5.5      # Slightly wider than the chamber
coil_turns = 6
coil_start_z = 3.0
coil_end_z = 17.0

# --- 1. Draw the Vacuum Chamber (Cylinder) ---
# Generate the mesh for the cylinder
z_cyl = np.linspace(0, chamber_height, 50)
theta_cyl = np.linspace(0, 2 * np.pi, 50)
theta_grid, z_grid = np.meshgrid(theta_cyl, z_cyl)

x_cyl = chamber_radius * np.cos(theta_grid)
y_cyl = chamber_radius * np.sin(theta_grid)

# Plot the cylindrical chamber (translucent blue to look like glass/quartz)
ax.plot_surface(x_cyl, y_cyl, z_grid, alpha=0.2, color='deepskyblue', 
                edgecolor='none', rstride=5, cstride=5)

# --- 2. Draw the RF Coil (Helix) ---
# Generate the parametric coordinates for the coil
t = np.linspace(0, coil_turns * 2 * np.pi, 1000)
z_coil = np.linspace(coil_start_z, coil_end_z, 1000)
x_coil = coil_radius * np.cos(t)
y_coil = coil_radius * np.sin(t)

# Plot the coil (copper color, thick line)
ax.plot(x_coil, y_coil, z_coil, color='#b87333', linewidth=5, label='RF Induction Coil')

# --- 3. Draw Top and Bottom Flanges (Optional detailing) ---
theta_flange = np.linspace(0, 2 * np.pi, 50)
x_flange = (chamber_radius + 1) * np.cos(theta_flange)
y_flange = (chamber_radius + 1) * np.sin(theta_flange)
ax.plot(x_flange, y_flange, np.zeros_like(x_flange), color='gray', linewidth=3, label='Base Flange')
ax.plot(x_flange, y_flange, np.full_like(x_flange, chamber_height), color='gray', linewidth=3)

# --- Formatting and Aesthetics ---
ax.set_title('Inductively Coupled Plasma (ICP) Chamber Concept', fontsize=14, pad=20)
ax.set_xlabel('X Axis (cm)')
ax.set_ylabel('Y Axis (cm)')
ax.set_zlabel('Z Axis (cm)')

# Set equal aspect ratio for realistic proportions
ax.set_box_aspect([1, 1, chamber_height/(2*chamber_radius)]) 

# Remove background grid panes for a cleaner look
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

ax.legend(loc='upper right')

plt.tight_layout()
plt.show()
