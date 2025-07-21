import requests
import os
import sys

def check_website(url):
    """
    سایت را چک می‌کند. اگر با موفقیت باز شد (status code 200)، True برمی‌گرداند.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"Success! Website {url} is up. Status code: {response.status_code}")
            return True
        else:
            print(f"Failure. Website {url} returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error checking website {url}: {e}")
        return False

def send_telegram_message(token, chat_id, message):
    """
    یک پیام متنی به ربات تلگرام ارسال می‌کند.
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200 and response.json().get("ok"):
            print("Telegram message sent successfully!")
        else:
            print(f"Failed to send Telegram message. Response: {response.text}")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

if __name__ == "__main__":
    # خواندن اطلاعات از متغیرهای محیطی که توسط GitHub Actions تنظیم می‌شوند
    SITE_URL = os.getenv("SITE_URL")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    # بررسی اینکه آیا متغیرها تنظیم شده‌اند
    if not all([SITE_URL, BOT_TOKEN, CHAT_ID]):
        print("Error: Required environment variables (SITE_URL, BOT_TOKEN, CHAT_ID) are not set.")
        sys.exit(1) # خروج با خطا

    # چک کردن سایت
    if check_website(SITE_URL):
        # اگر سایت بالا بود، پیام ارسال کن
        message_text = f"✅ سایت {SITE_URL} با موفقیت باز شد و در دسترس است!"
        send_telegram_message(BOT_TOKEN, CHAT_ID, message_text)