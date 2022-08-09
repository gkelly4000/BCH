# Function to check the generated check digits are not greater than 10
def check_digit(n):
    if(n > 10): return False
    return True

# Function to check if a digits is negative
def negative(x,m):
    if(x < 0): return m + x
    return x

# Function to find the inverse of a number under mod m
def inverse(n, m):
    if(n < 0): n = negative(n,m)
    for i in range(m):
        x = (i *n) % 11
        if(x == 1): return i
    return -1

# Function to add two numbers under mod m
def addition(x, y, m):
    if (x < 0): x = negative(x, m)
    if (y < 0): y = negative(y, m)
    return (((x % m) + (y % m)) % m)

# Function to multiply two numbera under mod m
def multiplication(x, y, m):
    if (x < 0): x = negative(x, m)
    if (y < 0): y = negative(y, m)
    return (((x % m) * (y % m)) % m)

# Function to find square root of a number under mod 11
def square_root(x):
    if(x == 1): return 1
    if(x == 2): return -1
    if(x == 3): return 5
    if(x == 4): return 2
    if(x == 5): return 4
    if(x == 6): return -1
    if(x == 7): return -1
    if(x == 8): return -1
    if(x == 9): return 3
    if(x == 10): return 1

# Function to generate the 4 check digits under mod 11
# Takes 6 digits from user and generates 4 check digits
# If any of the check digits are greater than 10 then
# that number is unusable
def gen_digits():
    c = input("Enter 6 digits: ")
    d = []

    for i in range(len(c)):
        x = int(c[i])
        d.append(x)

    d.append((4 * d[0] + 10 * d[1] + 9 * d[2] + 2 * d[3] + d[4] + 7 * d[5])%11)
    d.append((7 * d[0] + 8 * d[1] + 7 * d[2] + d[3] + 9 * d[4] + 6 * d[5])%11)
    d.append((9 * d[0] + d[1] + 7 * d[2] + 8 * d[3] + 7 * d[4] + 7 * d[5] % 11)) 
    d.append((d[0] + 2 * d[1] + 9 * d[2] + 10 * d[3] + 4 * d[4] + d[5]) % 11)

    for i in range(6,10):
        if(not check_digit(d[i])):
            print("Unuseable Number!")
            return 1
    
    print('output {}'.format(d))

# Function to generate the four syndromes needed for error detection and correction
# Takes an integer array as input 
# Returns the four syndromes
def gen_syndromes(d):
    s1 = 0
    s2 = 0
    s3 = 0
    s4 = 0

    for i in range(len(d)):
        s1 += d[i]
        s2 += (i+1) * d[i]
        s3 += (((i+1)*(i+1)) % 11) * d[i]
        s4 += (((i+1)*(i+1)*(i+1)) % 11) * d[i]

    s1 = s1 % 11
    s2 = s2 % 11
    s3 = s3 % 11
    s4 = s4 % 11

    return s1,s2,s3,s4

# Function to correct single errors in a BCH(10,6) number
# If the error position is equal to zero 
# Or the digit is corrected to a 10
# Then there is more than two errors present and are unable to correct the errors
def single_error(d,s1,s2,s3,s4,p,q,r):
    i = (s2 * inverse(s1, 11)) % 11
    a = s1
    
    d[i - 1] = d[i] - a
    d[i - 1] = d[i- 1] % 11

    if (i == 0 or d[i - 1] == 10):
        print("More than two errors(syn({},{},{},{}) pqr({},{},{}))".format(s1,s2,s3,s4,p,q,r)) 
        return

    print('output {}'.format(d))
    print('single_error (i={}, a={}, syn({},{},{},{}))'.format(i, a, s1,s2,s3,s4))
    return 

# Function to correct two errors in a BCH(10,6) number
# If there is no square root under mod 11,
# Or if either error position is 0,
# Or if either of the digits are corrected to 10
# Then there are more than two errors present and are unable to correct them
def double_error(d,s1,s2,s3,s4,p,q,r):
    inv = inverse((2*p),11) % 11
    sqr = ((q*q)-4*p*r) % 11
    sqr = square_root(sqr)

    if sqr == -1:
        print("More than two errors(syn({},{},{},{}) pqr({},{},{}))".format(s1,s2,s3,s4,p,q,r)) 
        return 

    i = (((q * -1) + sqr) * inv) % 11
    j = (((q * -1) - sqr) * inv) % 11

    if (i == 0 or j == 0):
        print("More than two errors(syn({},{},{},{}) pqr({},{},{}))".format(s1,s2,s3,s4,p,q,r)) 
        return

    b = (i*s1-s2) * inverse(negative((i-j),11),11) % 11
    a = negative((s1 - b), 11) % 11

    d[i - 1] -= a
    d[i - 1] = d[i - 1] % 11

    if(d[i - 1] == 10): 
        print("More than two errors(syn({},{},{},{}) pqr({},{},{}))".format(s1,s2,s3,s4,p,q,r)) 
        return

    d[j - 1] -= b
    d[j - 1] = d[j - 1] % 11

    if(d[j - 1] == 10):
        print("More than two errors(syn({},{},{},{}) pqr({},{},{}))".format(s1,s2,s3,s4,p,q,r)) 
        return
        
    print('output {}'.format(d))
    print('double_error (i={}, a={}, j={}, b={}, syn({},{},{},{})), pqr ({},{},{})'.format(i,a,j,b,s1,s2,s3,s4,p,q,r))
    return 
 
    
def main():
    inp = input("Press 1 to generate check digits or 2 for error correction: ")
    if inp == '1':
        gen_digits()
    elif inp == '2':
        c = input("Enter number: ")
        d = []

        for i in range(len(c)):
            x = int(c[i])
            d.append(x)

        s1, s2, s3, s4 = gen_syndromes(d)

        if(s1 == 0 and s2 == 0 and s3 == 0 and s4 == 0):
            print("No errors")
            return
        
        p = ((s2 * s2) - (s1 * s3)) % 11 
        q = ((s1 * s4) - (s2 * s3)) % 11
        r = ((s3 * s3) - (s2 * s4)) % 11

        if (p == 0) and (q == 0) and (r == 0):
            single_error(d,s1,s2,s3,s4,p,q,r)
            return 

        double_error(d,s1,s2,s3,s4,p,q,r)
        return 

    return -1  

main()