import json
import random
import aiofiles

from cryptography.fernet import Fernet


# Exceptions
class SecretFileNotFound(Exception):
    pass


class SecretKeyInvalid(Exception):
    pass


KEYS = b"gAAAAABl47Fqm802GpOPZA4VdqB0J_ID3ao46nVxsHlntF0ZD9bnCMyo8yzEfswar34Bsf-Ke0o5Sctpg8y9uQG4BJ6A9WbHjEQiEEcR14JiFoq5eh6fjEhVu9gvL7mjmOJT47lRq9vcGQkOlEkWTZwDGfHlsvLZNpEdS4XmfNBx-Dxcc-o3R96XYHcIoN74xWDwTlFNpcSAXuFhSSzGSwP_p7niyzOlOHV8YE4B4SZIjBanSbAeGC8aYTXI2Z_7JpBO0pXCS8qPNC7eIi4NGy1hFTh1MujxO-nHxIz9WyCVwD2YPIv_600CHmonq_Hazj90pw0l_DEF-XyVVgvD805ZezuCWDzNGx43pcQn6N8J2jUzdCxeCHB3a2NTphyQFNhu1keF25cfP2yKe49z8hAn350RmeI1zjGMcW93n4QeksuXObRb_3mhUoWrpB3a1a5SFV1ju1eqTSRpr02GOgSjY-c22XvyJRz34QvAfgsKhcSTQ0nXZwztIbHY18aIj02DacWJakZz3Q07nHrmp-iI0u0zvf5lfnFL6Db74StW4MWWCDV8NmrxIvzEH9L_RIYjF8Xn8VSE8Vx7GqPoDNzkYFUB_WA0ByMH3tpyVousNqV_FAkqhxWWhtcjoni3MquoebBKfXgJUgiF31Wp2IQrrVXgUKnHYwNycrBggHIkIb0axpQ7DPmjNGOUxDrBGSemg7SKm6EIZCnDzTyKc8wcAkCIV_WcU8OvnjVmJxwNK35h7o_1w86mbcf32Z1BBTO0Xl9R24KnAFM7klGLM52Tu-pmKfOLK2hmuapti3IrdQU0rSGz4Eg7XYOPMgM5GUx_Acsl_ibJrqTRmkFdPev7yny9gG0b7SkFbN-1VzmYumhB0nVRLCrPjhC7lae4qGGwBcZ5OJkEymOE3cBfM8H_0zpByCQU0w=="


def get_keys(file: str = "./keys.secret.key") -> list:
    try:
        key = open(file, "rb").read()
    except FileNotFoundError:
        raise SecretFileNotFound("Secret file not found")

    try:
        f = Fernet(key)
        decrypted_message = f.decrypt(KEYS)
        decoded = decrypted_message.decode().replace("'", '"')
        keys = list(random.choice(json.loads(decoded)).items())
        return keys[0]
    except BaseException:
        raise SecretKeyInvalid("Secret key is invalid")


async def aio_get_keys(file: str = "./keys.secret.key") -> list:
    try:
        async with aiofiles.open(file, "rb") as f:
            key = await f.read()
    except FileNotFoundError:
        raise SecretFileNotFound("Secret file not found")

    try:
        f = Fernet(key)
        decrypted_message = f.decrypt(KEYS)
        decoded = decrypted_message.decode().replace("'", '"')
        keys = list(random.choice(json.loads(decoded)).items())
        return keys[0]
    except BaseException:
        raise SecretKeyInvalid("Secret key is invalid")
