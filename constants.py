from cities_dict_maker import read_cities_file, create_cities_base


СITIES_FILE_PATH = 'cities.txt'
CITIES_BASE = create_cities_base(read_cities_file(СITIES_FILE_PATH))
SAVEPATH = 'save.txt'
BANNED_LETTERS = set('ёйьыъ')
HINT_COST = 50
STEP_REWARD = 10
FAKE_FAILURE_CHANCE = 5
COMMANDS = {
    '/exit' : f'• /cities - запустить или перезапустить игру',
    '/hint' : f'• /hint - получить подсказку (стоит {HINT_COST} очков)',
    '/score' : f'• /score - посмотреть текущий счет',
    '/cities' : f'• /exit - завершить игру и не начинать новую', 
}