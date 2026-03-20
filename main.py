import tkinter as tk
from tkinter import ttk, scrolledtext
import numpy as np
from datetime import datetime
import time
import sys


class TrailLogger:
    """Minimal logger to handle auto-numbering and formatting."""

    def __init__(self):
        self.steps = []
        self.step_num = 1

    def clear(self):
        self.steps = []
        self.step_num = 1

    def add_heading(self, heading):
        # Format the heading. Reset the counter if we hit the STEPS section.
        prefix = "\n" if heading != "GIVEN" else ""
        self.steps.append(f"{prefix}{heading}:")
        if heading == "STEPS":
            self.step_num = 1

    def add_step(self, text, is_substep=False):
        # Auto-number main steps, indent sub-steps
        if is_substep:
            self.steps.append(f"   {text}")
        else:
            self.steps.append(f"{self.step_num}. {text}")
            self.step_num += 1

    def add_info(self, text):
        # Regular text without numbering
        self.steps.append(text)

    def get_trail(self):
        return "\n".join(self.steps)


class NumericalDifferentiator:
    def __init__(self):
        self.logger = TrailLogger()

    def evaluate(self, x, expr):
        # Safely evaluate the mathematical expression
        allowed_names = {
            'x': x,
            'sin': np.sin, 'cos': np.cos, 'exp': np.exp,
            'log': np.log, 'sqrt': np.sqrt,
            'tan': np.tan
        }
        # Replace function names with numpy equivalents
        for func in ['sin', 'cos', 'exp', 'log', 'sqrt', 'tan']:
            expr = expr.replace(f'{func}(', f'np.{func}(')

        code = compile(expr, "<string>", "eval")
        for name in code.co_names:
            if name not in ['np'] and name not in allowed_names:
                raise NameError(f"Use of {name} not allowed")
        return eval(code, {"__builtins__": {}, "np": np}, allowed_names)

    def central_difference(self, f, x, h, tol=1e-6, max_iter=20):
        """Compute derivative iteratively using central difference method"""
        self.logger.clear()
        start_time = time.time()

        self.logger.add_heading("GIVEN")
        self.logger.add_info(f"Function f(x) = {f}")
        self.logger.add_info(f"Point x = {x}")
        self.logger.add_info(f"Initial Step size h = {h}")
        self.logger.add_info(f"Target Tolerance = {tol}")
        self.logger.add_info(f"Max Iterations = {max_iter}")

        self.logger.add_heading("METHOD")
        self.logger.add_info("Iterative Central Difference Approximation")
        self.logger.add_info("Halving step size until tolerance or max iterations reached.")

        self.logger.add_heading("STEPS")
        try:
            prev_deriv = None
            stop_reason = ""
            deriv = 0

            for i in range(1, int(max_iter) + 1):
                f_plus = self.evaluate(x + h, f)
                f_minus = self.evaluate(x - h, f)
                deriv = (f_plus - f_minus) / (2 * h)

                self.logger.add_step(f"Iteration {i} (h = {h}):")
                self.logger.add_step(f"f'({x}) ≈ {deriv:.8f}", is_substep=True)

                if prev_deriv is not None:
                    error = abs(deriv - prev_deriv)
                    self.logger.add_step(f"Error vs previous: {error:.2e}", is_substep=True)

                    if error <= tol:
                        self.logger.add_info(
                            f"\n[STOPPING RULE MET] Target tolerance ({tol}) reached at Iteration {i}.")
                        stop_reason = "Tolerance Met"
                        break
                    elif h < 1e-12:
                        self.logger.add_info(f"\n[STOPPING RULE MET] Machine precision limit reached (h too small).")
                        stop_reason = "Precision Limit"
                        break

                prev_deriv = deriv
                h = h / 2.0
            else:
                self.logger.add_info(f"\n[STOPPING RULE MET] Maximum iterations ({max_iter}) reached.")
                stop_reason = "Max Iterations"

            self.logger.add_heading("FINAL")
            self.logger.add_info(f"f'({x}) ≈ {deriv:.8f}")

            end_time = time.time()
            runtime = end_time - start_time
            self.logger.add_heading("SUMMARY")
            self.logger.add_info(f"Stop Reason: {stop_reason}")
            self.logger.add_info(f"Runtime: {runtime:.6f} seconds")
            self.logger.add_info(f"Python version: {sys.version.split()[0]}")
            self.logger.add_info(f"NumPy version: {np.__version__}")
            self.logger.add_info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            return deriv, self.logger.get_trail()

        except Exception as e:
            raise e  # Pass to UI for handling


class CalculatorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Numerical Differentiation Calculator")
        self.root.geometry("900x800")
        self.root.configure(bg="#f0f0f0")

        self.setup_styles()
        self.differentiator = NumericalDifferentiator()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), padding=10)
        style.configure("Input.TLabel", font=("Helvetica", 11), padding=5)
        style.configure("Hint.TLabel", font=("Helvetica", 10, "italic"), foreground="#666666")

        style.configure("Card.TLabelframe", background="#ffffff", borderwidth=2, relief="solid")
        style.configure("Card.TLabelframe.Label", font=("Helvetica", 12, "bold"),
                        background="#ffffff", foreground="#2c3e50")

        style.configure("Primary.TButton", font=("Helvetica", 11, "bold"), padding=10)
        style.configure("Secondary.TButton", font=("Helvetica", 10), padding=5)

    def insert_text(self, text):
        self.function_entry.insert(tk.INSERT, text)
        self.function_entry.focus()

    def setup_ui(self):
        title_label = ttk.Label(self.root, text="Numerical Differentiation Calculator",
                                style="Title.TLabel", background="#f0f0f0")
        title_label.pack(pady=(10, 5))

        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill="both", expand=True)

        input_frame = ttk.LabelFrame(main_container, text="Input Parameters",
                                     padding="20", style="Card.TLabelframe")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))

        function_container = ttk.Frame(input_frame)
        function_container.pack(fill="x", expand=True)

        function_input_frame = ttk.Frame(function_container)
        function_input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ttk.Label(function_input_frame, text="Function f(x)", style="Input.TLabel").pack(anchor="w")
        self.function_entry = ttk.Entry(function_input_frame, width=50, font=("Helvetica", 11))
        self.function_entry.pack(fill="x", pady=(0, 5))
        hint_label = ttk.Label(function_input_frame, text="Example: sin(x), x**2, exp(x)",
                               style="Hint.TLabel")
        hint_label.pack(anchor="w", pady=(0, 15))

        calc_frame = ttk.LabelFrame(function_container, text="Quick Functions", padding="10")
        calc_frame.pack(side="right", fill="y")

        buttons = [
            [('sin', 'sin(x)'), ('cos', 'cos(x)'), ('tan', 'tan(x)')],
            [('exp', 'exp(x)'), ('log', 'log(x)'), ('sqrt', 'sqrt(x)')],
            [('x²', 'x**2'), ('x³', 'x**3'), ('1/x', '1/x')],
            [('+', '+'), ('-', '-'), ('*', '*')],
            [('/', '/'), ('(', '('), (')', ')')]
        ]

        for row_idx, row in enumerate(buttons):
            button_frame = ttk.Frame(calc_frame)
            button_frame.pack(fill="x", pady=2)

            for label, value in row:
                btn = ttk.Button(button_frame, text=label,
                                 command=lambda v=value: self.insert_text(v),
                                 style="Secondary.TButton", width=8)
                btn.pack(side="left", padx=2)

        params_frame = ttk.Frame(input_frame)
        params_frame.pack(fill="x", pady=10)

        x_frame = ttk.Frame(params_frame)
        x_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Label(x_frame, text="x value", style="Input.TLabel").pack(anchor="w")
        self.x_entry = ttk.Entry(x_frame, width=15, font=("Helvetica", 11))
        self.x_entry.pack(fill="x")

        h_frame = ttk.Frame(params_frame)
        h_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Label(h_frame, text="Initial Step (h)", style="Input.TLabel").pack(anchor="w")
        self.h_entry = ttk.Entry(h_frame, width=15, font=("Helvetica", 11))
        self.h_entry.pack(fill="x")

        tol_frame = ttk.Frame(params_frame)
        tol_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Label(tol_frame, text="Tolerance", style="Input.TLabel").pack(anchor="w")
        self.tol_entry = ttk.Entry(tol_frame, width=15, font=("Helvetica", 11))
        self.tol_entry.insert(0, "1e-6")
        self.tol_entry.pack(fill="x")

        iter_frame = ttk.Frame(params_frame)
        iter_frame.pack(side="left", fill="x", expand=True)
        ttk.Label(iter_frame, text="Max Iters", style="Input.TLabel").pack(anchor="w")
        self.iter_entry = ttk.Entry(iter_frame, width=15, font=("Helvetica", 11))
        self.iter_entry.insert(0, "20")
        self.iter_entry.pack(fill="x")

        button_frame = ttk.Frame(input_frame)
        button_frame.pack(pady=(15, 0))

        calculate_btn = ttk.Button(button_frame, text="Compute", command=self.calculate,
                                   style="Primary.TButton")
        calculate_btn.pack(side="left", padx=5)

        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear,
                               style="Secondary.TButton")
        clear_btn.pack(side="left", padx=5)

        answer_frame = ttk.LabelFrame(main_container, text="Final Answer",
                                      padding="15", style="Card.TLabelframe")
        answer_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.final_answer_var = tk.StringVar()
        self.final_answer_var.set("Awaiting computation...")
        answer_label = ttk.Label(answer_frame, textvariable=self.final_answer_var,
                                 font=("Helvetica", 16, "bold"), foreground="#2980b9")
        answer_label.pack()

        result_frame = ttk.LabelFrame(main_container, text="Solution Trail",
                                      padding="15", style="Card.TLabelframe")
        result_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.result_text = scrolledtext.ScrolledText(
            result_frame, wrap=tk.WORD, height=15,
            font=("Consolas", 11), bg="#ffffff", fg="#2c3e50"
        )
        self.result_text.configure(state='disabled')
        self.result_text.pack(fill="both", expand=True)

    def calculate(self):
        self.result_text.configure(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.final_answer_var.set("Awaiting computation...")

        # --- WEEK 2 VALIDATION LOGIC ---
        self.result_text.insert(tk.END, "VALIDATION STATUS: ")
        f_str = self.function_entry.get().strip()
        x_str = self.x_entry.get().strip()
        h_str = self.h_entry.get().strip()
        tol_str = self.tol_entry.get().strip()
        iter_str = self.iter_entry.get().strip()

        try:
            # Rule 1: Required Fields
            if not f_str or not x_str or not h_str or not tol_str or not iter_str:
                raise ValueError("All fields (Function, x, h, Tolerance, Max Iters) must be filled.")

            # Rule 2: Type Checks
            try:
                x = float(x_str)
                h = float(h_str)
                tol = float(tol_str)
                max_iter = int(iter_str)
            except ValueError:
                raise ValueError("x, h, and Tolerance must be valid numbers. Max Iters must be a whole number.")

            # Rule 3: Range Check
            if h == 0:
                raise ValueError("Step size (h) cannot be exactly zero (division by zero error).")

            # If it gets here, validation passed
            self.result_text.insert(tk.END, "PASS ✓\n----------------------------------------\n\n")

            # Run computation
            derivative, steps = self.differentiator.central_difference(f_str, x, h, tol, max_iter)
            self.result_text.insert(tk.END, steps)
            self.final_answer_var.set(f"f'({x}) ≈ {derivative:.8f}")

        except Exception as e:
            # Catch Validation or Math Errors
            self.result_text.insert(tk.END,
                                    f"FAIL ✗\n\nERROR DETAIL:\n{str(e)}\n\nPlease correct the input and try again.")
            self.final_answer_var.set("Input Error")

        finally:
            self.result_text.configure(state='disabled')

    def clear(self):
        self.function_entry.delete(0, tk.END)
        self.x_entry.delete(0, tk.END)
        self.h_entry.delete(0, tk.END)
        self.tol_entry.delete(0, tk.END)
        self.tol_entry.insert(0, "1e-6")
        self.iter_entry.delete(0, tk.END)
        self.iter_entry.insert(0, "20")

        self.result_text.configure(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.configure(state='disabled')

        self.final_answer_var.set("Awaiting computation...")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = CalculatorApp()
    app.run()
