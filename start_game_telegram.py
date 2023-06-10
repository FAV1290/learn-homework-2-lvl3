import logging
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import API_KEY
from cities_game import greet_user, start_game, format_input, get_hint, make_turn


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def print_greetings(update, context):
    update.message.reply_text('Привет! Я бот для игры в "города". Доступные команды:')
    update.message.reply_text('\n'.join(greet_user()))


def start_handler(update, context):
    my = context.user_data.get
    start_result = start_game(my('game_started', False), my('user_score', 0), my('bonus_score', 0))
    context.user_data.update(start_result['parameters'])
    update.message.reply_text(start_result['reaction'])


def exit_game(update, context):
    if not context.user_data.get('game_started', False):
        update.message.reply_text('На данный момент игра не запущена')
    else:
        update.message.reply_text(f"Вы закончили игру со счетом {context.user_data['user_score']}")   
        context.user_data['game_started'] = None


def hint_handler(update, context):
    if not context.user_data.get('game_started', False):
        update.message.reply_text('Игра не запущена. Сперва начните игру командой /cities')
    else:
        hint_result = get_hint(context.user_data)
        context.user_data['user_score'] = hint_result['score']
        update.message.reply_text(hint_result['reaction'])


def show_score(update, context):
    if not context.user_data.get('game_started', False):
        update.message.reply_text('Игра не запущена. Сперва начните игру командой /cities')
    else:
        update.message.reply_text(f"У вас {context.user_data['user_score']} очков")


def turn_handler(update, context):
    if not context.user_data.get('game_started', False):
        update.message.reply_text('Игра не запущена. Сперва начните игру командой /cities')
    else:
        user_input = format_input(update.message.text)
        turn_result = make_turn(context.user_data, user_input)
        context.user_data.update(turn_result['parameters'])
        update.message.reply_text(turn_result['reaction'])
    if not context.user_data.get('game_started', False):
        update.message.reply_text(f"Вы закончили игру со счетом {context.user_data['user_score']}") 


def main():
    mybot = Updater(API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', print_greetings))
    dp.add_handler(CommandHandler('cities', start_handler))
    dp.add_handler(CommandHandler('hint', hint_handler))
    dp.add_handler(CommandHandler('score', show_score))
    dp.add_handler(CommandHandler('exit', exit_game))
    dp.add_handler(MessageHandler(Filters.text, turn_handler))
    logging.info(f'{datetime.datetime.now()}: Bot has started')
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()