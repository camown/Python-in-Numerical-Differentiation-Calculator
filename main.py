import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import numpy as np
from datetime import datetime
import time
import sys


class TrailLogger:
    """Refactored logger to handle crisp formatting and auto-numbering."""

    def __init__(self):
        self.steps = []
        self.step_num = 1

    def clear(self):
        self.steps = []
        self.step_num = 1

    def add_heading(self, heading):
        # Format with clear block dividers for readability
        prefix = "\n\n" if self.steps else ""
        self.steps.append(f"{prefix}=== {heading.upper()} ===")
        if heading == "STEPS":
            self.step_num = 1

    def add_step(self, text, is_substep=False):
        # Auto-number main steps, use arrow indentation for sub-steps
        if is_substep:
            self.steps.append(f"    ↳ {text}")
        else:
            self.steps.append(f" {self.step_num}. {text}")
            self.step_num += 1

    def add_info(self, text):
        # Indented regular text for clean block structure
        self.steps.append(f"  {text}")

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

    def compute_derivative(self, method, f, x, h, tol=1e-6, max_iter=20):
        """Compute derivative iteratively using the selected method"""
        self.logger.clear()
        start_time = time.time()

        # LOG THE GIVEN PARAMETERS
        self.logger.add_heading("GIVEN")
        self.logger.add_info(f"Function f(x)    = {f}")
        self.logger.add_info(f"Point x          = {x}")
        self.logger.add_info(f"Initial Step (h) = {h}")
        self.logger.add_info(f"Method           = {method}")
        self.logger.add_info(f"Target Tolerance = {tol}")
        self.logger.add_info(f"Max Iterations   = {max_iter}")

        self.logger.add_heading("METHOD")
        self.logger.add_info(f"Iterative {method} Approximation.")
        self.logger.add_info("Halving step size (h/2) until tolerance or max iterations reached.")

        self.logger.add_heading("STEPS")
        try:
            prev_deriv = None
            stop_reason = ""
            deriv = 0

            for i in range(1, int(max_iter) + 1):
                # Calculate necessary function points based on the method
                f_x = self.evaluate(x, f)
                f_plus = self.evaluate(x + h, f)
                f_minus = self.evaluate(x - h, f)

                # Route to the correct formula based on UI selection
                if method == "Central Difference":
                    deriv = (f_plus - f_minus) / (2 * h)
                elif method == "Forward Difference":
                    deriv = (f_plus - f_x) / h
                elif method == "Backward Difference":
                    deriv = (f_x - f_minus) / h
                else:
                    raise ValueError(f"Unknown method selected: {method}")

                self.logger.add_step(f"Iteration {i} (h = {h}):")
                self.logger.add_step(f"f'({x}) ≈ {deriv:.8f}", is_substep=True)

                if prev_deriv is not None:
                    error = abs(deriv - prev_deriv)
                    self.logger.add_step(f"Error vs previous: {error:.2e}", is_substep=True)

                    if error <= tol:
                        self.logger.add_info(
                            f"\n  [STOPPING RULE MET] Target tolerance ({tol}) reached at Iteration {i}.")
                        stop_reason = "Tolerance Met"
                        break
                    elif h < 1e-12:
                        self.logger.add_info(f"\n  [STOPPING RULE MET] Machine precision limit reached (h too small).")
                        stop_reason = "Precision Limit"
                        break

                prev_deriv = deriv
                h = h / 2.0
            else:
                self.logger.add_info(f"\n  [STOPPING RULE MET] Maximum iterations ({max_iter}) reached.")
                stop_reason = "Max Iterations"

            self.logger.add_heading("FINAL")
            self.logger.add_info(f"f'({x}) ≈ {deriv:.8f}")

            self.logger.add_heading("VERIFICATION")
            final_h = h * 2.0

            if prev_deriv is not None:
                residual = abs(deriv - prev_deriv)
                self.logger.add_info("Method: Iterative Step-Halving Consistency")
                self.logger.add_info(f"Calculated Residual: {residual:.2e}")

                try:
                    f_x = self.evaluate(x, f)
                    f_plus = self.evaluate(x + final_h, f)
                    predicted_diff = deriv * final_h
                    actual_diff = f_plus - f_x
                    taylor_error = abs(predicted_diff - actual_diff)
                    self.logger.add_info(f"Taylor Expansion Check: f(x+h) ≈ f(x) + f'(x)h")
                    self.logger.add_info(f"Taylor Residual: {taylor_error:.2e}")

                    if residual <= tol:
                        self.logger.add_info("Status: VERIFIED (Residual within Tolerance)")
                    else:
                        self.logger.add_info("Status: CAUTION (Residual exceeds Tolerance)")
                except:
                    self.logger.add_info("Status: VERIFIED (via Residual)")
            else:
                self.logger.add_info("Status: N/A (Single iteration complete)")

            end_time = time.time()
            runtime = end_time - start_time
            self.logger.add_heading("SUMMARY")
            self.logger.add_info(f"Stop Reason      : {stop_reason}")
            self.logger.add_info(f"Total Iterations : {i}")
            self.logger.add_info(f"Runtime          : {runtime:.6f} seconds")
            self.logger.add_info(f"Python version   : {sys.version.split()[0]}")
            self.logger.add_info(f"NumPy version    : {np.__version__}")
            self.logger.add_info(f"Timestamp        : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            return deriv, self.logger.get_trail()

        except Exception as e:
            raise e


class CalculatorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Numerical Differentiation Calculator v1.7.0")
        self.root.geometry("900x850")

        # --- SCIENTIFIC CALCULATOR COLOR PALETTE ---
        self.bg_color = "#383838"  # Main dark grey housing
        self.display_bg = "#1A1A1A"  # Deep black for screens/inputs
        self.text_main = "#FFFFFF"  # White text
        self.accent_yellow = "#F3C026"  # "2nd" key yellow
        self.accent_green = "#468B3F"  # "clear" key green
        self.btn_grey = "#5A5A5A"  # Standard function key grey
        self.btn_dark = "#2B2B2B"  # Numpad/Action key dark grey

        self.root.configure(bg=self.bg_color)
        self.setup_styles()
        self.differentiator = NumericalDifferentiator()

        self.test_cases = {
            "Test 1: sin(x) via Central": {"f": "sin(x)", "x": "1.570796", "h": "0.1", "method": "Central Difference"},
            "Test 2: x^2 via Forward": {"f": "x**2", "x": "2.0", "h": "0.5", "method": "Forward Difference"},
            "Test 3: exp(x) via Backward": {"f": "exp(x)", "x": "1.0", "h": "0.1", "method": "Backward Difference"},
            "Test 4: log(x) via Central": {"f": "log(x)", "x": "10.0", "h": "0.5", "method": "Central Difference"},
            "Test 5: sqrt(x) via Forward": {"f": "sqrt(x)", "x": "4.0", "h": "0.1", "method": "Forward Difference"}
        }

        self.setup_menu()
        self.setup_ui()

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menubar)

    def show_about(self):
        about_text = (
            "Project Name: \nNumerical Differentiation Calculator\n\n"
            "Project Members: \nJohn Paul Fidelson\n"
            "Emanuel Lloyd Dagdag \n"
            "Kyle Andrei Escauriaga \n\n"
            "Project Version: \n1.5.0"
        )
        messagebox.showinfo("About", about_text)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        font_family = "Consolas"  # Monospace digital feel

        # Global frame styling
        style.configure(".", background=self.bg_color, foreground=self.text_main, font=(font_family, 11))
        style.configure("TFrame", background=self.bg_color)

        # Headers & Titles (Accent Yellow)
        style.configure("Title.TLabel", font=(font_family, 20, "bold"), padding=15, foreground=self.text_main,
                        background=self.bg_color)
        style.configure("Input.TLabel", font=(font_family, 11, "bold"), padding=5, foreground=self.accent_yellow)
        style.configure("Hint.TLabel", font=(font_family, 9, "italic"), foreground="#A0A0A0")

        # Cards (LabelFrames)
        style.configure("Card.TLabelframe", background=self.bg_color, bordercolor="#555555", borderwidth=2,
                        relief="solid")
        style.configure("Card.TLabelframe.Label", font=(font_family, 12, "bold"), background=self.bg_color,
                        foreground=self.text_main, padding=(5, 0))

        # Buttons - Standard Grey Function Keys
        style.configure("Secondary.TButton", font=(font_family, 11, "bold"), background=self.btn_grey,
                        foreground="white", bordercolor="#444444", borderwidth=2, padding=6)
        style.map("Secondary.TButton", background=[("active", "#777777")])

        # Buttons - Action/Enter Keys (Dark)
        style.configure("Primary.TButton", font=(font_family, 12, "bold"), background=self.btn_dark, foreground="white",
                        bordercolor="#111111", borderwidth=2, padding=8)
        style.map("Primary.TButton", background=[("active", "#444444")])

        # Button - Clear Key (Green)
        style.configure("Green.TButton", font=(font_family, 12, "bold"), background=self.accent_green,
                        foreground="white", bordercolor="#2D5A28", borderwidth=2, padding=8)
        style.map("Green.TButton", background=[("active", "#5CB85C")])

        # Inputs (Deep Black displays)
        style.configure("TEntry", fieldbackground=self.display_bg, foreground=self.text_main, padding=6, borderwidth=1,
                        bordercolor="#555555")

        # FIX FOR COMBOBOXES: Force the readonly state to map to the correct black background and white text
        style.configure("TCombobox", fieldbackground=self.display_bg, foreground=self.text_main, borderwidth=1)
        style.map("TCombobox",
                  fieldbackground=[("readonly", self.display_bg)],
                  foreground=[("readonly", self.text_main)],
                  selectbackground=[("readonly", self.btn_grey)],
                  selectforeground=[("readonly", self.text_main)])

    def insert_text(self, text):
        self.function_entry.insert(tk.INSERT, text)
        self.function_entry.focus()

    def load_test_case(self, event=None):
        selection = self.test_var.get()
        if selection in self.test_cases:
            tc = self.test_cases[selection]
            self.function_entry.delete(0, tk.END)
            self.x_entry.delete(0, tk.END)
            self.h_entry.delete(0, tk.END)

            self.function_entry.insert(0, tc["f"])
            self.x_entry.insert(0, tc["x"])
            self.h_entry.insert(0, tc["h"])
            self.method_var.set(tc["method"])

            self.tol_entry.delete(0, tk.END)
            self.tol_entry.insert(0, "1e-6")
            self.iter_entry.delete(0, tk.END)
            self.iter_entry.insert(0, "20")

    def setup_ui(self):
        title_label = ttk.Label(self.root, text="Numerical Differentiation Calculator", style="Title.TLabel")
        title_label.pack(pady=(10, 5))

        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill="both", expand=True)

        input_frame = ttk.LabelFrame(main_container, text=" Input Parameters ", padding="20", style="Card.TLabelframe")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))

        # === POLISHED GRID ALIGNMENT: Top Controls ===
        top_frame = ttk.Frame(input_frame)
        top_frame.pack(fill="x", pady=(0, 15))
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(3, weight=1)

        ttk.Label(top_frame, text="Load Test Case:", style="Input.TLabel").grid(row=0, column=0, sticky="w")
        self.test_var = tk.StringVar(value="Select a test case...")
        self.test_cb = ttk.Combobox(top_frame, textvariable=self.test_var, state="readonly", font=("Consolas", 11))
        self.test_cb['values'] = list(self.test_cases.keys())
        self.test_cb.grid(row=0, column=1, sticky="ew", padx=(10, 30))
        self.test_cb.bind("<<ComboboxSelected>>", self.load_test_case)

        ttk.Label(top_frame, text="Calculation Method:", style="Input.TLabel").grid(row=0, column=2, sticky="w")
        self.method_var = tk.StringVar(value="Central Difference")
        self.method_cb = ttk.Combobox(top_frame, textvariable=self.method_var, state="readonly", font=("Consolas", 11))
        self.method_cb['values'] = ("Central Difference", "Forward Difference", "Backward Difference")
        self.method_cb.grid(row=0, column=3, sticky="ew", padx=(10, 0))

        # === FUNCTION INPUT ALIGNMENT ===
        function_container = ttk.Frame(input_frame)
        function_container.pack(fill="x", expand=True)

        function_input_frame = ttk.Frame(function_container)
        function_input_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

        ttk.Label(function_input_frame, text="Function f(x):", style="Input.TLabel").pack(anchor="w")
        self.function_entry = ttk.Entry(function_input_frame, font=("Consolas", 14))
        self.function_entry.pack(fill="x", pady=(5, 5))

        hint_label = ttk.Label(function_input_frame, text="Example: sin(x), x**2, exp(x)", style="Hint.TLabel")
        hint_label.pack(anchor="w", pady=(0, 15))

        # Quick Functions Pad
        calc_frame = ttk.LabelFrame(function_container, text=" Quick Functions ", padding="10",
                                    style="Card.TLabelframe")
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
                btn = ttk.Button(button_frame, text=label, command=lambda v=value: self.insert_text(v),
                                 style="Secondary.TButton", width=6)
                btn.pack(side="left", padx=2)

        # === POLISHED GRID ALIGNMENT: Bottom Parameters ===
        params_frame = ttk.Frame(input_frame)
        params_frame.pack(fill="x", pady=15)

        for i in range(4):
            params_frame.columnconfigure(i, weight=1, uniform="params")

        labels = ["x value:", "Initial Step (h):", "Tolerance:", "Max Iters:"]
        for i, text in enumerate(labels):
            ttk.Label(params_frame, text=text, style="Input.TLabel").grid(row=0, column=i, sticky="w",
                                                                          padx=(0, 10) if i < 3 else 0)

        self.x_entry = ttk.Entry(params_frame, font=("Consolas", 12))
        self.x_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(5, 0))

        self.h_entry = ttk.Entry(params_frame, font=("Consolas", 12))
        self.h_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(5, 0))

        self.tol_entry = ttk.Entry(params_frame, font=("Consolas", 12))
        self.tol_entry.insert(0, "1e-6")
        self.tol_entry.grid(row=1, column=2, sticky="ew", padx=(0, 10), pady=(5, 0))

        self.iter_entry = ttk.Entry(params_frame, font=("Consolas", 12))
        self.iter_entry.insert(0, "20")
        self.iter_entry.grid(row=1, column=3, sticky="ew", pady=(5, 0))

        # === CENTERED BUTTONS ===
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(pady=(15, 0))

        calculate_btn = ttk.Button(button_frame, text="Compute Result", command=self.calculate, style="Primary.TButton")
        calculate_btn.grid(row=0, column=0, padx=5)

        clear_btn = ttk.Button(button_frame, text="Clear All", command=self.clear, style="Green.TButton")
        clear_btn.grid(row=0, column=1, padx=5)

        export_btn = ttk.Button(button_frame, text="Export Report", command=self.export_report,
                                style="Secondary.TButton")
        export_btn.grid(row=0, column=2, padx=5)

        # === OUTPUT PANELS ===
        answer_frame = ttk.LabelFrame(main_container, text=" Final Output ", padding="15", style="Card.TLabelframe")
        answer_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.final_answer_var = tk.StringVar()
        self.final_answer_var.set("...")
        answer_label = ttk.Label(answer_frame, textvariable=self.final_answer_var,
                                 font=("Consolas", 24, "bold"), foreground=self.text_main, background=self.bg_color)
        answer_label.pack()

        result_frame = ttk.LabelFrame(main_container, text=" Solution Trail ", padding="15", style="Card.TLabelframe")
        result_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # --- ADDED: Expand Button Frame ---
        log_ctrl_frame = ttk.Frame(result_frame)
        log_ctrl_frame.pack(fill="x", pady=(0, 5))

        expand_btn = ttk.Button(log_ctrl_frame, text="Expand Log", command=self.open_expanded_log,
                                style="Secondary.TButton")
        expand_btn.pack(side="right")
        # ----------------------------------

        self.result_text = scrolledtext.ScrolledText(
            result_frame, wrap=tk.WORD, height=15,
            font=("Consolas", 11),
            bg=self.display_bg, fg=self.text_main,
            insertbackground="white", borderwidth=2, relief="solid", padx=10, pady=10
        )
        self.result_text.configure(state='disabled')
        self.result_text.pack(fill="both", expand=True)

    def calculate(self):
        self.result_text.configure(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.final_answer_var.set("computing...")

        f_str = self.function_entry.get().strip()
        x_str = self.x_entry.get().strip()
        h_str = self.h_entry.get().strip()
        tol_str = self.tol_entry.get().strip()
        iter_str = self.iter_entry.get().strip()
        method_str = self.method_var.get()

        try:
            if not f_str or not x_str or not h_str or not tol_str or not iter_str:
                raise ValueError("ERR: Missing Parameters")
            try:
                x = float(x_str)
                h = float(h_str)
                tol = float(tol_str)
                max_iter = int(iter_str)
            except ValueError:
                raise ValueError("ERR: Invalid Number Format")
            if h == 0:
                raise ValueError("ERR: Division by Zero (h=0)")

            self.result_text.insert(tk.END, "SYS_CHECK  : OK\n" + "-" * 40 + "\n")

            derivative, steps = self.differentiator.compute_derivative(method_str, f_str, x, h, tol, max_iter)
            self.result_text.insert(tk.END, steps)
            self.final_answer_var.set(f"{derivative:.8f}")

        except Exception as e:
            self.result_text.insert(tk.END, f"SYS_CHECK  : FAIL\n\n  > {str(e)}\n\n  Please verify inputs.")
            self.final_answer_var.set("ERR")

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
        self.method_var.set("Central Difference")
        self.test_var.set("Select a test case...")

        self.result_text.configure(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.configure(state='disabled')
        self.final_answer_var.set("...")

    # --- NEW FEATURE: Pop-out Log Window ---
    def open_expanded_log(self):
        content = self.result_text.get(1.0, tk.END).strip()
        if not content or "SYS_CHECK" not in content or "FAIL" in content:
            messagebox.showinfo("Empty Log", "Please run a successful calculation first to generate a solution trail.")
            return

        # Create a new top-level window
        popout = tk.Toplevel(self.root)
        popout.title("Solution Trail - Expanded View")
        popout.geometry("800x600")
        popout.configure(bg=self.bg_color)

        # Attempt to maximize the window (Works automatically on Windows)
        try:
            popout.state('zoomed')
        except:
            pass

            # Add a larger, read-only text box styled to match the main app
        expanded_text = scrolledtext.ScrolledText(
            popout, wrap=tk.WORD,
            font=("Consolas", 14),
            bg=self.display_bg, fg=self.text_main,
            insertbackground="white", borderwidth=2, relief="solid", padx=20, pady=20
        )
        expanded_text.pack(fill="both", expand=True, padx=15, pady=15)

        # Insert current log content and disable editing
        expanded_text.insert(tk.END, content)
        expanded_text.configure(state='disabled')

    def export_report(self):
        content = self.result_text.get(1.0, tk.END).strip()
        if not content or "SYS_CHECK" not in content or "FAIL" in content:
            messagebox.showwarning("Export Error", "No valid computation to export.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Export Solution Trail"
        )
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Data exported to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("IO Error", f"Failed to write file:\n{str(e)}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = CalculatorApp()
    app.run()