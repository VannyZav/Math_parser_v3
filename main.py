import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from itertools import zip_longest

from converter import normalize_exp

driver = webdriver.Chrome()
mathsolver_link = 'https://mathsolver.microsoft.com/ru/solve-problem/'


'''ввод задачи на сайте'''
def input_task(some_task):
    driver.get('https://mathsolver.microsoft.com/ru/solve-problem/')
    input_box = driver.find_element(By.CSS_SELECTOR, '#rif')
    input_box.send_keys(some_task)
    button = driver.find_element(By.CSS_SELECTOR, "#main > main > div:nth-child(1) > div.MathInputField_gfc__NY_r1 > button")
    button.click()
    time.sleep(2)
    return driver.current_url

'''конвертируем в словарь '''
def convert_to_answer_dict(title_, comment_list_, element_list_):
    answers = {}
    answers_list = []
    for el, com in zip_longest(element_list_, comment_list_):
        # answers = {}
        answers_list.append(f'$${el}$$\n')
        if com is not None:
            if 'x' in com:
                com = com.replace('x', '$x$')
            answers_list.append(f'{com}<br>\n')
        answers['method'] = title_
        answers['solution'] = answers_list
    # print(answers)
    return answers


'''поиск блока с кнопками-вариантами-ответа'''
def get_answer_block(link_with_input_task):
    driver.get(link_with_input_task)
    try:
        answer_block = driver.find_element(By.CSS_SELECTOR, "#main > main > div.c > div.c0 > div > div > \
                                                       div.ResultsWithLoading_resultsContainer__4MLRD > \
                                                       div.Answer_card__M9PzT.Answer_m__PN_fJ > \
                                                       div.ms-FocusZone.server-css-17 > div")
        # print('answer_block:', answer_block)
        return answer_block
    except Exception as e:
        pass


'''получение кнопок-вариантов-ответа'''
def get_buttons(block):
    try:
        bttns = block.find_elements(By.TAG_NAME, 'button')
        return bttns
    except Exception as e:
        print('error: нету кнопок', e)


def get_many_answers(list_of_buttons):
    answers_list = []
    for btn in list_of_buttons:
        elem_list = []
        comm_list = []
        title = btn.get_attribute('title')
        # print('\n\nвариант решения:', title)
        btn.click()
        elements_classe = driver.find_elements(By.CLASS_NAME, "Step_step__B9mau ")
        comment_classes = driver.find_elements(By.CLASS_NAME, "Step_stepPreviewContent__scxab")

        for i in elements_classe:

            elem = i.find_element(By.CLASS_NAME, "hidden").get_attribute('innerHTML').replace(" <!-- -->", '')
            elem_list.append(elem)

        # print("список элементов:", elem_list)

        for n in comment_classes:

            comment = n.find_element(By.CLASS_NAME, "hidden").get_attribute('innerHTML').replace(" <!-- -->", '')
            comm_list.append(comment)

        # print("список комментариев:", comm_list)
        dict_answ = convert_to_answer_dict(title, comm_list, elem_list)
        answers_list.append(dict_answ)
    # print(answers_list)
    return answers_list #dict_answ


def get_one_answer(link):
    elem_list = []
    comm_list = []
    driver.get(link)
    elements_classe = driver.find_elements(By.CLASS_NAME, "Step_step__B9mau ")
    comment_classes = driver.find_elements(By.CLASS_NAME, "Step_stepPreviewContent__scxab")
    title = driver.find_element(By.CSS_SELECTOR, '#main > main > div.c > div.c0 > div > div > \
    div.ResultsWithLoading_resultsContainer__4MLRD > div.Answer_card__M9PzT.Answer_m__PN_fJ > div:nth-child(4) \
    > div > div.Steps_title__rIykW > div').get_attribute('innerHTML')

    # print('\n\nвариант решения:', title)
    for i in elements_classe:
        elem = i.find_element(By.CLASS_NAME, "hidden").get_attribute('innerHTML').replace(" <!-- -->", '')
        elem_list.append(elem)
    # print("список элементов:", elem_list)
    for n in comment_classes:
        comment = n.find_element(By.CLASS_NAME, "hidden").get_attribute('innerHTML').replace(" <!-- -->", '')
        comm_list.append(comment)
    # print("список комментариев:", comm_list)

    _one_answer = convert_to_answer_dict(title, comm_list, elem_list)
    return _one_answer

def main(task_):
    task = normalize_exp(task_)

    main_answer = {}
    '''вбиваем задачу'''
    link_with_task = input_task(task)
    '''получаем блок с кнопками ответов если он есть'''
    block = get_answer_block(link_with_task)

    if block:
        '''получаем кнопки'''
        buttons = get_buttons(block)
        '''получение нескольких ответов'''
        answers_list = get_many_answers(buttons)
        main_answer['equation'] = task
        main_answer['vars_of_solutions'] = answers_list
        print("\n", main_answer)

    if not block:
        one_answer = get_one_answer(link_with_task)
        main_answer['equation'] = task
        main_answer.update(one_answer)
        print("\n", main_answer)


# task_with_one_answer = 'x+3x = 0' or 'x/4)=1'
# task_with_many_answer = 'x^2)-3x+2=0'
# try:
main(r'\frac{1}{2} - \frac{1}{3} - x^{2} = 0')

# except Exception:
#     print('некорректно подан пример')

#
# task = 'x^2)-3x+2=0'
# '''вбиваем задачу'''
# link_with_task = input_task(task)
# '''получаем блок с кнопками ответов если он есть'''
# block = get_answer_block(link_with_task)
# '''получаем кнопки'''
# buttons = get_buttons(block)
# '''получение нескольких ответов'''
# answers_dict = get_many_answers(buttons)


# expected_answer = {
#     "equation": 'x/4)=1',
#     "Варианты решения": [
#         {
#             "method": "первый метод",
#             "solution": ['первое решение']
#         },
#         {
#             "method": "второй метод",
#             "solution": ['второе решение']
#         }
#     ]
# }
