import requests
import config

def send_discord(message):
    data = {"content": message}

    try:
        response = requests.post(
            config.DISCORD_WEBHOOK,
            json=data,
            timeout=10
        )
        if response.status_code == 204:
            print("✅ Gửi Discord thành công!")
        else:
            print(f"⚠️ Discord trả về status: {response.status_code}")
    except requests.exceptions.Timeout:
        print("⚠️ Discord timeout, bỏ qua lần này.")
    except requests.exceptions.ConnectionError:
        print("⚠️ Mất kết nối, bỏ qua lần này.")
    except Exception as e:
        print("Lỗi Discord:", e)