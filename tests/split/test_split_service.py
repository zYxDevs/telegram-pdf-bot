from typing import Iterator
from unittest.mock import patch

import pytest
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from pdf_bot.analytics import TaskType
from pdf_bot.consts import PDF_INFO
from pdf_bot.file_task import FileTaskService
from pdf_bot.pdf import PdfService
from pdf_bot.split import SplitService, split_constants
from pdf_bot.telegram import TelegramService, TelegramUserDataKeyError


@pytest.fixture(name="split_service")
def fixture_split_servicee(
    file_task_service: FileTaskService,
    pdf_service: PdfService,
    telegram_service: TelegramService,
) -> SplitService:
    return SplitService(file_task_service, pdf_service, telegram_service)


@pytest.fixture(scope="session", autouse=True)
def set_lang() -> Iterator[None]:
    with patch("pdf_bot.split.split_service.set_lang"):
        yield


@pytest.fixture(scope="session", autouse=True)
def files_set_lang() -> Iterator[None]:
    with patch("pdf_bot.files.utils.set_lang"):
        yield


@pytest.fixture(scope="session", autouse=True)
def utils_set_lang() -> Iterator[None]:
    with patch("pdf_bot.utils.set_lang"):
        yield


def test_ask_split_range(
    split_service: SplitService,
    telegram_update: Update,
    telegram_context: CallbackContext,
):
    actual = split_service.ask_split_range(telegram_update, telegram_context)
    assert actual == split_constants.WAIT_SPLIT_RANGE


def test_split_pdf(
    split_service: SplitService,
    pdf_service: PdfService,
    telegram_service: TelegramService,
    telegram_update: Update,
    telegram_context: CallbackContext,
    telegram_text: str,
):
    file_id = "file_id"
    out_path = "out_path"

    telegram_service.get_user_data.return_value = (file_id, "file_name")
    pdf_service.split_pdf.return_value.__enter__.return_value = out_path

    with patch("pdf_bot.split.split_service.send_result_file") as send_result_file:
        actual = split_service.split_pdf(telegram_update, telegram_context)

        assert actual == ConversationHandler.END
        telegram_service.get_user_data.assert_called_once_with(
            telegram_context, PDF_INFO
        )
        pdf_service.split_pdf.assert_called_once_with(file_id, telegram_text)
        send_result_file.assert_called_once_with(
            telegram_update, telegram_context, out_path, TaskType.split_pdf
        )


def test_split_pdf_invalid_split_range(
    split_service: SplitService,
    pdf_service: PdfService,
    telegram_service: TelegramService,
    telegram_update: Update,
    telegram_context: CallbackContext,
):
    file_id = "file_id"

    telegram_service.get_user_data.return_value = (file_id, "file_name")
    pdf_service.split_range_valid.return_value = False

    with patch("pdf_bot.split.split_service.send_result_file") as send_result_file:
        actual = split_service.split_pdf(telegram_update, telegram_context)

        assert actual == split_constants.WAIT_SPLIT_RANGE
        telegram_service.get_user_data.assert_not_called()
        pdf_service.split_pdf.assert_not_called()
        send_result_file.assert_not_called()


def test_split_pdf_invalid_user_data(
    split_service: SplitService,
    pdf_service: PdfService,
    telegram_service: TelegramService,
    telegram_update: Update,
    telegram_context: CallbackContext,
):
    telegram_service.get_user_data.side_effect = TelegramUserDataKeyError()
    with patch("pdf_bot.split.split_service.send_result_file") as send_result_file:
        actual = split_service.split_pdf(telegram_update, telegram_context)

        assert actual == ConversationHandler.END
        telegram_service.get_user_data.assert_called_once_with(
            telegram_context, PDF_INFO
        )
        pdf_service.split_pdf.assert_not_called()
        send_result_file.assert_not_called()
