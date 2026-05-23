Project Changelog

Numerical Differentiation Calculator

$$0.9.0$$

  - Week 9
    
Focus: Verification Output (Auditing Requirement)

Verification auditing: Added a formal block in the solution trail that performs a dual-verify check.

Iterative Consistency Check: Compares the final result to the previous iteration's step-halving value.

Taylor Expansion Back-check: Verifies the derivative by substituting it back into the local linear approximation formula.

Summary Data: Enhanced the summary output to include total iteration counts for better auditing transparency.

$$0.8.0$$

  - Week 8
    
Focus: Robustness Output (Edge Cases)

Error Handling: Implemented explicit checks for Mathematical Domain Errors (e.g. sqrt of negative numbers).

Input Validation: Added range checks for solver configurations to prevent nonsensical inputs like negative iterations.

NumPy Failsafe: Implemented np.seterr(all='raise') to ensure mathematical impossibilities trigger clean UI warnings instead of silent NaNs.

$$0.7.0$$

  - Week 7
    
Focus: Midterm Documentation Output

About and Help Section: Added the About and Help Section to the System

Documentation: Added Github Documentation 


$$0.6.0$$

  - Week 6
    
Focus: Feature Expansion & Method Selection

Algorithm Expansion: Added Forward Difference and Backward Difference formulas to run alongside the original Central Difference method.

Dynamic Method Routing: Refactored the core calculation engine to dynamically apply the correct mathematical formula based on the user's choice.

UI Additions: Integrated new dropdown menus directly into the Tkinter window, allowing users to select their desired differentiation method and load pre-configured test scenarios.

Test Case Integration: Built an automated test loader containing 5 distinct test cases that instantly populates the inputs to streamline verification.


$$0.5.0$$

 - Week 5

Focus: Iterative Completion & Stopping Rules

Iterative Step Halving: Replaced single-run differentiation with an iterative loop that halves the step size (h) each iteration to hone in on the exact derivative.

Dynamic Stopping Rules: Implemented Target Tolerance (stops when error between iterations is small enough) and Max Iterations (stops to prevent infinite loops).

Machine Precision Failsafe: Added a catch for when h becomes smaller than 1e-12 to stop computations before hitting Python floating-point precision loss limits.

UI Additions: Integrated editable fields for Tolerance and Max Iterations directly into the Tkinter window for full user control.

$$0.4.0$$

 - Week 4

Focus: Working Solver Output (Minimum Working Version)

End-to-End Solver Verification: Successfully implemented and verified the central difference engine for polynomial, trigonometric, and exponential functions.

Mathematical Accuracy Validation: Documented and validated expected analytical derivatives against actual numerical outputs (e.g., f'(x) of sin(x) at 0.785398).

Computation Transparency: Verified the TrailLogger accurately displays real computation steps, including f(x+h) and f(x-h) evaluations, rather than just the final answer.

Truncation Error Analysis: Identified and documented the inherent minor residuals (e.g., in exponential functions) that occur due to the nature of numerical approximations.

$$0.3.0$$

 - Week 3

Focus: UI/UX Enhancements & Advanced Trail Logging

Dedicated TrailLogger Class: Refactored the internal step-tracking logic into a separate TrailLogger class to automatically handle step numbering, indentation, and clean formatting.

Enlarge Log Feature: Added a "⛶ Enlarge Log" button to the UI that pops out the solution trail into a dedicated, resizable window for better readability of long computations.

Auto-Scrolling: Implemented automatic scrolling (see(tk.END)) to ensure the latest computation steps and final answers are always instantly visible to the user.

$$0.2.0$$

 - Week 2

Focus: Input Validation & Error Handling

Added Validation Layer: Implemented a pre-computation check to verify all input fields before the mathematical engine runs.

New "Validation Status" Log: The Solution Trail now explicitly starts with a "PASS" or "FAIL" status to fulfill auditing requirements.

Error Messaging: Created user-friendly error details for common issues such as non-numeric inputs for x and h.

Division-by-Zero Protection: Added a specific check to prevent a crash if the step size (h) is set to zero.

Empty Field Detection: The app now detects if the user attempts to compute without filling in the function, x value, or step size.

$$0.1.0$$

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
