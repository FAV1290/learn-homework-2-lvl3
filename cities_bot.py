import logging
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


from settings import API_KEY
from constants import BANNED_LETTERS, СITIES_FILE_PATH, HINT_COST, STEP_REWARD
from cities_dict_maker import read_cities_file, create_cities_base
from gameplay import check_input, letter_for_next_player, generate_answer, generate_not_ok_reaction, fake_bot_failure


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def greet_user(update, context):
    update.message.reply_text('Привет! Я бот для игры в "города". Доступные команды:')
    update.message.reply_text('• /cities - запустить или перезапустить игру')
    update.message.reply_text('• /hint - получить подсказку (стоит 50 очков)')
    update.message.reply_text('• /score - посмотреть текущий счет')
    update.message.reply_text('• /exit - завершить игру и не начинать новую')


def start_game(update, context):
    user_id = update.message.from_user.id
    if user_id in context.bot_data and context.bot_data[user_id].get('bonus_score') is not None:
        score = context.bot_data[user_id]['bonus_score']
    else:
        score = 0
    if user_id in context.bot_data and context.bot_data[user_id].get('game_started'):
        update.message.reply_text(f"Вы закончили игру со счетом {context.bot_data[user_id]['user_score']}. А теперь начнем заново!")     
    context.bot_data[user_id] = {
        'cities_base' : create_cities_base(read_cities_file(СITIES_FILE_PATH)),
        'used_cities' : [],
        'user_score' : score,
        'necessary_letter' : None,
        'game_started' : True
    }
    score = context.bot_data[user_id]['user_score']
    update.message.reply_text(f"Игра началась! Введите название города или команду из списка. Начальный счет: {score}")


def get_hint(update, context):
    user_id = update.message.from_user.id
    if user_id not in context.bot_data or context.bot_data[user_id]['game_started'] is None:
        update.message.reply_text('Игра не запущена. Сперва начните игру командой /cities')
        return
    context.bot_data[user_id]['user_score'] -= HINT_COST
    necessary_letter = context.bot_data[user_id]['necessary_letter']
    cities_base = context.bot_data[user_id]['cities_base']
    used_cities = context.bot_data[user_id]['used_cities']
    reaction = generate_not_ok_reaction('need hint', necessary_letter, cities_base, used_cities)
    update.message.reply_text(reaction)


def show_score(update, context):
    user_id = update.message.from_user.id
    if user_id not in context.bot_data or context.bot_data[user_id]['game_started'] is None:
        update.message.reply_text('Игра не запущена. Сперва начните игру командой /cities')
    else:
        update.message.reply_text(f"Текущий счет: {context.bot_data[user_id]['user_score']}")


def cities_game(update, context):
    user_id = update.message.from_user.id
    if context.bot_data[user_id]['game_started'] is None:
        update.message.reply_text('Игра не запущена. Сперва начните игру командой /cities')
        return
    user_input = update.message.text.lower().strip().replace('ё', 'е')
    cities_base = context.bot_data[user_id]['cities_base']
    necessary_letter = context.bot_data[user_id]['necessary_letter']
    check_result = check_input(user_input, cities_base, context.bot_data[user_id]['used_cities'], necessary_letter, 'bot')
    if check_result == 'ok':
        context.bot_data[user_id]['used_cities'].append(user_input)
        context.bot_data[user_id]['user_score'] += STEP_REWARD
        answer_letter = letter_for_next_player(user_input, BANNED_LETTERS)
        answer = generate_answer(cities_base, answer_letter, context.bot_data[user_id]['used_cities'])
        if answer == 'no_answer' or fake_bot_failure():
            update.message.reply_text('Ничего не идет в голову. Вы меня обыграли! Ваш счет сохранен для следующей игры.')
            update.message.reply_text(f"Вы закончили игру со счетом {context.bot_data[user_id]['user_score']}")
            context.bot_data[user_id]['bonus_score'] = context.bot_data[user_id]['user_score']
            context.bot_data[user_id]['game_started'] = None
            return
        context.bot_data[user_id]['used_cities'].append(answer)
        necessary_letter = letter_for_next_player(answer, BANNED_LETTERS)
        context.bot_data[user_id]['necessary_letter'] = necessary_letter
        update.message.reply_text(f'{answer.title()} (Жду город на букву {necessary_letter.upper()})')
    else:
        reaction = generate_not_ok_reaction(check_result, necessary_letter, cities_base, context.bot_data[user_id]['used_cities'])
        update.message.reply_text(reaction)


def exit_game(update, context):
    user_id = update.message.from_user.id
    if user_id not in context.bot_data or context.bot_data[user_id].get('game_started') is None:
        update.message.reply_text('На данный момент игра не запущена')
    else:
        update.message.reply_text(f"Вы закончили игру со счетом {context.bot_data[user_id]['user_score']}")   
        context.bot_data[user_id]['game_started'] = None


def main():
    mybot = Updater(API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('cities', start_game))
    dp.add_handler(CommandHandler('hint', get_hint))
    dp.add_handler(CommandHandler('score', show_score))
    dp.add_handler(CommandHandler('exit', exit_game))
    dp.add_handler(MessageHandler(Filters.text, cities_game))
    logging.info(f'{datetime.datetime.now()}: Bot has started')
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
