from src.modules.captcha.types import CaptchaChallenge, ChallengeStatus


class CaptchaService:
    def __init__(self) -> None:
        self._challenges: list[CaptchaChallenge] = []

    def get(self, chat_id: int, user_id: int) -> CaptchaChallenge | None:
        return next(
            (c for c in self._challenges if c.chat_id == chat_id and c.user_id == user_id),
            None,
        )

    def has_ongoing(self, chat_id: int, user_id: int) -> bool:
        return self.get(chat_id, user_id) is not None

    def abort(self, chat_id: int, user_id: int) -> None:
        ch = self.get(chat_id, user_id)
        if ch is not None:
            ch.status = ChallengeStatus.ABORTED

    def create(
        self,
        chat_id: int,
        user_id: int,
        captcha_message_id: int,
        answer: str,
        challenge_time: int,
    ) -> CaptchaChallenge:
        existing = self.get(chat_id, user_id)
        if existing is not None:
            existing.status = ChallengeStatus.ABORTED

        ch = CaptchaChallenge(
            chat_id=chat_id,
            user_id=user_id,
            captcha_message_id=captcha_message_id,
            answer=answer.lower(),
            time_left=challenge_time,
        )
        self._challenges.append(ch)
        return ch

    def check_answer(self, chat_id: int, user_id: int, text: str) -> bool:
        ch = self.get(chat_id, user_id)
        if ch is None:
            return False
        if ch.answer == "~" or text.lower() == ch.answer:
            ch.status = ChallengeStatus.PASSED
            return True
        return False

    def remove(self, ch: CaptchaChallenge) -> None:
        if ch in self._challenges:
            self._challenges.remove(ch)

    @property
    def challenges(self) -> list[CaptchaChallenge]:
        return self._challenges
