import numpy as np
from scipy.integrate import solve_ivp
import os
from pathlib import Path

mpl_config_dir = Path("build") / "matplotlib"
mpl_config_dir.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(mpl_config_dir))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- 1. Baseline Circuit Parameters ---
Vs_amp = 10.0      # Source voltage amplitude (V)
L0 = 0.1           # Nominal Inductance (H)
C = 10e-6          # Capacitance (F)
R0 = 50.0          # Nominal baseline resistance (Ohms)
w0 = 1 / np.sqrt(L0 * C) # Resonant frequency (rad/s)

# --- 2. Non-Linear Parameters ---
k_thermal = 8000.0 # Heating coefficient for R(i)
I_sat = 0.05       # Saturation current for L(i) in Amps

# --- 3. The Unified ODE System ---
# This function implements the baseline ideal step response and several
# phenomenological non-ideal variations (thermal resistor, saturating
# inductor, and resonant AC forcing) for comparison.
def unified_rlc(t, y, scenario):
    """
    y[0] is v_c (capacitor voltage)
    y[1] is dv_c/dt (rate of change of voltage)
    """
    v_c = y[0]
    dv_c_dt = y[1]
    current = C * dv_c_dt
    
    # Default components
    R_dynamic = R0
    L_dynamic = L0
    Vin = Vs_amp # Default step input
    
    # Apply scenario-specific physics
    if scenario == 'thermal':
        R_dynamic = R0 + k_thermal * (current**2)
    elif scenario == 'saturation':
        L_dynamic = L0 / (1 + (current / I_sat)**2)
    elif scenario == 'ac_input':
        Vin = Vs_amp * np.sin(w0 * t)
        
    # The first-order derivatives
    dy1_dt = dv_c_dt
    dy2_dt = (Vin - v_c - R_dynamic * current) / (L_dynamic * C)
    
    return [dy1_dt, dy2_dt]

# --- 4. Simulation Setup ---
y0 = [0.0, 0.0] # Initial conditions: uncharged, no current
t_span = (0.0, 0.04) # Simulate for 40 milliseconds
t_eval = np.linspace(t_span[0], t_span[1], 2000) # High resolution for smooth curves

# Scenarios to run. The ideal baseline is compared against three
# non-ideal variants to show how component stress and resonant forcing
# modify the same underlying circuit dynamics.
scenarios = {
    'ideal': 'Ideal Step Response (Baseline)',
    'thermal': f'Thermal Resistor (k={k_thermal:.0f} Ohm/A^2)',
    'saturation': f'Inductor Saturation (Isat={I_sat} A)',
    'ac_input': 'AC Input at Resonance'
}

results = {}

# Run the solver for each scenario
for key in scenarios.keys():
    # We use args=(key,) to pass the specific scenario string into our unified_rlc function
    sol = solve_ivp(unified_rlc, t_span, y0, t_eval=t_eval, args=(key,), method='RK45')
    results[key] = sol.y[0] # Store the capacitor voltage

# --- 5. Plotting the 2x2 Grid ---
fig, axs = plt.subplots(2, 2, figsize=(14, 8))
fig.suptitle('Advanced RLC Circuit Modeling: Non-Linear and AC Dynamics', fontsize=16)

# Helper function to plot each subplot
def format_subplot(ax, time, voltage, title, is_ac=False):
    ax.plot(time, voltage, color='red' if title != 'Ideal Step Response (Baseline)' else 'blue', linewidth=1.5)
    
    # Plot baseline ideal for comparison on the non-linear step plots
    if title not in ['Ideal Step Response (Baseline)', 'AC Input at Resonance']:
        ax.plot(time, results['ideal'], color='blue', linestyle='--', alpha=0.5, label='Ideal Baseline')
        ax.legend()

    if not is_ac:
        ax.axhline(Vs_amp, color='black', linewidth=0.8, linestyle=':')
        
    ax.set_title(title)
    ax.set_ylabel('Capacitor Voltage (V)')
    ax.set_xlabel('Time (s)')
    ax.grid(True)
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# Plot Ideal
format_subplot(axs[0, 0], t_eval, results['ideal'], scenarios['ideal'])

# Plot Thermal
format_subplot(axs[0, 1], t_eval, results['thermal'], scenarios['thermal'])

# Plot Saturation
format_subplot(axs[1, 0], t_eval, results['saturation'], scenarios['saturation'])

# Plot AC Input
format_subplot(axs[1, 1], t_eval, results['ac_input'], scenarios['ac_input'], is_ac=True)

plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout so title fits

output_dir = Path("figures")
output_dir.mkdir(exist_ok=True)
fig.savefig(output_dir / "nonideal_rlc_simulation.pdf", bbox_inches="tight")
fig.savefig(output_dir / "nonideal_rlc_simulation.png", dpi=200, bbox_inches="tight")
print("Saved figures/nonideal_rlc_simulation.pdf and figures/nonideal_rlc_simulation.png")
