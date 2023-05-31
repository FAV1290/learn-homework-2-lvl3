# Консольная версия будущего бота
import random


def create_cities_base(filename):
    cities_base = {}
    with open(filename, 'r', encoding='utf-8') as file_handler:
        cities = file_handler.readlines()
    for city in cities:
        city_first_letter = city.lower().strip()[0]
        if cities_base.get(city_first_letter) is None:
            cities_base[city_first_letter] = [city.lower().strip(),]
        else:
            cities_base[city_first_letter].append(city.lower().strip())
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
    if word[-1] in banned_letters and word[-2] in banned_letters:
        return word[-3]
    elif word[-1] in banned_letters:
        return word[-2]
    else:
        return word[-1]


def generate_bot_answer(cities_base, answer_letter, used_cities):
    answer = None
    while answer is None or answer in used_cities:
        random_city_number = random.randint(0, len(cities_base[answer_letter]) - 1)
        answer = cities_base[answer_letter][random_city_number]
    return answer


def main():
    cities_base = create_cities_base('cities.txt')
    banned_letters = ('ё', 'ь', 'ы', 'ъ', 'й')
    used_cities = []
    necessary_letter = None
    user_input = None
    print('Игра началась! Введите название города или Выход для завершения игры')
    while user_input is None or user_input != 'выход':
        user_input = input('Игрок: ').lower().strip()
        check_result = check_input(user_input, cities_base, used_cities, necessary_letter)
        if check_result == 'exit':
            print('Бот: Очень жаль! До свидания')
        elif check_result == 'unknown city':
            print('Бот: Не знаю такого города! Попробуйте еще раз')
        elif check_result == 'wrong letter':
            print(f'Бот: Город должен начинаться с буквы {necessary_letter.upper()}. Попробуйте еще раз')
        elif check_result == 'used city':
            print('Бот: Этот город уже был! Попробуйте еще раз')
        else:
            used_cities.append(user_input)
            answer_letter = letter_for_next_player(user_input, banned_letters)
            answer = generate_bot_answer(cities_base, answer_letter, used_cities)
            used_cities.append(answer)
            necessary_letter = letter_for_next_player(answer, banned_letters) 
            print(f'Бот: {answer.capitalize()} (Ваш город должен начинаться с буквы {necessary_letter.upper()})')


# Далее:
# - Добавить принт по исчерпании ботом слов для ответа (мало ли)
# - Оставить большие буквы в пробельных и дефисных городах (как в базе)
# - Перенести в Telegram
# - Добавить возможность одновременной игры разными игроками
# - Добавить юзер скор (и таблицу рекордов)
# - Добавить города СНГ и прочих стран


if __name__ == '__main__':
    main()
