import math
import cmath
import numpy as _np

_SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')

_sign = lambda x: math.copysign(1, x)


def _signsym(x: float or int):
    if _sign(x) >= 0:
        return '+'
    elif _sign(x) == -1:
        return '-'
    else:
        raise ValueError('sign cannot be determined')

def _unpack(a):
    arr = []
    for x in a:
        if isinstance(x, complex):
            arr += [x.real, x.imag]
        elif isinstance(x, int | float):
            arr.append(float(x))
        elif isinstance(x, list):
            arr += _unpack(x)
    return arr

def _init(arr: list[int | float]):
    arr = _np.trim_zeros(arr, 'b')
    return [] if len(arr) == 0 else [(float(arr[n]) if n < len(arr) else 0) for n in range(2 ** math.ceil(math.log2(len(arr))))]


class Tsr:

    def __init__(self, *args):
        self.v = _init(_unpack(args))

    def dim(self):
        return len(self.v)

    def dimp(self):
        return int(math.log2(self.dim()))

    def __str__(self, show_zeroes=False):
        return_str = ''
        if self.dim() > 0:
            if not all([x == 0 for x in self.v]):
                for n in range(self.dim()):
                    if self.v[n] != 0 or show_zeroes:
                        return_str += f'{_signsym(self.v[n])}{abs(self.v[n])}e{str(n).translate(_SUB)}'
                if return_str[0] == '+':
                    return_str = return_str[1:]
        if return_str == '':
            return_str += '0'
        return f'({return_str})'

    def __abs__(self):
        return sum([x**2 for x in self.v])**0.5

    def __neg__(self):
        return Tsr([-x for x in self.v])

    def __add(self, other, t):
        if isinstance(other, Tsr):
            arr = []
            for n in range(max(self.dim(), other.dim())):
                s = self.v[n] if n < self.dim() else 0
                o = other.v[n] if n < other.dim() else 0
                arr.append(s + o)
            return Tsr(arr)
        else:
            raise TypeError(
                f'unsupported operand type(s) for {t}: \'{self.__class__.__name__}\' and \'{other.__class__.__name__}\'')

    def __add__(self, other):
        return self.__add(other, '+')

    def __iadd__(self, other):
        self.v = (self.__add(other, '+=')).v
        return self

    def __sub__(self, other):
        return self.__add(-other, '-')

    def __isub__(self, other):
        self.v = (self.__add(-other, '-')).v
        return self

    def __mul(self, other, t):
        if isinstance(other, int | float):
            return Tsr([other * x for x in self.v])
        elif isinstance(other, Tsr):
            if self.dim() <= 2 and other.dim() <= 2:
                return Tsr(self.native()*other.native())
            else:
                tsr = Tsr()
                for n in range(self.dim()):
                    for m in range(other.dim()):
                        s = self.v[n]
                        o = other.v[m]
                        w = n ^ m
                        tsr += e(w) * {1: -s, 0: s}[(n & m) & 1] * o
                return tsr
        else:
            raise TypeError(
                f'unsupported operand type(s) for {t}: \'{self.__class__.__name__}\' and \'{other.__class__.__name__}\'')

    def __mul__(self, other):
        return self.__mul(other, '*')

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        self.v = (self.__mul(other, '*=')).v
        return self

    def exp(self):
        if self.dim() <= 2:
            return Tsr(math.e**(self.native()))
        else:
            out = Tsr(1)
            for n in range(self.dim()):
                if n % 2 == 0:
                    out *= (math.cosh(self.v[n]) * Tsr(1) + math.sinh(self.v[n]) * e(n))
                if n % 2 == 1:
                    out *= (math.cos(self.v[n]) * Tsr(1) + math.sin(self.v[n]) * e(n))
            return out

    def cosh(self):
        return (self.exp() + (-self).exp()) / 2

    def ln(self):
        if self.dim() > 2:
            a = Tsr(self.v[0:self.dim() // 2])
            b = Tsr(self.v[self.dim() // 2:self.dim()])
            p = -((a - b) / (a.sq() - b.sq()).sqrt()).ln()
            out = (a / p.cosh()).ln() + p * e(self.dim() // 2)
            return out
        elif self.dim() == 2:
            return Tsr(cmath.log(self.native()))
        else:
            return Tsr(math.log(self.native()))

    def __round__(self, n=1):
        return Tsr([round(x, n) for x in self.v])

    def invert(self):
        if self.dim() <= 2:
            return Tsr(1 / self.native())
        else:
            return (-self.ln()).exp()

    def sqrt(self):
        if self.dim() <= 2:
            return Tsr(self.native() ** 0.5)
        else:
            return (self.ln() / 2).exp()

    def sq(self):
        return self * self

    def __truediv(self, other, t):
        if isinstance(other, int | float):
            return Tsr([x / other for x in self.v])
        elif isinstance(other, Tsr):
            return self * other.invert()
        else:
            raise TypeError(
                f'unsupported operand type(s) for {t}: \'{self.__class__.__name__}\' and \'{other.__class__.__name__}\'')

    def __truediv__(self, other):
        return self.__truediv(other, '/')

    def __rtruediv__(self, other):
        if isinstance(other, int | float | Tsr):
            return other * self.invert()
        else:
            raise TypeError(
                f'unsupported operand type(s) for /: \'{self.__class__.__name__}\' and \'{other.__class__.__name__}\'')

    def __itruediv__(self, other):
        self.v = (self.__truediv(other, '/=')).v
        return self

    def __pow(self, other, t):
        if isinstance(other, int | float | Tsr):
            if isinstance(other, Tsr):
                if self.dim() <= 2 and other.dim() <= 2:
                    return Tsr(self.native() ** other.native())
                elif other == Tsr(2):
                    return self.sq()
                else:
                    return (other * self.ln()).exp()
            elif isinstance(other, int | float):
                if other == 2:
                    return self.sq
                elif self.dim() <= 2:
                    return Tsr(self.native() ** other)
                else:
                    return (other * self.ln()).exp()
        else:
            raise TypeError(
                f'unsupported operand type(s) for {t}: \'{self.__class__.__name__}\' and \'{other.__class__.__name__}\'')

    def __pow__(self, other):
        return self.__pow(other, '**')

    def __rpow__(self, other):
        if isinstance(other, int | float | Tsr):
            if isinstance(other, Tsr):
                if self.dim() + other.dim() <= 4:
                    return Tsr(other.native() ** self.native())
                else:
                    return (other * self.ln()).exp()
            elif isinstance(other, int | float):
                if self.dim() <= 2:
                    return Tsr(other ** self.native())
                else:
                    return (other * self.ln()).exp()
        else:
            raise TypeError(
                f'unsupported operand type(s) for **: \'{self.__class__.__name__}\' and \'{other.__class__.__name__}\'')

    def __ipow__(self, other):
        self.v = (self.__pow(other, '**=')).v
        return self

    def native(self):
        match self.dim():
            case 2:
                return self.v[0] + self.v[1] * 1j
            case 1:
                return self.v[0]
            case 0:
                return 0
            case _:
                raise ValueError(
                    f'unsupported dimension: {self.dim()}')


def e(n):
    out = [0] * n
    out.append(1)
    return Tsr(out)
