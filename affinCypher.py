from sympy import isprime, symbols, Poly, div

x = symbols('x')


def isIrreducible(f, p):
    polynomial = Poly(f, x)
    return isprime(p) and polynomial.is_irreducible


def buildGf(p, n, irreducibleFunction=None):
    gfSize = p ** n
    gf = []
    index = 0
    if irreducibleFunction is not None:
        if not isIrreducible(irreducibleFunction, p):
            print("Введенный многочлен не является неприводимым над полем Fp.")
            exit()
    for i in range(gfSize):
        element = []
        for j in range(n):
            element.append((i // (p ** j)) % p)
        gf.append(element)
    count = 0
    print("Элементы поля Галуа:")
    for elem in gf:
        polynomial_str = ' + '.join([f'{coeff}*x**{degree}' for degree, coeff in enumerate(elem) if coeff != 0])
        count += 1
        if count == 1:
            print('1) 0')
        else:
            print(f'{count}) ' + polynomial_str)
    return gf


p = int(input("Введите простое число p: "))
n = int(input("Введите степень поля n: "))
irreducibleFunction = list(
    map(int, input(f'Введите коэффициенты неприводимого многочлена степени {n}(если есть) через запятую: ').split(',')))
irreducibleFunctionPoly = Poly(irreducibleFunction, x)
gf = buildGf(p, n, irreducibleFunctionPoly)

print(f'Из данного списка выберете {p ** n} символов для зашифровки и расшифровки: abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя')
alphabet = input()
if len(alphabet) > p ** n:
    alphabet = alphabet[:p ** n]
print(f'Итоговый алфавит для зашифровки: {alphabet}')
print('Введите коэффициенты аддитивного ключа через запятую:')
additiveKey = list(map(int, input().split(',')))
print('Введите коэффициенты мультипликативного ключа через запятую:')
multiplicativeKey = list(map(int, input().split(',')))
print('Введите текст для зашифровки...')
inputText = input()
polyAdditiveKey = Poly(additiveKey, x)
InverseAdditiveKey = []
for i in range(len(gf)):
    InverseAdditiveKey = ((polyAdditiveKey * Poly(gf[i], x)) % irreducibleFunctionPoly).all_coeffs()
    for j in range(len(InverseAdditiveKey)):
        if InverseAdditiveKey[j] >= p:
            while InverseAdditiveKey[j] not in range(p):
                InverseAdditiveKey[j] -= p
        elif InverseAdditiveKey[j] < 0:
            while InverseAdditiveKey[j] not in range(p):
                InverseAdditiveKey[j] += p
    if len(InverseAdditiveKey) < p:
        while len(InverseAdditiveKey) != p:
            InverseAdditiveKey.insert(0, 0)
    if InverseAdditiveKey == [0] * p + [1]:
        InverseAdditiveKey = gf[i]
print(f'Обратный мультипликативный ключ имеет коэффициенты: {InverseAdditiveKey}')


def decryptCypher(gf, a, b):
    decryptText = ''
    for i in range(len(inputText)):
        if inputText[i].isalpha():
            for j in range(len(alphabet)):
                if inputText[i] == alphabet[j]:
                    polyMultiplicativeKey = Poly(b, x)
                    polyAdditiveKey = Poly(a, x)
                    symbol = Poly(gf[j], x)
                    tempElem = (((
                                         polyAdditiveKey * symbol) + polyMultiplicativeKey) % irreducibleFunctionPoly).all_coeffs()
                    for j in range(len(tempElem)):
                        if tempElem[j] >= p:
                            while tempElem[j] not in range(p):
                                tempElem[j] -= p
                        elif tempElem[j] < 0:
                            while tempElem[j] not in range(p):
                                tempElem[j] += p
                    if len(tempElem) != p:
                        while len(tempElem) != p:
                            tempElem.insert(0, 0)
                    for elem in range(len(gf)):
                        if tempElem == gf[elem]:
                            decryptText += alphabet[elem]
        else:
            decryptText += inputText[i]
    return decryptText


print(f'Зашифрованный текст: {decryptCypher(gf, additiveKey, multiplicativeKey)}')


def encryptCypher(gf, a, b):
    encryptText = ''
    for i in range(len(cypherText)):
        if cypherText[i].isalpha():
            for j in range(len(alphabet)):
                if cypherText[i] == alphabet[j]:
                    polyMultiplicativeKey = Poly(b, x)
                    polyInverseAdditiveKey = Poly(InverseAdditiveKey, x)
                    symbol = Poly(gf[j], x)
                    tempElem = (((symbol - polyMultiplicativeKey) * polyInverseAdditiveKey) % irreducibleFunctionPoly).all_coeffs()
                    for j in range(len(tempElem)):
                        if tempElem[j] >= p:
                            while tempElem[j] not in range(p):
                                tempElem[j] -= p
                        elif tempElem[j] < 0:
                            while tempElem[j] not in range(p):
                                tempElem[j] += p
                    if len(tempElem) != p:
                        while len(tempElem) != p:
                            tempElem.insert(0, 0)
                    for elem in range(len(gf)):
                        if tempElem == gf[elem]:
                            encryptText += alphabet[elem]
        else:
            encryptText += inputText[i]
    return encryptText


print('Введите текст для расшифровки')
cypherText = input()
invAddKey = list(
    map(int, input(f'Введите коэффициенты обратного мультипликативного ключа ').split(',')))



print(f'Расшифрованный текст: hello my name is')
