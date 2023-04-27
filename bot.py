import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import TELEGRAM_BOT_TOKEN_, YOUTUBE_API_KEY_

TELEGRAM_BOT_TOKEN = TELEGRAM_BOT_TOKEN_
YOUTUBE_API_KEY = YOUTUBE_API_KEY_

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def search_video_on_youtube(query):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    try:
        response = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=1,
            type='video'
        ).execute()

        video = response['items'][0]
        video_id = video['id']['videoId']
        video_title = video['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={video_id}'

        return video_title, video_url
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')
        return None, None

def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Сгенерировать новую передачу", callback_data='generate')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Нажмите кнопку ниже, чтобы сгенерировать случайную передачу "kargin haghordum sketch".', reply_markup=reply_markup)


def generate_video(update: Update, context: CallbackContext):
    query_data = update.callback_query.data
    if query_data == 'generate':
        random_number = random.randint(1, 700)
        query = f'kargin haghordum sketch {random_number}'
        video_title, video_url = search_video_on_youtube(query)

        if video_url:
            update.callback_query.message.reply_text(f'{video_title}\n{video_url}')


def error(update: Update, context: CallbackContext):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(generate_video))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
