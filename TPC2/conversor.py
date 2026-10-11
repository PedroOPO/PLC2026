
import re


def converter_inline(texto):
    # Converter imagens
    texto = re.sub(
        r"!\[(.+?)\]\((.+?)\)",
        r'<img src="\2" alt="\1"/>',
        texto
    )

    # Converter links
    texto = re.sub(
        r"\[(.+?)\]\((.+?)\)",
        r'<a href="\2">\1</a>',
        texto
    )

    # Converter negrito
    texto = re.sub(
        r"\*\*(.+?)\*\*",
        r"<b>\1</b>",
        texto
    )

    # Converter itálico
    texto = re.sub(
        r"\*(.+?)\*",
        r"<i>\1</i>",
        texto
    )

    return texto


def markdown_para_html(texto):
    linhas = texto.split("\n")
    resultado = []
    dentro_lista = False

    for linha in linhas:

        # Verificar se a linha é um item de lista numerada
        item_lista = re.match(r"^\s*\d+\.\s+(.+)$", linha)

        if item_lista:

            # Abrir a lista, se ainda não estiver aberta
            if not dentro_lista:
                resultado.append("<ol>")
                dentro_lista = True

            # Converter o conteúdo do item
            item = converter_inline(item_lista.group(1))
            resultado.append(f"<li>{item}</li>")

        else:

            # Fechar a lista quando encontramos outra linha
            if dentro_lista:
                resultado.append("</ol>")
                dentro_lista = False

            # Verificar se a linha é um cabeçalho
            cabecalho = re.match(r"^(#{1,3}) (.+)$", linha)

            if cabecalho:
                nivel = len(cabecalho.group(1))
                titulo = converter_inline(cabecalho.group(2))
                linha = f"<h{nivel}>{titulo}</h{nivel}>"

            else:
                linha = converter_inline(linha)

            resultado.append(linha)

    # Fechar a lista se o texto terminar dentro dela
    if dentro_lista:
        resultado.append("</ol>")

    return "\n".join(resultado)


if __name__ == "__main__":

    teste = """# Título
## Subtítulo
### Secção

Texto com **negrito** e *itálico*.

Como pode ser consultado em [página da UC](http://www.uc.pt).

Como se vê na imagem seguinte: ![imagem dum coelho](http://www.coellho.com)

1. Primeiro item
2. Segundo item
3. Terceiro item

Texto depois da lista."""

    print(markdown_para_html(teste))

