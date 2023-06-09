import random
from constants import BANNED_LETTERS, CITIES_BASE, HINT_COST, STEP_REWARD, FAKE_FAILURE_CHANCE, COMMANDS


def greet_user():
    return list(COMMANDS.values())


def get_start_parameters(game_started, last_score, bonus_score):
    parameters = {
        'used_cities' : [],
        'user_score': bonus_score,
        'necessary_letter' : None,
        'game_started' : True,
        'bonus_score': 0
    }
    parameters['reaction'] = f"Введите город или команду из списка. Начальный счет: {parameters['user_score']}"
    if game_started:
        parameters['reaction'] = f'Вы закончили игру со счетом {last_score}. А теперь начнем заново! \n' + parameters['reaction']
    return parameters


def formatted_input(user_input):
    return user_input.lower().strip().replace('ё', 'е')


def generate_answer(cities_base, answer_letter, used_cities):
    if set(cities_base[answer_letter]) - set(used_cities) == set():
        return 'no_answer'
    answer = None
    while answer is None or answer in used_cities:
        answer = random.choice(cities_base[answer_letter])
    return answer


def get_hint(parameters):
        if parameters['necessary_letter'] is None:
            necessary_letter = random.choice(tuple(CITIES_BASE.keys()))
        else:
            necessary_letter = parameters['necessary_letter']
        answer = generate_answer(CITIES_BASE, necessary_letter, parameters['used_cities'])
        if answer == 'no_answer':
            parameters['reaction'] = f'Не могу придумать городов на эту букву. Возможно, стоит сдаться?'
        else:
            parameters['user_score'] -= HINT_COST
            parameters['reaction'] = f'Как насчет города под названием {answer.title()}?'
        return parameters


def check_input(user_input, cities_base, used_cities, necessary_letter):
    if user_input in used_cities:
        return 'used city'
    elif necessary_letter is not None and necessary_letter != user_input[0]:
        return 'wrong letter'
    elif user_input not in cities_base[user_input[0]]:
        return 'unknown city'
    else:
        return 'ok'
    

def letter_for_next_player(word, banned_letters):
    for letter in reversed(word):
        if letter not in banned_letters:
            return letter    


def generate_not_ok_reaction(check_result, necessary_letter):
    if check_result == 'unknown city':
        return 'Не знаю такого города! Попробуйте еще раз'
    elif check_result == 'wrong letter':
        return f'Город должен начинаться с буквы {necessary_letter.upper()}. Попробуйте еще раз'
    elif check_result == 'used city':
        return 'Этот город уже был! Попробуйте еще раз'


def fake_bot_failure():
    return random.randint(1, 100) in range(1, FAKE_FAILURE_CHANCE + 1)


def next_turn(parameters, user_input):
    check_result = check_input(user_input, CITIES_BASE, parameters['used_cities'], parameters['necessary_letter'])
    if check_result == 'ok':
        parameters['used_cities'].append(user_input)
        parameters['user_score'] += STEP_REWARD
        answer_letter = letter_for_next_player(user_input, BANNED_LETTERS)
        answer = generate_answer(CITIES_BASE, answer_letter, parameters['used_cities'])
        if answer == 'no_answer' or fake_bot_failure():
            parameters['reaction'] = 'Ничего не идет в голову. Вы меня обыграли! Ваш счет сохранен для следующей игры.'
            parameters['bonus_score'] = parameters['user_score']
            parameters['game_started'] = None
        else:
            parameters['used_cities'].append(answer)
            parameters['necessary_letter'] = letter_for_next_player(answer, BANNED_LETTERS)
            parameters['reaction'] = f"{answer.title()} (Жду город на букву {parameters['necessary_letter'].upper()})"
    else:
        parameters['reaction'] = generate_not_ok_reaction(check_result, parameters['necessary_letter'])
    return parameters
