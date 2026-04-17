from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/api/games/<int:appid>/screenshots')
def get_screenshots(appid):
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=en"
        res = requests.get(url, headers={
            'User-Agent': 'Gameflix-Browser/1.0',
            'Accept-Language': 'en-US,en;q=0.9'
        }, timeout=10)
        data = res.json()
        app_data = data.get(str(appid), {})

        if not app_data.get('success'):
            return jsonify({"screenshots": [], "fullDescription": ""})

        screenshots = []
        for s in app_data.get('data', {}).get('screenshots', [])[:10]:
            screenshots.append({
                "id": s["id"],
                "path_thumbnail": s["path_thumbnail"],
                "path_full": s["path_full"]
            })

        full_description = app_data.get('data', {}).get('detailed_description', '')

        return jsonify({
            "screenshots": screenshots,
            "fullDescription": full_description
        })
    except Exception as e:
        print(f"Steam API error: {e}")
        return jsonify({"screenshots": [], "fullDescription": ""})
