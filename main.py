import json
import os
import time
from base64 import b64decode
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

load_dotenv()

api_point = os.getenv("POP_API_POINT")
next_token = ""


def pop() -> None:
    global next_token
    query = {
        'count': 800,
        'token': next_token,
        'captcha_token': ''
    }
    url = f"{api_point}?{urlencode(query)}"
    response = requests.post(url)
    if response.status_code in [200, 201]:
        result = response.json()
        next_token = result["new_token"]
        data = next_token.split(".")
        if len(data) == 3:
            missing_padding = 4 - len(data[1]) % 4
            if missing_padding:
                data[1] += "=" * missing_padding
            token_raw = b64decode(data[1])
            print(json.dumps(json.loads(token_raw), sort_keys=True, indent=4))
    else:
        print(f"Error: {response.status_code}")


if __name__ == '__main__':
    while True:
        pop()
        time.sleep(1)
