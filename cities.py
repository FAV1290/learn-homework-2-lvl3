import cities_base as cb
import score as sc
import gameplay as gp


def main():
    cities_base = cb.create_cities_base(cb.read_cities_file('cities.txt'))
    banned_letters = set('ёйьыъ')
    savepath = 'save.txt'
    used_cities = []
    user_score = sc.load_score(savepath)
    necessary_letter = None
    user_input = None
    print("Игра началась! Введите название города, 'выход' или 'подсказка' (стоит 50 очков). Начальный счет:", user_score)
    while user_input is None or user_input != 'выход':
        user_input = input('Игрок: ').lower().strip().replace('ё', 'е')
        check_result = gp.check_input(user_input, cities_base, used_cities, necessary_letter)
        if check_result == 'ok':
            used_cities.append(user_input)
            user_score += 10
            answer_letter = gp.letter_for_next_player(user_input, banned_letters)
            answer = gp.generate_answer(cities_base, answer_letter, used_cities)
            if answer == 'no_answer' or gp.fake_bot_failure():
                print('Бот: Ничего не идет в голову. Вы меня обыграли! Ваш счет сохранен для следующей игры.')
                sc.save_score(savepath, user_score)
                break
            used_cities.append(answer)
            necessary_letter = gp.letter_for_next_player(answer, banned_letters)
            print(f'Бот: {answer.title()} (Жду город на букву {necessary_letter.upper()})')
        else:
            if check_result == 'need hint':
                user_score -= 50
            print(gp.generate_not_ok_reaction(check_result, necessary_letter, cities_base, used_cities))
    print('Бот: Вы закончили игру со счетом', user_score)


if __name__ == '__main__':
    main()
