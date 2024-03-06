import math

class _Funciones:


    def histograma(num1,num2,num3):
        print()
        print(num1*"*")
        print(num2*"*")
        print(num3*"*")
        print()


    def contarlista(lista):
        n=0
        for i in lista:
            n=n+1

        return n
    

    def mayor(num1,num2):
        if num1<num2:
            return num2
        elif num1>num2:
            return num1
        else:
            return num1,"=",num2
        

    def generar(num,string):
        print(num*string)


    def inverso(string):
        reverso=string[::-1]
        return reverso

    def multiplicar(valores):
        n=1
        for i in valores:
            n=n*i
        return n

    def palindromo(string):
        reverso=string[::-1]
        verificar=string==reverso
        return verificar

    def sumar(valores):
        n=0
        for i in valores:
            n=n+i
        return n


    def vocalono(string):
        n=string.lower()
        vocales=["a","e","i","o","u"]
        if vocales.count(n)>0:
            return True
        else:
            return False
    import math

    def media(lista):
        n=0
        for i in lista:
            n=n+i
        numero=len(lista)
        resultado=n/numero
        return resultado



    def raizentera(num):
    
        for i in range(0,100000000000000000):
            if num==i*i:
                return i


    def binarioent(num):
        ent=str(num)
        nums=list()
        ex=0
        s=0
        for i in ent:
            nums.append(i)
        c=int(len(nums))
    
        for n in nums:
            p=int(n)
            c=c-1
            b=(p*math.pow(2,c))
            s=s+b
        return s
    
    def interescomp(cap,tasa,tiempo):
        res=cap*math.pow(1+tasa/100,tiempo)
        res=round(res,4)
        return res
