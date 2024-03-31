import re

from pylatexenc.latex2text import LatexNodes2Text

'''функция конвертации из латекса в текст'''


def covert_latex_to_text(expr):
    latex_expression = expr
    converter = LatexNodes2Text()
    plain_expression = converter.latex_to_text(latex_expression)
    print("конвертирую из латекса в текст:", plain_expression)
    return plain_expression


'''функция для записи квадратного корня'''


def insert_caret_and_bracket(expression):
    pattern = r'([a-zA-Z]\^\d)'
    matches = re.finditer(pattern, expression)

    new_expression = expression
    offset = 0
    for match in matches:
        start, end = match.span()
        new_expression = new_expression[:end + offset] + ')' + new_expression[end + offset:]
        offset += 1

    new_expression = new_expression.replace('-', '-')  # Заменяем русские "-" на англ. "-"
    print("добавляю скобку после степени", new_expression)
    return new_expression


# print(insert_caret_and_bracket('x^2-5=0'))

#
# def add_bracket_after_denominator(expression):
#     pattern = r'(\d+)/(\d+)'
#     matches = re.finditer(pattern, expression)
#
#     new_expression = expression
#     offset = 0
#     for match in matches:
#         start, end = match.span()
#         new_expression = new_expression[:end + offset] + ')' + new_expression[end + offset:]
#         offset += 1
#     print("добавляю скобку после знаменателя", new_expression)
#     return new_expression
def add_bracket_after_denominator(expression):
    pattern = r'(\w+)/(\d+)'
    new_expression = re.sub(pattern, r'\1/\2)', expression)
    print("добавляю скобку после числа, на которое делится первое число:", new_expression)
    return new_expression
#
# input_expression = "x/4 = 0"
# output_expression = add_bracket_after_denominator(input_expression)


# print(output_expression)


def normalize_exp(exp_):
    text_exp = covert_latex_to_text(exp_)
    if '^' in text_exp:
        text_exp = insert_caret_and_bracket(text_exp)
    if "/" in text_exp:
        text_exp = add_bracket_after_denominator(text_exp)


    return text_exp
