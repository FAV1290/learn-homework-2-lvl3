import logging
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import API_KEY
from cities_game import greet_user, get_start_parameters, formatted_input, get_hint, next_turn


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def print_greetings(update, context):
    update.message.reply_text('Привет! Я бот для игры в "города". Доступные команды:')
    update.message.reply_text('\n'.join(greet_user()))


def start_handler(update, context):
    user_id = update.message.from_user.id
    if user_id not in context.bot_data:
        context.bot_data[user_id] = get_start_parameters(0, 0, 0)
    else:
        my = context.bot_data[user_id]
        context.bot_data[user_id] = get_start_parameters(my['game_started'], my['user_score'], my['bonus_score'])
    update.message.reply_text(context.bot_data[user_id].pop('reaction'))


def exit_game(update, context):
    user_id = update.message.from_user.id
    if user_id not in context.bot_data or context.bot_data[user_id].get('game_started') is None:
        update.message.reply_text('На данный момент игра не запущена')
    else:
        update.message.reply_text(f"Вы закончили игру со счетом {context.bot_data[user_id]['user_score']}")   
        context.bot_data[user_id]['game_started'] = None


def hint_handler(update, context):
    user_id = update.message.from_user.id
    if user_id not in context.bot_data or context.bot_data[user_id]['game_started'] is None:
        update.message.reply_text('Игра не запущена. Сперва начните игру командой /cities')
        return
    context.bot_data[user_id] = get_hint(context.bot_data[user_id])
    update.message.reply_text(context.bot_data[user_id].pop('reaction'))


def show_score(update, context):
    user_id = update.message.from_user.id
    if user_id not in context.bot_data or context.bot_data[user_id]['game_started'] is None:
        update.message.reply_text('Игра не запущена. Сперва начните игру командой /cities')
    else:
        update.message.reply_text(f"У вас {context.bot_data[user_id]['user_score']} очков")


def next_turn_handler(update, context):
    user_id = update.message.from_user.id
    if user_id not in context.bot_data or context.bot_data[user_id]['game_started'] is None:
        update.message.reply_text('Игра не запущена. Сперва начните игру командой /cities')
    else:
        user_input = formatted_input(update.message.text)
        context.bot_data[user_id] = next_turn(context.bot_data[user_id], user_input)
        update.message.reply_text(context.bot_data[user_id].pop('reaction'))
    if context.bot_data[user_id]['game_started'] is None:
        update.message.reply_text(f"Вы закончили игру со счетом {context.bot_data[user_id]['user_score']}") 


def main():
    mybot = Updater(API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', print_greetings))
    dp.add_handler(CommandHandler('cities', start_handler))
    dp.add_handler(CommandHandler('hint', hint_handler))
    dp.add_handler(CommandHandler('score', show_score))
    dp.add_handler(CommandHandler('exit', exit_game))
    dp.add_handler(MessageHandler(Filters.text, next_turn_handler))
    logging.info(f'{datetime.datetime.now()}: Bot has started')
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()