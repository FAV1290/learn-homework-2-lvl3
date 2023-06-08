import random


def check_input(user_input, cities_base, used_cities, necessary_letter, mode='console'):
    if user_input == 'выход' and mode != 'bot':
        return 'exit'
    elif user_input == 'подсказка' and mode != 'bot':
        return 'need hint'
    elif user_input in used_cities:
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


def generate_answer(cities_base, answer_letter, used_cities):
    if set(cities_base[answer_letter]) - set(used_cities) == set():
        return 'no_answer'
    answer = None
    while answer is None or answer in used_cities:
        answer = random.choice(cities_base[answer_letter])
    return answer


def generate_not_ok_reaction(check_result, necessary_letter, cities_base, used_cities):
    if check_result == 'exit':
        return 'Очень жаль! До свидания'
    elif check_result == 'unknown city':
        return'Не знаю такого города! Попробуйте еще раз'
    elif check_result == 'wrong letter':
        return f'Город должен начинаться с буквы {necessary_letter.upper()}. Попробуйте еще раз'
    elif check_result == 'used city':
        return 'Этот город уже был! Попробуйте еще раз'
    elif check_result == 'need hint':
        if necessary_letter is None:
            necessary_letter = random.choice(tuple(cities_base.keys()))
        answer = generate_answer(cities_base, necessary_letter, used_cities)
        if answer == 'no_answer':
            return f'Не могу придумать городов на эту букву. Возможно, стоит сдаться?'
        else:
            return f'Как насчет города под назанием {answer.title()}?'
    

def fake_bot_failure(mode = 'user'):
    if mode == 'developer':
        return random.randint(1, 5) == 3
    else:
        return random.randint(1, 30) == 5