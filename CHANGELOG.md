Project Changelog

Numerical Differentiation Calculator

$$1.3.0$$

 - Week 5

Focus: Iterative Completion & Stopping Rules

Iterative Step Halving: Replaced single-run differentiation with an iterative loop that halves the step size (h) each iteration to hone in on the exact derivative.

Dynamic Stopping Rules: Implemented Target Tolerance (stops when error between iterations is small enough) and Max Iterations (stops to prevent infinite loops).

Machine Precision Failsafe: Added a catch for when h becomes smaller than 1e-12 to stop computations before hitting Python floating-point precision loss limits.

UI Additions: Integrated editable fields for Tolerance and Max Iterations directly into the Tkinter window for full user control.

$$1.2.0$$

 - Week 4

Focus: Working Solver Output (Minimum Working Version)

End-to-End Solver Verification: Successfully implemented and verified the central difference engine for polynomial, trigonometric, and exponential functions.

Mathematical Accuracy Validation: Documented and validated expected analytical derivatives against actual numerical outputs (e.g., f'(x) of sin(x) at 0.785398).

Computation Transparency: Verified the TrailLogger accurately displays real computation steps, including f(x+h) and f(x-h) evaluations, rather than just the final answer.

Truncation Error Analysis: Identified and documented the inherent minor residuals (e.g., in exponential functions) that occur due to the nature of numerical approximations.

$$1.1.5$$

 - Week 3

Focus: UI/UX Enhancements & Advanced Trail Logging

Dedicated TrailLogger Class: Refactored the internal step-tracking logic into a separate TrailLogger class to automatically handle step numbering, indentation, and clean formatting.

Enlarge Log Feature: Added a "⛶ Enlarge Log" button to the UI that pops out the solution trail into a dedicated, resizable window for better readability of long computations.

Auto-Scrolling: Implemented automatic scrolling (see(tk.END)) to ensure the latest computation steps and final answers are always instantly visible to the user.

$$1.1.0$$

 - Week 2

Focus: Input Validation & Error Handling

Added Validation Layer: Implemented a pre-computation check to verify all input fields before the mathematical engine runs.

New "Validation Status" Log: The Solution Trail now explicitly starts with a "PASS" or "FAIL" status to fulfill auditing requirements.

Error Messaging: Created user-friendly error details for common issues such as non-numeric inputs for x and h.

Division-by-Zero Protection: Added a specific check to prevent a crash if the step size (h) is set to zero.

Empty Field Detection: The app now detects if the user attempts to compute without filling in the function, x value, or step size.

$$1.0.0$$

 - Week 1

Focus: UI Skeleton & Core Engine

Initial UI Build: Developed the main application window using Tkinter with a clean, modern layout.

Numerical Engine: Integrated the Central Difference Method formula for calculating derivatives.

Quick Functions Pad: Added a button grid for easy entry of common functions like sin, cos, exp, and log.

Solution Trail Panel: Created the scrollable text area to display the "Given," "Method," and "Steps" of the calculation.

Final Answer Display: Implemented a dedicated highlighted area for the final numerical result.

Repo Initialization: Hosted the source code on GitHub for version control and group collaboration.

Key Validation Rules Implemented

Required Fields: Function f(x), x value, and Step size (h) cannot be empty.

Type Checks: Numerical inputs must be floating-point numbers.

Range Checks: Step size (h) must not be zero to avoid division errors.

Syntax Checks: Function strings must utilize restricted, safe mathematical terms (e.g., np.sin, exp).
