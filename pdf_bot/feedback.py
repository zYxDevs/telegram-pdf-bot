import os

from dotenv import load_dotenv
from langdetect import detect
from loguru import logger
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from telegram import ChatAction, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
)

from pdf_bot.consts import CANCEL, TEXT_FILTER
from pdf_bot.language import set_lang
from pdf_bot.utils import cancel, reply_with_cancel_btn

load_dotenv()
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

slack_client = WebClient(SLACK_TOKEN)


def feedback_cov_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("feedback", feedback)],
        states={0: [MessageHandler(TEXT_FILTER, check_text)]},
        fallbacks=[CommandHandler("cancel", cancel)],
        run_async=True,
    )


def feedback(update: Update, context: CallbackContext) -> int:
    """
    Start the feedback conversation
    Args:
        update: the update object
        context: the context object

    Returns:
        The variable indicating to wait for feedback
    """
    _ = set_lang(update, context)
    text = _(
        "Send me your feedback (only English feedback will be "
        "forwarded to my developer)"
    )
    reply_with_cancel_btn(update, context, text)

    return 0


def check_text(update: Update, context: CallbackContext) -> int:
    update.effective_message.chat.send_action(ChatAction.TYPING)
    _ = set_lang(update, context)
    if update.effective_message.text == _(CANCEL):
        return cancel(update, context)

    return receive_feedback(update, context)


def receive_feedback(update: Update, context: CallbackContext) -> int:
    message = update.effective_message
    feedback_msg = message.text
    feedback_lang = detect(feedback_msg)  # pylint: disable=no-member

    _ = set_lang(update, context)
    if feedback_lang.lower() == "en":
        try:
            text = (
                f"Feedback received from @{message.chat.username} "
                f"({message.chat.id}):\n\n{feedback_msg}"
            )
            slack_client.chat_postMessage(channel="#pdf-bot-feedback", text=text)
        except SlackApiError:
            logger.exception("Failed to send feedback to Slack")

        message.reply_text(
            _("Thank you for your feedback, I've already forwarded it to my developer")
        )
        return ConversationHandler.END

    message.reply_text(_("The feedback is not in English, try again"))
    return 0
