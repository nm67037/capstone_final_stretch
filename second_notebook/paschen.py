import numpy as np
import matplotlib.pyplot as plt

def calculate_paschen(pd, A, B, gamma):
    """
    Calculates breakdown voltage using Paschen's Law.
    V_b = (B * pd) / (ln(A * pd) - ln(ln(1 + 1/gamma)))
    """
    # Protect against math errors (log of negative/zero)
    valid_pd = pd > (np.exp(np.log(np.log(1 + 1/gamma))) / A)
    
    V_b = np.full_like(pd, np.nan) # Fill with NaNs by default
    
    pd_valid = pd[valid_pd]
    numerator = B * pd_valid
    denominator = np.log(A * pd_valid) - np.log(np.log(1 + 1/gamma))
    
    V_b[valid_pd] = numerator / denominator
    return V_b

def main():
    print("Generating Paschen's Law swoosh for the notebook...")

    # Define a range for Pressure * Distance (pd) in Torr-cm
    # Use a logarithmic space to capture the swoosh nicely
    pd = np.logspace(-1, 3, 500) 

    # Empirical constants for different gases [A, B, gamma]
    # A (cm^-1 Torr^-1), B (V cm^-1 Torr^-1), gamma (secondary electron emission)
    gases = {
        'Air': [15.0, 365.0, 0.01, 'blue'],
        'Argon': [11.5, 176.0, 0.01, 'red'],
        'Helium': [2.8, 34.0, 0.01, 'green']
    }

    plt.figure(figsize=(9, 6))

    # Plot the swoosh for each gas
    for name, params in gases.items():
        A, B, gamma, color = params
        V = calculate_paschen(pd, A, B, gamma)
        plt.loglog(pd, V, label=name, color=color, linewidth=2)

    # --- Plot your specific DBD Prototype ---
    # Pressure = 1 atm (760 Torr)
    # Gap = 0.5 cm
    dbd_pressure = 760 
    dbd_gap = 0.5
    dbd_pd = dbd_pressure * dbd_gap # 380 Torr-cm

    # Calculate exact voltage required for Air at that gap
    dbd_voltage = calculate_paschen(np.array([dbd_pd]), gases['Air'][0], gases['Air'][1], gases['Air'][2])[0]

    # Put a massive dot where your prototype is on the graph
    plt.plot(dbd_pd, dbd_voltage, 'ko', markersize=10, label=f'DBD Prototype\n(0.5cm Gap in Air)')
    
    # Add a dashed line dropping down to the axes to make it look professional
    plt.vlines(dbd_pd, ymin=100, ymax=dbd_voltage, colors='k', linestyles='dashed', alpha=0.5)
    plt.hlines(dbd_voltage, xmin=0.1, xmax=dbd_pd, colors='k', linestyles='dashed', alpha=0.5)

    # Formatting for the notebook
    plt.title("Paschen's Law: Breakdown Voltage vs. Pressure $\\times$ Distance", fontsize=14, pad=15)
    plt.xlabel("Pressure $\\times$ Distance ($p \\cdot d$) [Torr$\\cdot$cm]", fontsize=12)
    plt.ylabel("Breakdown Voltage ($V_b$) [Volts]", fontsize=12)
    
    # Set axis limits to make the swoosh look good
    plt.xlim(0.1, 1000)
    plt.ylim(100, 30000)

    plt.grid(True, which="both", ls="--", alpha=0.3)
    plt.legend(loc='upper left', fontsize=11)
    
    # Text box with the math result for easy copying into your notebook text
    result_text = f"Required Ignition Voltage:\n~ {int(dbd_voltage):,} Volts"
    plt.text(10, 500, result_text, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

    plt.tight_layout()
    out_file = "Paschen_Curve_Notebook.png"
    plt.savefig(out_file, dpi=200)
    print(f"Done! Saved to {out_file}")
    
    # Print the exact voltage to the terminal so you have it
    print(f"\n--- Notebook Data ---")
    print(f"DBD Gap: 0.5 cm")
    print(f"Operating Pressure: 760 Torr (1 atm)")
    print(f"Calculated pd: {dbd_pd} Torr-cm")
    print(f"Required Voltage to Ignite: {int(dbd_voltage):,} Volts")

if __name__ == "__main__":
    main()
