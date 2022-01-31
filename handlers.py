import datetime
import pytz

import settings

from telegram import Update
from telegram.ext import CallbackContext


def generate_order_message(context: CallbackContext):
    i = 0
    text = ""
    for user, order in context.chat_data["order"].items():
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
    if update.effective_message.reply_to_message.text.startswith("Нове"):
        for key in context.chat_data.copy().keys():
            del context.chat_data[key]
        context.chat_data["message_id"] = update.effective_message.reply_to_message.message_id
        context.chat_data["order"] = {}
    context.chat_data["order"][update.effective_user.id] = update.message.text
    edit_order_message(update, context)


def remove_order(update: Update, context: CallbackContext):
    del context.chat_data["order"][update.effective_user.id]
    edit_order_message(update, context)


def time_to_eat(context: CallbackContext):
    now = datetime.datetime.now().astimezone(pytz.timezone("Europe/Kiev"))
    if datetime.datetime.strftime(now, "%H:%M") == settings.time_to_eat and now.weekday() not in [5, 6]:
        context.bot.send_message(
            text="Нове замовлення\n\nРеплай на повідомлення - добавити своє замовлення",
            chat_id=settings.chat_id,
        )
