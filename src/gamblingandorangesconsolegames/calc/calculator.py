import math
import cmath
import re
import typing


class Calculator:
    def __init__(self):
        self.mode = "real"
        self.angle_unit = "degrees"
        self.memory = 0
        self.ans = 0
        self.constants = {
            "pi": math.pi,
            "e": math.e,
            "i": 1j
        }

    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if y == 0:
            raise ValueError("divide by zero error")
        return x / y

    def power(self, x, y):
        return x ** y

    def square_root(self, x):
        if self.mode == "real" and x < 0:
            raise ValueError("cannot calculate square root of a negative number in real mode please switch to complex mode to do this by running 'mode' ")
        return cmath.sqrt(x) if self.mode == "complex" else math.sqrt(x)

    def logarithm(self, x, base=math.e):
        if self.mode == "real" and x <= 0:
            raise ValueError("log is undefined for non-positive numbers in real mode")
        if base <= 0 or base == 1:
            raise ValueError("invalid logarithm base. the default log base is 10")
        return cmath.log(x, base) if self.mode == "complex" else math.log(x, base)

    def sine(self, x):
        x = self.to_radians(x)
        return cmath.sin(x) if self.mode == "complex" else math.sin(x)

    def cosine(self, x):
        x = self.to_radians(x)
        return cmath.cos(x) if self.mode == "complex" else math.cos(x)

    def tangent(self, x):
        x = self.to_radians(x)
        return cmath.tan(x) if self.mode == "complex" else math.tan(x)

    def to_radians(self, x):
        return x if self.angle_unit == "radians" else math.radians(x)

    def factorial(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("factorial is only defined for non-negative integers")
        return math.factorial(n)

    def absolute(self, x):
        return abs(x)

    def store_in_memory(self, value):
        self.memory = value

    def recall_memory(self):
        return self.memory

    def clear_memory(self):
        self.memory = 0

    def switch_mode(self):
        self.mode = "complex" if self.mode == "real" else "real"
        return f"switched to {self.mode} number mode successfully"

    def switch_angle_unit(self):
        self.angle_unit = "radians" if self.angle_unit == "degrees" else "degrees"
        return f"Switched to {self.angle_unit}"

    def exponential(self, x):
        return cmath.exp(x) if self.mode == "complex" else math.exp(x)

    def reciprocal(self, x):
        if x == 0:
            raise ValueError("cannot calculate reciprocal of zero")
        return 1 / x

    def to_polar(self, x):
        if self.mode != "complex":
            raise ValueError("to polar conversion is only available in complex mode. please make sure calculator is set to complex")
        r, theta = cmath.polar(x)
        return f"r = {r}, θ = {theta} radians"

    def to_rectangular(self, r, theta):
        if self.mode != "complex":
            raise ValueError("to rectangular conversion is only available in complex mode")
        return cmath.rect(r, theta)

calc = Calculator()

operations = {
    '+': calc.add,
    '-': calc.subtract,
    '*': calc.multiply,
    '/': calc.divide,
    '^': calc.power,
    'sqrt': calc.square_root,
    'log': calc.logarithm,
    'ln': lambda x: calc.logarithm(x, math.e),
    'sin': calc.sine,
    'cos': calc.cosine,
    'tan': calc.tangent,
    'fact': calc.factorial,
    'abs': calc.absolute,
    'exp': calc.exponential,
    'rec': calc.reciprocal,
}

def parse_complex(s):
    match = re.match(r'([-+]?\d*\.?\d*)(?:([-+])(\d*\.?\d*)i)?$', s.replace(' ', ''))
    if match:
        real = float(match.group(1) or 0)
        imag = float((match.group(2) or '+') + (match.group(3) or '1'))
        return complex(real, imag)
    raise ValueError(f"invalid complex number format: {s}. please make sure your format is in a+bi")

def parse_input(user_input):
    pattern = r'(\w+|\d+\.?\d*|ans|\-?\d+\.?\d*(?:[-+]\d*\.?\d*i)?)\s*([\+\-\*/\^]|\w+)\s*(\d+\.?\d*|ans|\-?\d+\.?\d*(?:[-+]\d*\.?\d*i)?)?'
    match = re.match(pattern, user_input)
    if match:
        groups = match.groups()
        x = groups[0]
        operation = groups[1]
        y = groups[2]

        if x == 'ans':
            x = calc.ans
        elif calc.mode == "complex":
            x = parse_complex(x)
        else:
            x = float(x)

        if y:
            if y == 'ans':
                y = calc.ans
            elif calc.mode == "complex":
                y = parse_complex(y)
            else:
                y = float(y)

        return x, operation, y
    raise ValueError("invalid input format")

def calculate(x, operation, y=None):
    if operation not in operations:
        raise ValueError(f"unsupported operation: {operation}")
    
    if y is None and operation not in ['sqrt', 'sin', 'cos', 'tan', 'fact', 'abs', 'exp', 'rec', 'ln']:
        raise ValueError(f"this operation: {operation} requires two operands")
    
    if y is not None:
        result = operations[operation](x, y)
    else:
        result = operations[operation](x)
    
    calc.ans = result
    return result

def format_complex(z):
    if isinstance(z, complex):
        return f"{z.real:.4f} {'+' if z.imag >= 0 else '-'} {abs(z.imag):.4f}i"
    return f"{z:.4f}"

@typing.no_type_check
def run_calculator():
    print("simple py calculator written by @orangejuiceplz")
    print("supported operations: +, -, *, /, ^, sqrt, log, ln, sin, cos, tan, fact (factorial), abs (absolute value), exp (exponential), rec (reciprocal)")
    print("commands:")
    print("  mode: switch between real and complex number mode")
    print("  angle: switch between degrees and radians")
    print("  store <value>: store a value in memory. note that this may cause a memory leak if too much values are stored")
    print("  recall: recall the value from memory")
    print("  clear: clear the memory")
    print("  polar <complex>: convert complex number to polar form")
    print("  rect <r> <theta>: convert polar to rectangular form")
    print("  constants: list available constants")
    print("  q: quit and return to the main menu screen")
    print("\nUse 'ans' to refer to the previous result")
    print("in complex mode, enter numbers as a+bi, e.g., 3+4i or 2-1i where a is your constant, b is your coefficient, and i is the imaginary unit")
    
    while True:
        user_input = input(f"\n[{calc.mode.upper()}, {calc.angle_unit.upper()}] enter your calculation: ").lower()
        
        if user_input == 'q':
            print("returning to the main menu shortly...")
            break
        elif user_input == 'mode':
            print(calc.switch_mode())
            continue
        elif user_input == 'angle':
            print(calc.switch_angle_unit())
            continue
        elif user_input.startswith('store '):
            value = float(user_input.split()[1])
            calc.store_in_memory(value)
            print(f"stored {value} in memory")
            continue
        elif user_input == 'recall':
            print(f"recalled value: {calc.recall_memory()}")
            continue
        elif user_input == 'clear':
            calc.clear_memory()
            print("mem cleared")
            continue
        elif user_input.startswith('polar '):
            try:
                complex_num = parse_complex(user_input.split(maxsplit=1)[1])
                print(calc.to_polar(complex_num))
            except ValueError as e:
                print(f"error: {str(e)}")
            continue
        elif user_input.startswith('rect '):
            try:
                r, theta = map(float, user_input.split()[1:])
                result = calc.to_rectangular(r, theta)
                print(f"rect form: {format_complex(result)}")
            except ValueError as e:
                print(f"error: {str(e)}")
            continue
        elif user_input == 'constants':
            print("constants avalible:")
            for name, value in calc.constants.items():
                print(f"  {name}: {value}")
            continue
        
        try:
            x, operation, y = parse_input(user_input)
            result = calculate(x, operation, y)
            print(f"res: {format_complex(result)}")
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"an unexpected error occurred: {str(e)}. please report this to the repository")

if __name__ == "__main__":
    run_calculator()