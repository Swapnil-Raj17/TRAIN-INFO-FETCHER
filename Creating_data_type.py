class Fraction:
    def __init__(self, n, d):
        if d == 0:
            raise ValueError("Denominator cannot be zero.")
        
        gcd = self.find_gcd(n, d)
        self.num = n // gcd
        self.den = d // gcd

    def find_gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def __str__(self):
        return f"{self.num}/{self.den}"

    def __add__(self, other):
        temp_num = self.num * other.den + other.num * self.den
        temp_den = self.den * other.den
        return Fraction(temp_num, temp_den) 
    
    def __sub__(self, other):
        temp_num = self.num * other.den - other.num * self.den
        temp_den = self.den * other.den
        return Fraction(temp_num, temp_den) 
    def __mul__(self,other):
        temp_num = self.num * other.num
        temp_den = self.den * other.den
        return Fraction(temp_num, temp_den)
    
    def __truediv__(self,other):
        temp_num = self.num * other.den
        temp_den = self.den * other.num
        return Fraction(temp_num, temp_den)
        

x = Fraction(5,2)
y = Fraction(3,4)
print(x + y)
print(x - y)
print(x * y)
print(x / y)
