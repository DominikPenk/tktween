import math
import enum
from typing import Callable, Dict

class Easing(enum.Enum):
    SINUSOIDAL_IN = enum.auto()
    SINUSOIDAL_OUT = enum.auto()
    SINUSOIDAL_IN_OUT = enum.auto()

    QUADRATIC_IN = enum.auto()
    QUADRATIC_OUT = enum.auto()
    QUADRATIC_IN_OUT = enum.auto()

    CUBIC_IN = enum.auto()
    CUBIC_OUT = enum.auto()
    CUBIC_IN_OUT = enum.auto()
    
    QUARTIC_IN = enum.auto()
    QUARTIC_OUT = enum.auto()
    QUARTIC_IN_OUT = enum.auto()

    QUINTIC_IN = enum.auto()
    QUINTIC_OUT = enum.auto()
    QUINTIC_IN_OUT = enum.auto()

    EXPONENTIAL_IN = enum.auto()
    EXPONENTIAL_OUT = enum.auto()
    EXPONENTIAL_IN_OUT = enum.auto()

    CIRCULAR_IN = enum.auto()
    CIRCULAR_OUT = enum.auto()
    CIRCULAR_IN_OUT = enum.auto()


# Sinusoidal easing
def sinusoidal_in(x):
    return 1 - math.cos((x * math.pi) * 0.5)

def sinusoidal_out(x):
    return math.sin((x * math.pi) * 0.5)

def sinusoidal_in_out(x):
    return -0.5 * (math.cos(math.pi * x) - 1)

# Polynomial easing
def quadratic_in(x):
    return x ** 2

def quadratic_out(x):
    return 1 - (1 - x) ** 2

def quadratic_in_out(x):
    return 2 * x ** 2 if x < 0.5 else 1 - ((-2 * x + 2) ** 2) * 0.5

def cubic_in(x):
    return x ** 3

def cubic_out(x):
    return 1 - (1 - x) ** 3

def cubic_in_out(x):
    return 4 * x ** 3 if x < 0.5 else 1 - ((-2 * x + 2) ** 3) * 0.5

def quartic_in(x):
    return x ** 4

def quartic_out(x):
    return 1 - (1 - x) ** 4

def quartic_in_out(x):
    return 8 * x ** 4 if x < 0.5 else 1 - ((-2 * x + 2) ** 4) / 2

def quintic_in(x):
    return x ** 5

def quintic_out(x):
    return 1 - (1 - x) ** 5

def quintic_in_out(x):
    return 16 * x ** 5 if x < 0.5 else 1 - ((-2 * x + 2) ** 5) * 0.5

# Exponential easing
def exponential_in(x):
    return 2 ** (10 * (x - 1)) if x != 0 else 0

def exponential_out(x):
    return 1 - 2 ** (-10 * x) if x < 1 else 1

def exponential_in_out(x):
    if x == 0:
        return 0.0
    elif x == 1:
        return 1.0
    elif x < 0.5:
        return 0.5 * 2 ** (20 * x - 10)
    else:
        return 1 - 0.5 * 2 ** (-20 * x + 10)

# Circular easing
def circular_in(x):
    return 1 - math.sqrt(1 - x ** 2)

def circular_out(x):
    return math.sqrt(1 - (1 - x) ** 2)

def circular_in_out(x):
    if x < 0.5:
        return (1 - math.sqrt(1 - (2 * x) ** 2)) * 0.5
    else:
        return (math.sqrt(1 - (-2 * x + 2) ** 2) + 1) * 0.5


EASING_FUNCTIONS: Dict[Easing, Callable[[float], float]] = {
    Easing.SINUSOIDAL_IN: sinusoidal_in,
    Easing.SINUSOIDAL_OUT: sinusoidal_out,
    Easing.SINUSOIDAL_IN_OUT: sinusoidal_in_out,
    Easing.QUADRATIC_IN: quadratic_in,
    Easing.QUADRATIC_OUT: quadratic_out,
    Easing.QUADRATIC_IN_OUT: quadratic_in_out,
    Easing.CUBIC_IN: cubic_in,
    Easing.CUBIC_OUT: cubic_out,
    Easing.CUBIC_IN_OUT: cubic_in_out,
    Easing.QUARTIC_IN: quartic_in,
    Easing.QUARTIC_OUT: quartic_out,
    Easing.QUARTIC_IN_OUT: quartic_in_out,
    Easing.QUINTIC_IN: quintic_in,
    Easing.QUINTIC_OUT: quintic_out,
    Easing.QUINTIC_IN_OUT: quintic_in_out,
    Easing.EXPONENTIAL_IN: exponential_in,
    Easing.EXPONENTIAL_OUT: exponential_out,
    Easing.EXPONENTIAL_IN_OUT: exponential_in_out,
    Easing.CIRCULAR_IN: circular_in,
    Easing.CIRCULAR_OUT: circular_out,
    Easing.CIRCULAR_IN_OUT: circular_in_out,
}

def get_easing(type: Easing | None) -> Callable[[float], float]:
    if type is None or callable(type):
        return lambda x: x
    return EASING_FUNCTIONS[type]


def get_inverse_easing(type: Easing | None) -> Easing | None:
    inverse_mapping = {
        Easing.SINUSOIDAL_IN: Easing.SINUSOIDAL_OUT,
        Easing.SINUSOIDAL_OUT: Easing.SINUSOIDAL_IN,
        Easing.SINUSOIDAL_IN_OUT: Easing.SINUSOIDAL_IN_OUT,
        Easing.QUADRATIC_IN: Easing.QUADRATIC_OUT,
        Easing.QUADRATIC_OUT: Easing.QUADRATIC_IN,
        Easing.QUADRATIC_IN_OUT: Easing.QUADRATIC_IN_OUT,
        Easing.CUBIC_IN: Easing.CUBIC_OUT,
        Easing.CUBIC_OUT: Easing.CUBIC_IN,
        Easing.CUBIC_IN_OUT: Easing.CUBIC_IN_OUT,
        Easing.QUARTIC_IN: Easing.QUARTIC_OUT,
        Easing.QUARTIC_OUT: Easing.QUARTIC_IN,
        Easing.QUARTIC_IN_OUT: Easing.QUARTIC_IN_OUT,
        Easing.QUINTIC_IN: Easing.QUINTIC_OUT,
        Easing.QUINTIC_OUT: Easing.QUINTIC_IN,
        Easing.QUINTIC_IN_OUT: Easing.QUINTIC_IN_OUT,
        Easing.EXPONENTIAL_IN: Easing.EXPONENTIAL_OUT,
        Easing.EXPONENTIAL_OUT: Easing.EXPONENTIAL_IN,
        Easing.EXPONENTIAL_IN_OUT: Easing.EXPONENTIAL_IN_OUT,
        Easing.CIRCULAR_IN: Easing.CIRCULAR_OUT,
        Easing.CIRCULAR_OUT: Easing.CIRCULAR_IN,
        Easing.CIRCULAR_IN_OUT: Easing.CIRCULAR_IN_OUT,
    }

    return inverse_mapping.get(type, None)



