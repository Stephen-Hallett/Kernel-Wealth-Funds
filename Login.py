import os

import requests


def get_kernel_token() -> float:
    session = requests.Session()

    res = session.get("https://my.kernelwealth.co.nz/api/auth/csrf")
    csrf = res.json()["csrfToken"]

    url = "https://my.kernelwealth.co.nz/api/auth/callback/login?"

    payload = {
        "username": os.environ["KERNEL_USERNAME"],
        "password": os.environ["KERNEL_PASSWORD"],
        "csrfToken": csrf,
        "json": True,
    }
    response = session.post(url, json=payload)

    url = "https://my.kernelwealth.co.nz/api/auth/session"
    response = session.get(url)
    return response.json()["accessToken"]
