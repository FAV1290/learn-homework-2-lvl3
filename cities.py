from cities_dict_maker import read_cities_file, create_cities_base
from score import save_score, load_score
from gameplay import check_input, letter_for_next_player, generate_answer, generate_not_ok_reaction, fake_bot_failure
from constants import SAVEPATH, BANNED_LETTERS, СITIES_FILE_PATH


def main():
    cities_base = create_cities_base(read_cities_file(СITIES_FILE_PATH))
    used_cities = []
    user_score = load_score(SAVEPATH)
    necessary_letter = None
    user_input = None    
    print("Игра началась! Введите название города, 'выход' или 'подсказка' (стоит 50 очков). Начальный счет:", user_score)
    while user_input is None or user_input != 'выход':
        user_input = input('Игрок: ').lower().strip().replace('ё', 'е')
        check_result = check_input(user_input, cities_base, used_cities, necessary_letter)
        if check_result == 'ok':
            used_cities.append(user_input)
            user_score += 10
            answer_letter = letter_for_next_player(user_input, BANNED_LETTERS)
            answer = generate_answer(cities_base, answer_letter, used_cities)
            if answer == 'no_answer' or fake_bot_failure('developer'):
                print('Бот: Ничего не идет в голову. Вы меня обыграли! Ваш счет сохранен для следующей игры.')
                save_score(SAVEPATH, user_score)
                break
            used_cities.append(answer)
            necessary_letter = letter_for_next_player(answer, BANNED_LETTERS)
            print(f'Бот: {answer.title()} (Жду город на букву {necessary_letter.upper()})')
        else:
            if check_result == 'need hint':
                user_score -= 50
            print(f'Бот: {generate_not_ok_reaction(check_result, necessary_letter, cities_base, used_cities)}')
    print('Бот: Вы закончили игру со счетом', user_score)


if __name__ == '__main__':
    main()
