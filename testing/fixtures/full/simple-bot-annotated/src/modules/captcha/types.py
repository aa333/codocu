from dataclasses import dataclass
from enum import Enum

CAPTCHA_OUTDATED_TIMEOUT = 45


class ChallengeStatus(Enum):
    ONGOING = 1
    PASSED = 2
    ABORTED = 3


class JoinOutcome(Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ABORTED = "aborted"


@dataclass
class CaptchaChallenge:
    chat_id: int
    user_id: int
    captcha_message_id: int
    answer: str
    time_left: int
    status: ChallengeStatus = ChallengeStatus.ONGOING

    def __str__(self) -> str:
        return (
            f"{self.chat_id}:{self.user_id} ans:{self.answer} st:{self.status} t:{self.time_left}"
        )
