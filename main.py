import asyncio
import json
import os
from base64 import b64decode
from urllib.parse import urlencode

import aiohttp
from dotenv import load_dotenv

load_dotenv()
api_point = os.getenv("POP_API_POINT")
coroutine_number = int(os.getenv("POP_COROUTINE"))


async def main() -> None:
    tokens = ["" for _ in range(coroutine_number)]
    while True:
        async with aiohttp.ClientSession() as session:
            promises = [pop(session, token) for token in tokens]
            tokens = await asyncio.gather(*promises)


async def pop(session: aiohttp.ClientSession, token: str) -> str:
    url = get_request_url(token)
    async with session.post(url) as response:
        if response.status in [200, 201]:
            result = await response.json()
            next_token = result["new_token"]
            data = next_token.split(".")
            if len(data) == 3:
                missing_padding = 4 - len(data[1]) % 4
                if missing_padding:
                    data[1] += "=" * missing_padding
                token_raw = b64decode(data[1])
                print(json.dumps(json.loads(token_raw), sort_keys=True, indent=4))
            return next_token
        else:
            print(f"Error: {response.status}")
    return ""


def get_request_url(token: str) -> str:
    query = {
        'count': 800,
        'token': token,
        'captcha_token': ''
    }
    return f"{api_point}?{urlencode(query)}"


if __name__ == '__main__':
    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
