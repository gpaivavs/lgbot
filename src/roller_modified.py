import random
from functools import reduce


class Rolagem:
    def __init__(self, quantidade=1, face=20, vantagem=0, modificador=0, nome=None):
        self.quantidade = int(quantidade)
        self.face = int(face)
        self.vantagem = int(vantagem)
        self.modificador = int(modificador)
        self.nome = nome
        self.total = 0
        self.resultados = []

    def rolar(self):
        self.resultados = [random.randint(1, self.face) for dado in range(self.quantidade)]
        resultados_sorted = self.resultados.sort(reverse=True)
        if self.vantagem > 0:
            self.total = reduce(lambda a, b: a + b, self.resultados[:self.vantagem])
        elif self.vantagem < 0:
            self.total = reduce(lambda a, b: a + b, self.resultados[self.vantagem:])
        else:
            self.total = reduce(lambda a, b: a + b, self.resultados)
        self.total += self.modificador


def limpar_string(string=''):
    quantidade, string = string.split('d')
    if quantidade == '':
        quantidade = 1
    face = 20
    vantagem = 0
    modificador = 0
    desvantagem = False
    mod_neg = False

    if 'l' in string: desvantagem = True
    if '-' in string: mod_neg = True

    if ('h' in string or 'l' in string) and ('+' in string or '-' in string):
        if 'h' in string:
            face, string = string.split('h')
        elif 'l' in string:
            face, string = string.split('l')
        if '+' in string:
            vantagem, modificador = string.split('+')
        elif '-' in string:
            vantagem, modificador = string.split('-')
    elif ('h' or 'l') in string:
        if 'h' in string:
            face, vantagem = string.split('h')
        elif 'l' in string:
            face, vantagem = string.split('l')
    elif ('+' or '-') in string:
        if '+' in string:
            face, modificador = string.split('+')
        elif '-' in string:
            face, modificador = string.split('-')
    else:
        face = string

    quantidade = int(quantidade)
    face = int(face)
    vantagem = int(vantagem)
    modificador = int(modificador)
    if desvantagem:
        vantagem *= -1

    if mod_neg:
        modificador *= -1

    return quantidade, face, vantagem, modificador


rolagem_dict = {}

if __name__ == '__main__':
    input = '5d100l2+20'
    a, b, c, d = limpar_string(input)
    rolagem = Rolagem(a, b, c, d)
    rolagem.rolar()
    print(a, b, c, d)
    print(rolagem.resultados)
    print(rolagem.total)
