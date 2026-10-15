from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "Free Fire API is running successfully!",
        "usage": "/get_player?uid=YOUR_UID"
    })

@app.route('/get_player', methods=['GET', 'POST'])
def get_player():
    if request.method == 'POST':
        data = request.get_json() or {}
        uid = data.get("uid")
    else:
        uid = request.args.get("uid")

    if not uid:
        return jsonify({"status": "error", "message": "UID আবশ্যক! দয়া করে সঠিক UID প্রদান করুন।"}), 400

    # নির্ভরযোগ্য পাবলিক ফ্রি ফায়ার প্রক্সি এপিআই সোর্স
    proxy_api_url = f"https://ff-info-api.vercel.app/api/player?uid={uid}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(proxy_api_url, headers=headers, timeout=12)
        
        if response.status_code == 200:
            res_data = response.json()
            
            # নিখুঁত ফরম্যাটে প্লেয়ারের ডেটা রিটার্ন করা
            return jsonify({
                "status": "success",
                "data": {
                    "uid": uid,
                    "nickname": res_data.get("nickname", res_data.get("name", "N/A")),
                    "level": res_data.get("level", "N/A"),
                    "exp": res_data.get("exp", "N/A"),
                    "likes": res_data.get("likes", "N/A"),
                    "region": res_data.get("region", "IND/BD"),
                    "signature": res_data.get("signature", "N/A"),
                    "created_at": res_data.get("created_at", "N/A"),
                    "last_login": res_data.get("last_login", "N/A"),
                    "br_rank": res_data.get("br_rank", "N/A"),
                    "cs_rank": res_data.get("cs_rank", "N/A"),
                    "guild_name": res_data.get("guild_name", "N/A"),
                    "guild_id": res_data.get("guild_id", "N/A"),
                    "guild_leader": res_data.get("guild_leader", "N/A")
                }
            }), 200
        else:
            return jsonify({
                "status": "error", 
                "message": "প্লেয়ার পাওয়া যায়নি বা সার্ভার ব্যস্ত রয়েছে।"
            }), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    
