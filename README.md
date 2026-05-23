# Numerical Differentiation Calculator v1.0

A modern, comprehensive desktop application for calculating numerical derivatives using finite difference methods. Developed as a final project for Week 13.

## Created By
- Fidelson, John Paul M.
- Escauriaga, Kyle Andrei
- Dagdag, Emanuel Lloyd

## Features
- **Multiple Methods:** Calculate derivatives using Central, Forward, and Backward difference methods.
- **Iterative Refinement:** Automatically halves step size (h) until a target tolerance is met or max iterations are reached.
- **Auditing & Verification:** Dual-verify check utilizing Taylor Expansion and step-halving consistency to guarantee accuracy.
- **Export Capabilities:** Export detailed computation trails (TXT) for academic documentation and audits.
- **Modern UI:** Responsive, dark-themed scientific calculator interface with grid alignment, quick-function pads, and a pop-out log viewer.

## Limitations
- Highly complex or composite functions may require extensive iterations, leading to standard Python floating-point imprecision.
- The mathematical domain is restricted by standard constraints (e.g., calculating `sqrt(x)` at negative `x` values will raise a domain error).
- Designed strictly for scalar inputs (single real numbers), not matrices or multi-variable vectors.

## Requirements
- Python 3.7+
- `numpy`
- `tkinter` (Standard Python GUI library)

## Installation & Setup
1. Clone this repository or download the source code.
2. Open a terminal or command prompt in the project directory.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
4. Run the application:
   ```bash
   python main.py

## Usage 

- Load a Preset (Optional): Use the "Load Test Case" dropdown to populate known values for quick testing.
- Enter Parameters: - Function f(x): Enter a valid mathematical expression (e.g., sin(x), x2, exp(x)). Use the Quick Functions pad to easily build the formula.
- Method: Choose between Central, Forward, or Backward difference.
- x value: The mathematical point at which to evaluate the derivative.
- Initial Step (h): The starting step size (e.g., 0.1).
- Tolerance & Max Iters: Set stopping conditions for the iterative loop.
- Compute: Click Compute Result. The final numerical answer will display in the bottom left, and the step-by-step auditing trail will generate in the text box.
- Review & Export: Click Expand Log for an enlarged view, or click Export Report to save the entire computation trail to a local .txt file for documentation.
