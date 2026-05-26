import asyncio
import random
import time

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, User

from src.modules.captcha import strings
from src.modules.captcha.service import CaptchaService
from src.modules.captcha.types import CAPTCHA_OUTDATED_TIMEOUT, JoinOutcome
from src.modules.chats.service import ChatsService


class CaptchaBotConnector:
    def __init__(
        self,
        service: CaptchaService,
        chats: ChatsService,
        challenge_time: int,
    ) -> None:
        self._service = service
        self._chats = chats
        self._challenge_time = challenge_time

    def register(self, bot: AsyncTeleBot) -> None:
        bot.register_message_handler(
            self._handle_left_member,  # pyright: ignore[reportArgumentType]
            content_types=["left_chat_member"],
            pass_bot=True,
        )

    async def verify_answer(self, bot: AsyncTeleBot, message: Message) -> None:
        if message.from_user is None or message.text is None:
            return
        if self._service.check_answer(message.chat.id, message.from_user.id, message.text):
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.id)
            except Exception:
                pass
            await bot.send_message(
                message.chat.id,
                strings.PASSED.format(name=message.from_user.full_name or ""),
            )

    async def handle_join(self, bot: AsyncTeleBot, message: Message, new_user: User) -> JoinOutcome:
        if new_user.is_bot:
            await bot.send_message(
                message.chat.id,
                strings.PASSED_BOT.format(name=new_user.full_name or ""),
            )
            return JoinOutcome.SKIPPED

        if message.from_user is not None and new_user.id != message.from_user.id:
            return JoinOutcome.SKIPPED

        if self._chats.is_known(message.chat.id, new_user.id):
            return JoinOutcome.SKIPPED

        if time.time() - message.date > CAPTCHA_OUTDATED_TIMEOUT:
            try:
                member = await bot.get_chat_member(message.chat.id, new_user.id)
                if member.status == "member":
                    await bot.reply_to(message, strings.OUTDATED)
            except Exception:
                pass
            return JoinOutcome.SKIPPED

        return await self._run_challenge(bot, message, new_user)

    async def _run_challenge(
        self, bot: AsyncTeleBot, message: Message, new_user: User
    ) -> JoinOutcome:
        question, answer = random.choice(strings.QUESTIONS)
        intro = strings.CHALLENGE_INTRO.format(time=self._challenge_time)

        challenge_msg = await bot.reply_to(message, f"{intro}`{question}`")
        ch = self._service.create(
            message.chat.id,
            new_user.id,
            challenge_msg.id,
            answer,
            challenge_time=self._challenge_time,
        )

        while ch.status == ch.status.ONGOING and ch.time_left > 0:
            await asyncio.sleep(1)
            ch.time_left -= 1

        await self._cleanup(bot, ch)

        if ch.status == ch.status.ABORTED:
            return JoinOutcome.ABORTED

        if ch.status == ch.status.ONGOING:
            try:
                await bot.ban_chat_member(
                    chat_id=ch.chat_id,
                    user_id=ch.user_id,
                    revoke_messages=False,
                )
                # Stagger: without a brief gap the unban can race the ban on
                # Telegram's side, leaving the user banned (only_if_banned then
                # silently no-ops because the ban isn't committed yet).
                await asyncio.sleep(1)
                await bot.unban_chat_member(
                    chat_id=ch.chat_id,
                    user_id=ch.user_id,
                    only_if_banned=True,
                )
                await bot.send_message(
                    ch.chat_id,
                    strings.TIMEOUT.format(name=new_user.full_name or str(new_user.id)),
                )
            except Exception:
                pass
            return JoinOutcome.FAILED

        return JoinOutcome.PASSED

    async def _cleanup(self, bot: AsyncTeleBot, ch) -> None:  # noqa: ANN001
        try:
            await bot.delete_message(ch.chat_id, ch.captcha_message_id)
        except Exception:
            pass
        self._service.remove(ch)

    async def _handle_left_member(self, message: Message, bot: AsyncTeleBot) -> None:
        if message.left_chat_member is not None:
            self._service.abort(message.chat.id, message.left_chat_member.id)
