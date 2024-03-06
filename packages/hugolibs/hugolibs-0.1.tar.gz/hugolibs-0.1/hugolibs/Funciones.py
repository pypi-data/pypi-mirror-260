

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
