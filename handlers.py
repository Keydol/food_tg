import datetime
import pytz
import random

import settings

from telegram import Update
from telegram.ext import CallbackContext


def generate_order_message(context: CallbackContext):
    i = 0
    text = ""
    for order in context.chat_data["order"].values():
        i += 1
        text += f"{i}. {order}\n"
    return settings.message_template.format(order=text)


def edit_order_message(update: Update, context: CallbackContext):
    context.bot.edit_message_text(
        text=generate_order_message(context),
        chat_id=update.effective_chat.id,
        message_id=context.chat_data["message_id"]
    )


def add_order(update: Update, context: CallbackContext):
    context.chat_data["order"][update.effective_user.id] = update.message.text
    context.chat_data["order_people"][update.effective_user.id] = update.effective_user.first_name
    edit_order_message(update, context)


def remove_order(update: Update, context: CallbackContext):
    del context.chat_data["order"][update.effective_user.id]
    del context.chat_data["order_people"][update.effective_user.id]
    edit_order_message(update, context)


def get_chat_id(update: Update, context: CallbackContext):
    print(update._effective_chat.id)


def time_to_eat(context: CallbackContext):
    now = datetime.datetime.now().astimezone(pytz.timezone("Europe/Kiev"))
    if datetime.datetime.strftime(now, "%H:%M") == settings.time_to_eat and now.weekday() not in [4, 5, 6]:
        message = context.bot.send_message(
            text=settings.first_message,
            chat_id=settings.chat_id,
        )
        context.dispatcher.chat_data[settings.chat_id].clear()
        context.dispatcher.chat_data[settings.chat_id]["message_id"] = message.message_id
        context.dispatcher.chat_data[settings.chat_id]["order"] = {}
        context.dispatcher.chat_data[settings.chat_id]["order_people"] = {}

    if datetime.datetime.strftime(now, "%H:%M") == settings.time_to_order and now.weekday() not in [4, 5, 6]:
        order_peoples = context.dispatcher.chat_data[settings.chat_id]["order_people"]
        peoples = list(order_peoples.keys())
        user = peoples[random.randint(0, len(peoples) - 1)]
        message = context.bot.send_message(
            text=f"Сьогодні замовляє [{order_peoples[user]}](tg://user?id={user})",
            chat_id=settings.chat_id,
            parse_mode="Markdown"
        )

