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
