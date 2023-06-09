from save_load import save_score, load_score
from constants import SAVEPATH, COMMANDS
from cities_game import greet_user, get_start_parameters, formatted_input, get_hint, next_turn


def print_greetings():
    print('Бот: Привет! Я бот для игры в "города". Доступные команды:')
    print('\n'.join(greet_user()))


def start_handler(game_started, last_score, bonus_score):
    parameters = get_start_parameters(game_started, last_score, bonus_score)
    return parameters


def command_handler(parameters, user_input):
    if user_input == '/exit':
        parameters['reaction'] = 'Бот: Очень жаль! До свидания'
        parameters['game_started'] = None
    elif user_input == '/hint':
        parameters = get_hint(parameters)
    elif user_input == '/score':
       parameters['reaction'] = f"Бот: У вас {parameters['user_score']} очков"
    elif user_input == '/cities':
        parameters = start_handler(1, parameters['user_score'], 0)
    return parameters


def main():
    print_greetings()
    print()
    parameters = start_handler(0, 0, load_score(SAVEPATH))
    print(f"Бот: {parameters.pop('reaction')}")
    while parameters['game_started']:
        user_input = formatted_input(input('Игрок: '))
        if user_input in COMMANDS.keys():
            parameters = command_handler(parameters, user_input)
        else:
            parameters = next_turn(parameters, user_input)
        print(f"Бот: {parameters.pop('reaction')}")
    save_score(SAVEPATH, parameters['bonus_score'])
    print(f"Бот: Вы закончили игру со счетом {parameters['user_score']}")


if __name__ == "__main__":
    main()
    