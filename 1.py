for j in range(len(tempElem.all_coeffs())):
    if tempElem[j] >= p:
        while tempElem[j] not in range(p):
            tempElem[j] -= p
    elif tempElem[j] < 0:
        while tempElem[j] not in range(p):
            tempElem[j] += p
print(i, ')', tempElem)


 print(temporary)
                    for ind in range(len(temporary)):
                        if temporary[ind] >= p:
                            while temporary[ind] not in range(p):
                                temporary[ind] -= p
                        elif temporary[ind] < 0:
                            while temporary[ind] not in range(p):
                                temporary[ind] += p
                    for elem in range(len(gf)):
                        if gf[elem] == temporary:
                            decryptText += alphabet[elem]
        else:
            decryptText += inputText[i]
    return decryptText


print(f'Зашифрованный текст: {encryptCypher(gf, additiveKey, multiplicativeKey)}')

polyInverseAdditiveKey = []
for i in range(len(gf)):
    polyInverseAdditiveKey = ((polyAdditiveKey * Poly(gf[i], x)) % irreducibleFunctionPoly).all_coeffs()

    for j in range(len(polyInverseAdditiveKey)):
        if polyInverseAdditiveKey[j] >= p:
            while polyInverseAdditiveKey[j] not in range(p):
                polyInverseAdditiveKey[j] -= p
        elif polyInverseAdditiveKey[j] < 0:
            while polyInverseAdditiveKey[j] not in range(p):
                polyInverseAdditiveKey[j] += p
    print(polyInverseAdditiveKey)
