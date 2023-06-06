import random


def read_cities_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file_handler:
        cities_list = file_handler.readlines()
    return cities_list


def create_cities_base(cities_list):
    cities_base = {}
    for city in cities_list:
        city = city.lower().strip()
        if cities_base.get(city[0]) is None:
            cities_base[city[0]] = [city]
        else:
            cities_base[city[0]].append(city)
    return cities_base


def check_input(user_input, cities_base, used_cities, necessary_letter):
    if user_input == 'выход':
        return 'exit'
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


def generate_bot_answer(cities_base, answer_letter, used_cities):
    if set(cities_base[answer_letter]) - set(used_cities) == set():
        return 'bot_failed'
    answer = None
    while answer is None or answer in used_cities:
        answer = random.choice(cities_base[answer_letter])
    return answer


def generate_not_ok_reaction(check_result, necessary_letter):
    if check_result == 'exit':
        return 'Бот: Очень жаль! До свидания'
    elif check_result == 'unknown city':
        return'Бот: Не знаю такого города! Попробуйте еще раз'
    elif check_result == 'wrong letter':
        return f'Бот: Город должен начинаться с буквы {necessary_letter.upper()}. Попробуйте еще раз'
    elif check_result == 'used city':
        return 'Бот: Этот город уже был! Попробуйте еще раз'


def main():
    cities_list = read_cities_file('cities.txt') 
    cities_base = create_cities_base(cities_list)
    banned_letters = set('ёйьыъ')
    used_cities = []
    necessary_letter = None
    user_input = None
    print("Игра началась! Введите название города или 'выход' для завершения игры")
    while user_input is None or user_input != 'выход':
        user_input = input('Игрок: ').lower().strip()
        check_result = check_input(user_input, cities_base, used_cities, necessary_letter)
        if check_result == 'ok':
            used_cities.append(user_input)
            answer_letter = letter_for_next_player(user_input, banned_letters)
            answer = generate_bot_answer(cities_base, answer_letter, used_cities)
            if answer == 'bot_failed' or random.randint(0, 100) == 5:   # real or fake bot failure
                print('Бот: Ничего не идет в голову. Вы меня обыграли!')
                break
            used_cities.append(answer)
            necessary_letter = letter_for_next_player(answer, banned_letters) 
            print(f'Бот: {answer.capitalize()} (Жду город на букву {necessary_letter.upper()})')
        else:
            print(generate_not_ok_reaction(check_result, necessary_letter))


# Далее:
# - Оставить большие буквы в пробельных и дефисных городах (как в базе)
# - Добавить юзер скор (и таблицу рекордов)
# - Определиться с буквой 'ё'
# - Перенести в Telegram
# - Добавить возможность одновременной игры разными игроками
# - Добавить крупные города Европы, США, Азии, Австралии


if __name__ == '__main__':
    main()
