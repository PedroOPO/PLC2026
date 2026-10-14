
def analisar(texto):
   

    tokens = []
    i = 0
    n = len(texto)

    while i < n:
        c = texto[i]

        if c.isspace():
            i += 1

        elif c == "#":
            while i < n and texto[i] != "\n":
                i += 1

        elif c == '"':
            inicio = i
            i += 1

            while i < n and texto[i] != '"':
                i += 1

            if i == n:
                raise ValueError(
                    f"String sem aspas de fecho na posição {inicio}"
                )

            valor = texto[inicio:i + 1]
            tokens.append(("STRING", valor))
            i += 1

        elif c == "?":
            inicio = i
            i += 1

            inicio_nome = i
            while i < n and texto[i].isalnum():
                i += 1

            if i == inicio_nome:
                raise ValueError(
                    f"Variável sem identificador na posição {inicio}"
                )

            valor = texto[inicio:i]
            tokens.append(("VARIAVEL", valor))

        elif c == "@":
            inicio = i

            if i + 2 >= n:
                raise ValueError(
                    f"Identificador de língua incompleto na posição {inicio}"
                )

            lingua = texto[i + 1:i + 3]

            if not all(carater.isalnum() for carater in lingua):
                raise ValueError(
                    f"Identificador de língua inválido na posição {inicio}"
                )

            if i + 3 < n and texto[i + 3].isalnum():
                raise ValueError(
                    f"O identificador de língua deve ter dois caracteres "
                    f"na posição {inicio}"
                )

            tokens.append(("LINGUA", texto[i:i + 3]))
            i += 3

        elif c in "{}.":
            tokens.append(("DELIMITADOR", c))
            i += 1

        elif c.isdigit():
            inicio = i

            while i < n and texto[i].isdigit():
                i += 1

            tokens.append(("NUMERO", texto[inicio:i]))

        elif c.isalnum():
            inicio = i

            while i < n and texto[i].isalnum():
                i += 1

            if (
                i < n
                and texto[i] == ":"
                and i + 1 < n
                and texto[i + 1].isalnum()
            ):
                i += 1

                while i < n and texto[i].isalnum():
                    i += 1

            valor = texto[inicio:i]

            if valor == "LIMIT":
                tokens.append(("RESERVADA", valor))
            else:
                tokens.append(("CONCEITO", valor))

        else:
            raise ValueError(
                f"Caráter inesperado {c!r} na posição {i}"
            )

    return tokens


if __name__ == "__main__":
    query = '''
# DBPedia: obras de Chuck Berry

select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
'''

    for tipo, valor in analisar(query):
        print(f"{tipo:12} {valor}")
