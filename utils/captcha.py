import requests
from django.conf import settings


def verify_recaptcha(token):
    """Google reCAPTCHA tokenini tekshirish"""
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={"secret": settings.GOOGLE_RECAPTCHA_SECRET, "response": token},
    )
    result = response.json()
    return result.get("success", False)


def get_recaptcha_token():
    url = f"https://www.google.com/recaptcha/api.js?render={settings.RECAPTCHA_SITE_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Successfully fetched reCAPTCHA script")
    else:
        print("Error fetching reCAPTCHA script: ", response.text)
