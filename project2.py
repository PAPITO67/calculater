import ast
import math
import operator
import tkinter as tk
from tkinter import messagebox

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Div: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

functions = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,

}

def calculate_experession(expr):
    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.Name) and node.id == "pi":
            return math.pi

        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            return operators[type(node.op)](
                evaluate(node.left),
                evaluate(node.right)
                )
        if isinstance(node, ast.Call) and isinstance(node.func,ast.Name):
            name = node.func.id
            if name in functions and len(node.args) == 1 and not node.keywords:
                return functions[name](evaluate(node.args[0]))

            raise ValueError("Unsupported calculation.")
    return evaluate(ast.parse(expr, mode="eval").body)


def add_to_display(value):
    display.insert(tk.END, value)

def clear_display():
    display.delete(0, tk.END)

def delete_last():
    current = display.get()
    display.delete(len(current) - 1, tk.END)

def calculate():
    expression = display.get().strip()
    try:
        result = calculate_experession(expression)
        display.delete(0, tk.END)
        display.insert(0, str(result))
    except (SyntaxError, ValueError, ZeroDivisionError):
        messagebox.showerror("Error", "Invalid calculation.")
window = tk.Tk()
window.title("Calculator")
window.resizable(False, False)

display = tk.Entry(window, font=("Arial", 22), justify="right", width=18)
display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["(", "0", ")", "+"],
    ["C", "⌫", "sqrt(", "="],
]

for row, button_row in enumerate(buttons, start=1):
    for col, label in enumerate(button_row):
        if label == "C":
            action = clear_display
        elif label == "⌫":
            action = delete_last
        elif label == "=":
            action = calculate
        else:
            action = lambda value=label: add_to_display(value)

        tk.Button(
            window,
            text=label,
            font=("Arial", 16),
            width=5,
            height=2,
            command=action
        ).grid(row=row, column=col, padx=2, pady=2)

window.bind("<Return>", lambda event: calculate())
window.mainloop()