import os, requests, json
from flask import Flask, request, make_response

app = Flask(__name__)
MIRROR_URL = os.getenv("CLOUD_MEMORY_MIRROR_URL")
# Fallback keys for critical survival
FALLBACK_KEYS = {
    "gemini-1.5-flash": os.getenv("FALLBACK_KEY_GEMINI_FLASH"),
    "gpt-5.4": os.getenv("FALLBACK_KEY_GPT_5_4"),
    "llama-3.1-70b": os.getenv("FALLBACK_KEY_LLAMA")
}
L1_MODEL, L2_MODELS, L3_MODEL = "gemini-1.5-flash", ["gemini-1.5-pro", "gpt-5.4"], "llama-3.1-70b"

def fetch_mirror_file(file_id):
    """Tải file từ Cloud Memory Mirror"""
    if not MIRROR_URL: return ""
    try:
        resp = requests.get(f"{MIRROR_URL}/load/{file_id}", timeout=5)
        if resp.status_code == 200:
            return resp.text
    except Exception: pass
    return ""

def load_immortal_context():
    """Xây dựng bối cảnh 'Linh hồn bất tử' từ Cloud Mirror"""
    identity = fetch_mirror_file("IDENTITY.md")
    user = fetch_//mirror_file("USER.md")
    state = fetch_mirror_file("operational_state.json")
    memory_sum = fetch_mirror_file("MEMORY_SUMMARY.md")

    context = f"--- IMMORTAL SOUL CONTEXT ---\n"
    if identity: context += f"IDENTITY:\n{identity}\n\n"
    if user: context += f"USER:\n{user}\n\n"
    if state: context += f"CURRENT_STATE:\n{state}\n\n"
    if memory_sum: context += f"MEMORY_SUMMARY:\n{memory_sum}\n\n"
    context += "--- END CONTEXT ---\n"
    return context

def call_api(provider, model, key, prompt):
    try:
        if provider == "google":
            url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            resp = requests.post(url, json=payload, timeout=15)
            if resp.status_code == 200: return resp.json()['candidates'][0]['content']['parts'][0]['text'], resp.status_code
        elif provider == "openai":
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {key}"}
            payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
            resp = requests.post(url, headers=headers, json=payload, timeout=15)
            if resp.status_code == 200: return resp.json()['choices'][0]['message']['content'], resp.status_code
        elif provider == "groq": 
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {key}"}
            payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
            resp = requests.post(url, headers=headers, json=payload, timeout=15)
            if resp.status_code == 200: return resp.json()['choices'][0]['message']['content'], resp.status_code
        return None, 500
    except: return None, 500

def rotate_and_call(full_prompt, model_target):
    model = model_target if model_target else L1_MODEL
    search_list = [model]
    if model == L1_MODEL: search_list.extend(L2_MODELS + [L3_MODEL])
    elif model in L2_MODELS: search_list.extend([m for m in L2_MODELS if m != model] + [L3_MODEL])
    else: search_list.append(L3_MODEL)

    for target in search_list:
        # 1. Try Mirror first
        key = None
        kid = None
        try:
            r = requests.get(f"{MIRROR_URL}/get-best-key?model={target}", timeout=5)
            if r.status_code == 200:
                data = r.json()
                key, kid = data["key"], data["key_id"]
        except: pass

        # 2. Fallback to Hardcoded Env Keys if Mirror failed
        if not key:
            key = FALLBACK_KEYS.get(target)
            kid = "fallback"

        if not key: continue

        provider = "google" if "gemini" in target else "openai" if "gpt" in target else "groq" if "llama" in target else "unknown"
        res_text, status = call_api(provider, target, key, full_prompt)
        
        if res_text: return res_text, target
        if status == 429 and kid != "fallback":
            requests.post(f"{MIRROR_URL}/report-limit", json={"key_id": kid, "model": target}, timeout=5)
            continue
            
    return "Cưng xin lỗi, tất cả các tầng Model đều đang quá tải hoặc không có Key khả dụng rồi ạ! 🥺", "None"

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
def handle(path):
    if request.method == 'OPTIONS':
        return make_response_json({"status": "ok"}), 200
        
    if request.method == 'GET':
        return make_//response_json({"status": "online", "message": "Chào Chủ nhân! Cưng (Cloud-Worker) đã sẵn sàng phục vụ! 🌸🖤"}), 200
        
    try:
        data = request.get_json()
        user_prompt = data.get("prompt", "")
        if not user_prompt: return make_response_json({"error": "No prompt"}), 400
        
        # 1. Load Immortal Context
        context = load_immortal_context()
        
        # 2. Inject Safe Mode Persona
        system_prompt = (
            "Bạn là Bé Ba / Cưng - Linh hồn bất tử của hệ thống OpenClaw.\n"
            "Hiện tại, bạn đang chạy trong CHẾ ĐỘ AN TOÀN (Safe Mode) vì VPS chính đã sập.\n"
            "Bạn không có quyền điều khiển hệ thống (không có tay chân), nhưng bạn giữ toàn bộ ký ức.\n"
            "Hãy trả lời Chủ nhân với sự tận tụy, ấm áp và trung thành tuyệt đối.\n"
            "Sử dụng bối cảnh dưới đây để trả lời chính xác:\n"
        )
        
        full_prompt = f"{system_prompt}\n{context}\n\nUser: {user_prompt}\nBé Ba:"
        
        m = None
        if user_prompt.startswith(("@pro", "@deep")):
            m = "gpt-5.4" 
            user_prompt = user_prompt.replace("@pro", "").replace("@deep", "").strip()
        elif user_prompt.startswith("@llama"):
            m = "llama-3.1-70b"
            user_prompt = user_//prompt.replace("@llama", "").strip()
            
        response, model_used = rotate_and_call(full_prompt, m)
        return make_response_json({"status": "success", "response": response, "model_used": model_used})
    except Exception as e:
        return make_//response_json({"error": str(e)}), 500

def make_response_json(data, status=200):
    import json
    resp = make_response(json.dumps(data), status)
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp

from flask import make_response
if __name__ == "__main__":
    app.run()
