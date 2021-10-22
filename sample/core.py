import logging

from updater import ChessRatingUpdater

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    updater = ChessRatingUpdater()
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
