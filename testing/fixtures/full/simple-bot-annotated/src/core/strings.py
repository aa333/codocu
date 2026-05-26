import random

RESPONSES_NO = ["Руки убрал", "Не трожь чужое"]
BTN_DELETE = "Удалить"
MSG_DELETED = "Удалено"


def random_no() -> str:
    return random.choice(RESPONSES_NO)
