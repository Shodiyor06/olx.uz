import hashlib
import hmac

from django.conf import settings


def check_telegram_auth(data: dict) -> bool:
    """
    Telegram login hash verification
    """

    received_hash = data.get("hash")

    # hash ni olib tashlaymiz
    data = {k: v for k, v in data.items() if k != "hash"}

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))

    secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()

    calculated_hash = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    return calculated_hash == received_hash
