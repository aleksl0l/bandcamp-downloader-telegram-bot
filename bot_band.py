from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import os
import shutil

count = 0
path = r'~/music/'
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Я бот, который будет скачивать музыку...")

def download_and_upload(bot, update):
    global count
    msg = update.message.text
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="Пасибо, что скачал этот прекрасный релиз!")

    # скачать
    os.system('soundscrape ' + msg + ' -p '+ path + ' -f -b')
    dirs = [dI for dI in os.listdir(path) if os.path.isdir(os.path.join(path,dI))]
    m = os.stat(path+dirs[0]).st_mtime
    direc = dirs[0]
    for d in dirs:
        if m < os.stat(path+d).st_mtime:
            m = os.stat(path+d).st_mtime
            direc = d
    print(direc)
    shutil.make_archive(path + direc, 'zip', path+direc)
    bot.send_document(chat_id=chat_id, document=open(path + direc + '.zip', 'rb'))

if __name__ == "__main__":
    with open('token', 'r') as myfile:
        token = myfile.read()
    token = token[:-1]
    updater = Updater(token=token)

    dispatcher = updater.dispatcher

    # logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    start_handler = CommandHandler('start', start)
    img_handler = MessageHandler(Filters.text, download_and_upload)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(img_handler)
    updater.start_polling()
