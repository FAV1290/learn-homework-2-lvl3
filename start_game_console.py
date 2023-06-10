from save_load import save_score, load_score
from constants import SAVEPATH, COMMANDS
from cities_game import greet_user, start_game, format_input, get_hint, make_turn


def print_greetings():
    print('Бот: Привет! Я бот для игры в "города". Доступные команды:')
    print('\n'.join(greet_user()))


def start_handler(game_started, last_score, bonus_score):
    parameters, reaction = start_game(game_started, last_score, bonus_score).values()
    return parameters, reaction


def command_handler(parameters, user_input):
    if user_input == '/exit':
        reaction = 'Очень жаль! До свидания'
        parameters['game_started'] = False
    elif user_input == '/hint':
        parameters['user_score'], reaction = get_hint(parameters).values()
    elif user_input == '/score':
       reaction = f"У вас {parameters['user_score']} очков"
    elif user_input == '/cities':
        parameters, reaction = start_handler(True, parameters['user_score'], 0)
    return parameters, reaction


def main():
    print_greetings()
    print()
    parameters, reaction = start_handler(False, 0, load_score(SAVEPATH))
    print(f"Бот: {reaction}")
    while parameters['game_started']:
        user_input = format_input(input('Игрок: '))
        if user_input in COMMANDS.keys():
            parameters, reaction = command_handler(parameters, user_input)
        else:
            parameters, reaction = make_turn(parameters, user_input).values()
        print(f"Бот: {reaction}")
    save_score(SAVEPATH, parameters['bonus_score'])
    print(f"Бот: Вы закончили игру со счетом {parameters['user_score']}")


if __name__ == "__main__":
    main()
    