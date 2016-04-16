import math

def main():
    q=1.60217657*(10**-19) #C
    m=9.10938291*(10**-31) #kg
    B=1.5 #kg/(Cs)
    c=299792458 #m/s
    for i in range(100):
        x=float((i*0.1))
        w=0.1
        j=(m**2)*(c**4)+(q*B*c*((x**2)+(w**2))/(2*w))**2
        E=math.sqrt(j)/(1.602*(10**-10))
        print("%r meters: %r GeV") %(x, E)
        
main()