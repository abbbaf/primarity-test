from primarity_test import isPrime


def abs(a):
    a = int(a) 
    return a if a > 0 else -a

def gcd(a,b):
        a, b = int(a), int(b)
        while b:
            a, b = b, a % b
        return a



class Remainder():

    def __init__(self,modulus,value):
        value = int(value)  
        self.__value = value % modulus.value
        self.__modulus = modulus

    @property
    def modulus(self):
        return self.__modulus

    @property
    def value(self):
        return self.__value


    def __int__(self):
        return self.__value

   
    def __lt__(self,v):
        return self.__value < int(v) % self.__modulus.value
  

    def __le__(self,v):
        return self.__value <= int(v) % self.__modulus.value


    def __eq__(self,v):
        return self.__value == int(v) % self.__modulus.value


    def __ne__(self,v):
        return self.__value != int(v) % self.__modulus.value


    def __ge__(self,v):
        return self.__value >= int(v) % self.__modulus.value


    def __gt__(self,v):
        return self.__value > int(v) % self.__modulus.value
 
   

    def __inv__(self):
        return self.__compute(lambda a: ~a)


    def __add__(self,v):
        return self.__compute(lambda a,b: a+b,v)

    
    def __and__(self,v):
        return self.__compute(lambda a,b: a & b,v)
    

    def __div__(self,v):
        return self.__compute(lambda a,b: a*self.__modulus.inverse(b),v)          
    
    

    def __floordiv__(self,v):
        return self.__div__(v)

    
    def __truediv__(self,v):
        return self.__div__(v)

    
    def __lshift__(self,v):
        return self.__compute(lambda a,b: a << b,v)

    
    def __mod__(self,v):
        modulus = Modulus(v)
        value = self.__value % self.__modulus.value
        return Remainder(modulus,value)


    def __mul__(self,v):
        return self.__compute(lambda a,b: a*b,v) 

    
    def __neg__(self):
        return self.__compute(lambda a: -a)

    
    def __pos__(self):
        return self

    
    def __or__(self,v):
        return self.__compute(lambda a,b: a | b,v)


    def __pow__(self,v):
        result = self.__compute(lambda a,n: pow(a,n,self.__modulus.value),abs(v))
        return result if v >= 0 else self.__modulus.inverse(result)


    def __rshift__(self,v):
        return self.__compute(lambda a,b: a >> b,v)

    
    def __sub__(self,v):
        return self.__compute(lambda a,b: a-b,v)


    def __xor__(self,v):
        return self.__compute(lambda a,b: a^b,v) 
    

    def __iadd__(self,v):
        return self.__compute(lambda a,b: a+b,v,True) 
    

    def __iand__(self,v):
        return self.__compute(lambda a,b: a & b,v,True) 


    def __idiv__(self,v):
        return self.__div(v,True)

    
    def __ifloordiv__(self,v):
        return self.__div(v,True)


    def __itruediv__(self,v):
        return self.__div(v,True)


    def __ilshift__(self,v):
        return self.__compute(lambda a,b: a << b,v,True)

    def __imod__(self,v):
        self.__modulus = Modulus(v)
        self.__value = self.__value % self.__modulus.value
        return self


    def __imul__(self,v):
        return self.__compute(lambda a,b: a*b,v,True) 


    def __ior__(self,v):
        return self.__compute(lambda a,b: a | b,v,True) 


    def __ipow__(self,v):
        result = self.__compute(lambda a,n: pow(a,n,self.__modulus.value),abs(v),True)
        return result if v >= 0 else self.__modulus.inverse(result)

    
    def __irshift__(self,v):
        return self.__compute(lambda a,b: a >> b,v,True) 

    
    def __isub__(self,v):
        return self.__compute(lambda a,b: a-b,v,True) 

 
    def __ixor__(self,v):
        self.__compute(lambda a,b: a^b,v,True) 
        return self


    def __radd__(self,v):
        v = v % self.__modulus
        return v.__add__(self)

    
    def __rmul__(self,v):
        v = v % self.__modulus
        return v.__mul__(self)


    def __ror__(self,v):
        v = v % self.__modulus
        return v.__mul__(self)


    def __rxor__(self,v):
        v = v % self.__modulus
        return v.__mul__(self)


    def __rsub__(self,v):
        v = v % self.__modulus
        return v.__sub__(self)


    def __rdiv__(self,v):
        v = v % self.__modulus
        return v.__div__(self)


    def __rfloordiv__(self,v):
        return self.__rdiv__(v)

    
    def __rtruediv__(self,v):
        return self.__rdiv__(v)


    def __rpow__(self,v):
        v = v % self.__modulus
        return v.__pow__(self)


    def __rlshift__(self,v):
        v = v % self.__modulus
        return v.__lshift__(self)


    def __rrshift__(self,v):
        v = v % self.__modulus
        return v.__rshift__(self)


    def __repr__(self):
        return str(self.__value)


    def __compute(self,expression, value = None, inPlace = False):
        if value and type(value) == Remainder and value.__modulus.value != self.__modulus.value:
            raise ArithmeticError("Cannot compute remainders with different modulus.")

        args = [self, value] if value else [self]
        result = expression(*[int(arg) for arg in args]) % self.__modulus.value
        if inPlace:
            self.__value = result
        return Remainder(self.__modulus,result) if not inPlace else self


class Modulus():

    
    def __init__(self,modulus):
        self.__value = int(modulus)
        
        self.__isPrime = isPrime(self.__value)
        
    
    @property
    def value(self):
        return self.__value


    def remainderOf(self,n):
        return Remainder(self,n)
   

    def isPrime(self):
        return self.__isPrime


    def inverse(self,a):
        if self.__isPrime:
            return pow(a,self.__value-2,self.__value)
        else:
            return self.__euclidean_algorithm(a)


    def __repr__(self):
        return str(self.__value)


    def __int__(self):
        return self.__value


    def __rmod__(self,n):
        if type(n) == Remainder:
            return n.__mod__(self.__value)
        else:
            return self.remainderOf(n)


    def __euclidean_algorithm(self,a):
        a = int(a)
        t, t_next = 0, 1
        r, r_next = self.__value, a

        while r_next:
            q = r // r_nextg
            t, t_next = t_next, t - q * t_next
            r, r_next = r_next, r - q * r_next

        if r <= 1:
            return t % self.__value
        else:
            raise ArithmeticError("{} has no inverse modulo {}".format(a,self.__value))
 
