from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Free Fire Public & Dynamic Profile Inspection Endpoint
GARENA_PROFILE_API = "https://client.ind.garena.com/api/player/get_player_info"

@app.route('/get_player', methods=['GET', 'POST'])
def get_player():
    if request.method == 'POST':
        data = request.get_json() or {}
        uid = data.get("uid")
    else:
        uid = request.args.get("uid")

    if not uid:
        return jsonify({"status": "error", "message": "UID আবশ্যক"}), 400

    payload = {"uid": str(uid)}
    
    # ব্রাউজার বা রিয়েল অ্যাপ্লিকেশনের মতো ফেক হেডার ও কুকি স্ট্রাকচার যাতে ব্লক না খায়
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; M2004J19CI Build/RP1A.200720.011)",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json",
        "Connection": "Keep-Alive",
        "X-Requested-With": "com.dts.freefireth"
    }

    try:
        # সেশন রিকোয়েস্ট তৈরি করা
        session = requests.Session()
        response = session.post(GARENA_PROFILE_API, json=payload, headers=headers, timeout=12)
        
        if response.status_code == 200:
            res_data = response.json()
            
            # সব সঠিক ডেটা ম্যাপ করে রিটার্ন করা
            return jsonify({
                "status": "success",
                "data": {
                    "uid": uid,
                    "nickname": res_data.get("nickname", "N/A"),
                    "level": res_data.get("level", "N/A"),
                    "exp": res_data.get("exp", "N/A"),
                    "likes": res_data.get("likes", "N/A"),
                    "region": res_data.get("region", "BD/IND"),
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
                "message": "সঠিক ডাটা পাওয়া যায়নি। ইউআইডি চেক করুন।"
            }), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    
