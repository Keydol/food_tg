import settings
from handlers import add_order, remove_order, time_to_eat

from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    PicklePersistence,
    Updater,
)


def main():
    persistence = PicklePersistence(filename="food_persistence")
    updater = Updater(token=settings.BOT_TOKEN, persistence=persistence)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(filters=(Filters.reply & Filters.text), callback=add_order))
    dispatcher.add_handler(CommandHandler("cancel", remove_order))

    job_queue = updater.job_queue
    job_queue.run_repeating(time_to_eat, interval=60, first=0)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
