from pylatexenc.latex2text import LatexNodes2Text


def covert_latex_to_text(expr):
    latex_expression = expr
    converter = LatexNodes2Text()
    plain_expression = converter.latex_to_text(latex_expression)
    return plain_expression

print(covert_latex_to_text(r"$\left(\begin{matrix}  2  & 3 \\5  & 4   \end{matrix}\right)   \left(\begin{matrix}  2  & 0  & 3 \\-1  & 1  & 5   \end{matrix}\right) $"))