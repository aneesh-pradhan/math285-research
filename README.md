# math285-research

Research project conducted under Prof. Santiago at CSU East Bay for MATH 285 as part of a UHP contract.

## Project Overview

This project investigates series RLC circuits through the lens of ordinary differential equations (ODEs), focusing on how resistance influences damping and stability. The analysis derives and solves first-order ODEs for RC and RL sub-circuits, as well as the second-order ODE for the full RLC system. The ideal analytic solutions are extended with numerical simulations incorporating phenomenological non-ideal behaviors like current-dependent resistor heating and inductor saturation.

### Research Question

How do resistors influence the damping and stability of series RLC circuits as described by ODEs, and what are the practical implications for engineering applications such as filters and oscillators?

### Key Findings

- Resistance governs whether the circuit is overdamped, critically damped, or underdamped.
- Non-ideal components can suppress, shift, or amplify transient oscillations compared to ideal models.
- Practical applications include bandpass filters, resonant oscillators, and impedance-matching networks.

## Repository Structure

- `main.tex`: Main LaTeX document compiling the research paper.
- `content/`: LaTeX source files for each section (introduction, system model, analytical methods, results, non-ideal simulation, discussion, conclusion).
- `bibliography/refs.bib`: Bibliography references.
- `simulate_rlc.py`: Python script for numerical simulation of non-ideal RLC circuits.
- `figures/`: Generated figures and plots.
- `Makefile`: Build automation for the LaTeX document.
- `requirements.txt`: Python dependencies for simulations.
- `build/`: Directory for LaTeX build artifacts (ignored by git).
- `styles/`: LaTeX style files.
- `include/`: Additional LaTeX includes.

## Installation and Setup

### Prerequisites

- Python 3.14 or later
- LaTeX distribution (e.g., TeX Live)
- `latexmk` for automated LaTeX builds

### Python Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

Dependencies include:
- `numpy`: Numerical computations
- `scipy`: ODE integration (solve_ivp)
- `matplotlib`: Plotting and figure generation

### LaTeX Setup

Ensure `latexmk` and a LaTeX distribution are installed. On Ubuntu/Debian:

```bash
sudo apt-get install texlive-latex-extra latexmk
```

## Usage

### Building the Paper

Compile the LaTeX document to PDF:

```bash
make all
```

This generates `build/main.pdf`.

For continuous compilation during editing:

```bash
make watch
```

To open the PDF after building:

```bash
make open
```

### Running Simulations

Execute the numerical simulation script:

```bash
python3 simulate_rlc.py
```

This generates figures in `figures/nonideal_rlc_simulation.pdf` and `figures/nonideal_rlc_simulation.png`, comparing ideal and non-ideal RLC responses.

### Word Count

Count words in the LaTeX content:

```bash
make wc
```

### Cleaning Build Artifacts

Remove build files:

```bash
make clean
```

## Methodology

1. **System Modeling**: Derive ODEs from Kirchhoff's Voltage Law for RC, RL, and RLC circuits.
2. **Analytic Solutions**: Solve ODEs for step responses, identifying damping regimes.
3. **Numerical Simulation**: Use SciPy's `solve_ivp` with RK45 method to simulate non-ideal behaviors.
4. **Visualization**: Generate plots using Matplotlib for comparison.

## References

- Nilsson, J. W., & Riedel, S. A. (2019). *Electric Circuits* (12th ed.). Pearson.
- Hayt, W. H., Kemmerly, J. E., & Durbin, S. M. (2018). *Engineering Circuit Analysis* (9th ed.). McGraw-Hill.
- Other references in `bibliography/refs.bib`.

## Contributing

This is an academic research project. For questions or suggestions, contact the author or Prof. Santiago.

## License

See `LICENSE` file.
