from django.core.management import BaseCommand
from telebot import TeleBot, types
from core.settings import BOT_TOKEN


bot = TeleBot(token=BOT_TOKEN)


@bot.channel_post_handler()
def command_start(message: types.Message):
    print(message)


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('bot is running')
        bot.polling(none_stop=True)