import requests
import time

# ====== TELEGRAM SETTINGS ======
BOT_TOKEN = "8990635970:AAEw7NVARFeX324AOWdNBxrJNpdG2TaQccA"
CHAT_ID = "8156956504"

# ====== AMAZON JOB PAGE ======
URL = "https://www.jobsatamazon.co.uk/app#/jobSearch?query=Warehouse%20Operative"

# To avoid duplicate alerts
last_state = None


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })


def check_page():
    response = requests.get(URL)
    html = response.text.lower()

    # If this text is present → no jobs
    no_jobs_text = "sorry, there are no jobs available"

    if no_jobs_text in html:
        return False
    else:
        return True


def main():
    global last_state

    while True:
        try:
            job_available = check_page()

            # If job appears (state change)
            if job_available and last_state != True:
                send_telegram("🚨 Amazon Warehouse JOB FOUND!\nCheck now:\n" + URL)
                last_state = True

            # Reset when no jobs
            if not job_available:
                last_state = False

            print("Checked - Job available:", job_available)

        except Exception as e:
            print("Error:", e)

        time.sleep(300)  # every 5 minutes


if __name__ == "__main__":
    main()
