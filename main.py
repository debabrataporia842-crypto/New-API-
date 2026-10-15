from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# গ্যারেনা অফিশিয়াল ইন্ডিয়া/বিডি প্লেয়ার ইনফো অ্যান্ডপয়েন্ট
GARENA_PLAYER_API = "https://client.ind.garena.com/api/player/get_player_info"

@app.route('/get_player', methods=['GET', 'POST'])
def get_player():
    # GET অথবা POST উভয়ভাবেই UID নেওয়া যাবে
    if request.method == 'POST':
        data = request.get_json() or {}
        uid = data.get("uid")
    else:
        uid = request.args.get("uid")

    if not uid:
        return jsonify({"status": "error", "message": "UID আবশ্যক"}), 400

    payload = {"uid": str(uid)}
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11)",
        "Content-Type": "application/json",
        "X-GARENA-GAME": "100067"
    }

    try:
        response = requests.post(GARENA_PLAYER_API, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            res_data = response.json()
            
            # নিখুঁত এবং সঠিক ডেটা রিটার্ন
            return jsonify({
                "status": "success",
                "data": {
                    "uid": uid,
                    "nickname": res_data.get("nickname", "N/A"),
                    "level": res_data.get("level", "N/A"),
                    "exp": res_data.get("exp", "N/A"),
                    "likes": res_data.get("likes", "N/A"),
                    "region": res_data.get("region", "IND"),
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
                "message": "গ্যারেনা সার্ভার থেকে সঠিক ডাটা পাওয়া যায়নি বা প্লেয়ার পাওয়া যায়নি।"
            }), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
