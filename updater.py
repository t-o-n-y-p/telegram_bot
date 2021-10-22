import datetime

from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext, Updater, CommandHandler, CallbackQueryHandler

from container import RatingContainer
from tgtoken import TOKEN


def _build_markup(button_rows):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text, callback_data=callback_data) for text, callback_data in button_row]
        for button_row in button_rows
    ])


class ChessRatingUpdater(Updater):
    @staticmethod
    def _build_markup_310(button_rows):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text, callback_data=callback_data) for text, callback_data in button_row]
            for button_row in button_rows
        ])

    _rating_container = RatingContainer()
    _invitation_text = 'Select rating type below.'
    _error_text = 'Something went wrong. Please try again later or select other rating type.'
    _reply_markup = _build_markup(
        [
            [('Classic', 'open'), ('Women classic', 'women')],
            [('Rapid', 'men_rapid'), ('Women rapid', 'women_rapid')],
            [('Blitz', 'men_blitz'), ('Women blitz', 'women_blitz')]
        ]
    )

    def __init__(self):
        super().__init__(TOKEN, use_context=True)
        self.dispatcher.add_handler(CommandHandler('start', self._start_command))
        self.dispatcher.add_handler(CallbackQueryHandler(self._button))
        self.job_queue.run_daily(
            self._update_ratings,
            time=datetime.time(hour=0, minute=0)
        )

    def _start_command(self, update: Update, context: CallbackContext):
        context.bot.send_message(
            text=self._invitation_text,
            chat_id=update.effective_chat.id,
            reply_markup=self._reply_markup
        )

    def _button(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        context.bot.send_message(
            text=f'{self._rating_container.get(query.data, self._error_text)}\n\n{self._invitation_text}',
            chat_id=update.effective_chat.id,
            reply_markup=self._reply_markup
        )

    def _update_ratings(self, context):
        try:
            self._rating_container.update_ratings()
        except:
            pass    # not to crash the bot if something happened
