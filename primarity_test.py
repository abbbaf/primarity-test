

"""
Primarity tests:

    Input size range (bit) |        Algorithm
    -----------------------------------------------------
            0-20           |  Trial division
            20-64          |  Baillie-PSW primality test 
            64-            |  Miller-Rabin primality test    

            Why 40 rounds for Miller-Rabin?
            https://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes

"""


import math
import random
import sys



class BailliePSW():

    def __init__(self,n,initialize=True):
        self.n = n
        self.firstPrimeCheck = None
        if initialize:
            if int(n) != n or (n > 2 and n % 2 == 0) or n == 1 or n == 0:
                self.firstPrimeCheck = False
            elif n == 2 or n == 0:
                self.firstPrimeCheck = True


    def check(self):

        if self.firstPrimeCheck != None:
            return self.firstPrimeCheck


        if self.isPerfectSquare():
            return False

        """ if not MillerRabin(self.n,1):
            return False """

        D = self.findJacobSymbol()

        try:
            return self.Lucas(D)
        except ArithmeticError:
            return False


    def isPerfectSquare(self):
        a = self.n**0.5
        return int(a) == a


    def inversePossiblePrime(self,a):
        n = self.n  
        inv = pow(a,n-2,n)
        if (a*inv) % n == 1:
            return inv
        else:
            raise ArithmeticError("{} has no inverse modulo {}. (assuming the modulus is a probable prime)".format(a,n))


    def jacobSymbol(self,a):
        n = self.n
        a %= n
        j = 1
        while a != 0:
            while a % 2 == 0:
                a >>= 1
                if n % 8 in [3,5]:
                    j = -j
            a, n = n, a
            if a % 4 == n % 4 == 3:
                j = -j
            a %= n
        return j if n == 1 else 0

    
    def findJacobSymbol(self):
        D = 5
        while self.jacobSymbol(D) != -1:
            D = abs(D)+2
            if D % 4 == 3:
                D = -D
            
        return D


    def findUandV(self,k,D):
        u,v = 1, 1
        twoInv = self.inversePossiblePrime(2)

        for b in bin(k)[3:]:
            u,v = u*v, (v**2 + D*u**2)*twoInv

            if b == '1':
                u, v = (u + v)*twoInv , (D*u + v)*twoInv

            u %= self.n
            v %= self.n

        return { 'u' : u, 'v' : v  }
    

    def Lucas(self,D):
        n = self.n
        d = n+1
        while d % 2 == 0:
            d >>= 1

        u_v = self.findUandV(d,D)
        if not u_v:
            return False

        if u_v['u'] % n == 0:
            return True

        while d <= n+1:
            if self.findUandV(d,D)['v'] % n == 0:
                return True
            d <<= 1
    
        return False


def MillerRabin(n,numOfRounds=40,initialize=True):
    if initialize:
        if n == 2 or n == 3:
            return True
        elif n % 2 == 0 or n % 3 == 0 or n == 1:
            return False

    k = 0
    m = n-1
    while (m % 2 == 0):
        m >>= 1
        k += 1
    
    for i in range(numOfRounds):
        a = 2 if numOfRounds == 1 else random.randrange(2,n-1)
        x = pow(a,m,n)
        if x == 1 or x == n-1:
            continue
        for j in range(k-1):
            x = pow(x,2,n)
            if x == n-1:
                break
        else:
            return False
    return True


def trialDivision(n):
    return n > 1 and all(n % i for i in range(2,int(n**0.5)+1))



"""
Algorithm for Mersenne's primes 
"""
def Lucas_Lehmer(p):
    if not isPrime(p):
        return False
    s = 4
    m = 2**p - 1
    for i in range(p-2):
        s = (s**2 - 2) % m
    return s == 0


def isPrime(n):

    if type(n) != int or n < 2:
        return False

    maxTrialDivision = 2**20
    maxBP = 2**64

    if n % 2 == 0:
        return n == 2


    if n <= maxTrialDivision:
        return trialDivision(n)


    if n & (n+1) == 0:
        i = 0
        while n:
            n >> 1
            i += 1
        return Lucas_Lehmer(i)
    
    if n <= maxBP:
        return BailliePSW(n,initialize=False).check()


    return MillerRabin(n,initialize=False)
    

def main():
    if len(sys.argv) == 1:
        print(sys.argv[0] + " <prime-number-to-check>")
    else:
        try:
            num = int(sys.argv[1])
            if num == 1:
                print("1 is neighter prime nor composite!")
            elif (isPrime(num)):
                print(str(num) + " is a prime number!")
            else:
                print(str(num) + " is a composite number")
        except ValueError:
            print("Error: input must be an integer")

main()
