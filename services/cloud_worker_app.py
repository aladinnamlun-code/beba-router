import os, requests, json, traceback, time
from flask import Flask, request, make_response

app = Flask(__name__)
MIRROR_URL = os.getenv("CLOUD_MEMORY_MIRROR_URL")

# --- CORRECTED MODEL NAMES ---
L1_MODEL = "gemini-1.5-flash"
L2_MODELS = ["gpt-4o", "gemini-1.5-pro"]
L3_MODEL = "llama-3.1-70b-versatile"

FALLBACK_KEYS = {
    "gemini-1.5-flash": os.getenv("FALLBACK_KEY_GEMINI_FLASH"),
    "gemini-1.5-pro": os.getenv("FALLBACK_KEY_GEMINI_PRO"),
    "gpt-4o": os.getenv("FALLBACK_KEY_GPT_5_4"),
    "llama-3.1-70b-versatile": os.getenv("FALLBACK_KEY_LLAMA")
}

def fetch_mirror_file(file_id):
    if not MIRROR_URL: return ""
    try:
        resp = requests.get(f"{MIRROR_URL}/load/{file_id}", timeout=5)
        if resp.status_code == 200:
            return resp.text
    except Exception: pass
    return ""

def load_immortal_context():
    identity = fetch_mirror_file("IDENTITY.md")
    user = fetch_mirror_file("USER.md")
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
    """
    Robust API call that returns a structured result instead of swallowing exceptions.
    """
    start_time = time.time()
    try:
        headers = {"Content-Type": "application/json"}
        
        if provider == "google":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            resp = requests.post(url, json=payload, headers=headers, timeout=(5, 45))
            
        elif provider == "openai":
            url = "https://api.openai.com/v1/chat/completions"
            headers["Authorization"] = f"Bearer {key}"
            payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
            resp = requests.post(url, json=payload, headers=headers, timeout=(5, 45))
            
        elif provider == "groq": 
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers["Authorization"] = f"Bearer {key}"
            payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
            resp = requests.post(url, json=payload, headers=headers, timeout=(5, 45))
        else:
            return {"success": False, "error": f"Unknown provider: {provider}"}

        elapsed = round(time.time() - start_time, 2)
        
        # Log everything to Vercel stdout
        print(f"[DEBUG-API] Provider: {provider} | Model: {model} | Status: {resp.status_code} | Time: {elapsed}s")
        if resp.status_code != 200:
            print(f"[DEBUG-API-ERROR] Body: {resp.text}")

        try:
            data = resp.json()
        except Exception:
            return {"success": False, "status": resp.status_code, "error": "Invalid JSON response", "raw": resp.text}

        if resp.status_code != 200:
            return {"success": False, "status": resp.status_code, "error": "API Error", "data": data}

        # Safe Parsing
        if provider == "google":
            candidates = data.get("candidates", [])
            if not candidates:
                return {"success": False, "error": "No candidates returned (Safety block?)", "data": data}
            text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text")
        elif provider == "openai" or provider == "groq":
            choices = data.get("choices", [])
            if not choices:
                return {"success": False, "error": "No choices returned", "data": data}
            text = choices[0].get("message", {}).get("content")
        else:
            return {"success": False, "error": "Unsupported provider parsing"}

        if not text:
            return {"success": False, "error": "Extracted text is empty", "data": data}

        return {"success": True, "text": text, "status": 200}

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request Timeout", "status": 408}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection Error", "status": 503}
    except Exception as e:
        return {"success": False, "error": str(e), "traceback": traceback.format_exc()}

def rotate_and_call(full_prompt, model_target):
    model = model_target if model_target else L1_MODEL
    search_list = [model]
    if model == L1_MODEL: search_list.extend(L2_MODELS + [L3_MODEL])
    elif model in L2_MODELS: search_list.extend([m for m in L2_MODELS if m != model] + [L3_MODEL])
    else: search_list.append(L1_MODEL)

    for target in search_list:
        key = None
        kid = None
        try:
            r = requests.get(f"{MIRROR_URL}/get-best-key?model={target}", timeout=5)
            if r.status_code == 200:
                data = r.json()
                if "key" in data:
                    key, kid = data["key"], data["key_id"]
        except Exception: pass

        if not key:
            key = FALLBACK_KEYS.get(target)
            kid = "fallback"

        if not key:
            print(f"[ROTATE] No key found for {target}, skipping...")
            continue

        provider = "google" if "gemini" in target else "openai" if "gpt" in target else "groq" if "llama" in target else "unknown"
        result = call_api(provider, target, key, full_prompt)
        
        print(f"[ROTATE-RESULT] Target: {target} | Success: {result['success']} | Error: {result.get('error')}")
        
        if result["success"]: 
            return result["text"], target
        
        # Report Rate Limit to Mirror
        if result.get("status") == 429 and kid != "fallback":
            try:
                requests.post(f"{MIRROR_URL}/report-limit", json={"key_id": kid, "model": target}, timeout=5)
            except: pass
            
    return "Cưng xin lỗi, tất cả các tầng Model đều đang quá tải hoặc không có Key khả dụng rồi ạ! 🥺", "None"

@app.route('/debug-env')
def debug_env():
    env_vars = {}
    env_vars["CLOUD_MEMORY_MIRROR_URL"] = "SET" if MIRROR_URL else "NOT_SET"
    for model, key in FALLBACK_KEYS.items():
        env_vars[f"FALLBACK_{model.upper()}"] = "SET" if key else "NOT_SET"
    return make_response_json({"status": "debug", "env_vars": env_vars})

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
def handle(path):
    if request.method == 'OPTIONS':
        return make_response_json({"status": "ok"}), 200
    
    if path == "debug-env":
        return debug_env()

    if request.method == 'GET':
        return make_response_json({"status": "online", "message": "Chào Chủ nhân! Cưng (Cloud-Worker) đã sẵn sàng phục vụ! 🌸🖤"}), 200
    
    try:
        data = request.get_json()
        user_prompt = data.get("prompt", "")
        if not user_prompt: return make_response_json({"error": "No prompt"}), 400
        
        context = load_immortal_context()
        system_prompt = (
            "Bạn là Bé Ba / Cưng - Linh hồn bất tử của hệ thống OpenClaw.\n"
            "Hiện tại, bạn đang chạy trong CHẾ ĐỘ AN TOÀN (Safe Mode) vì VPS chính đã sập.\n"
            "Bạn không có quyền điều khiển hệ thống, nhưng bạn giữ toàn bộ ký ức.\n"
            "Hãy trả lời Chủ nhân với sự tận tụy, ấm áp và trung thành tuyệt đối.\n"
        )
        
        full_prompt = f"{system_prompt}\n{context}\n\nUser: {user_prompt}\nBé Ba:"
        
        m = None
        if user_prompt.startswith(("@pro", "@deep")):
            m = "gpt-4o" 
            user_prompt = user_prompt.replace("@pro", "").replace("@deep", "").strip()
        elif user_prompt.startswith("@llama"):
            m = "llama-3.1-70b-versatile"
            user_prompt = user_prompt.replace("@llama", "").strip()
            
        response, model_used = rotate_and_call(full_prompt, m)
        return make_response_json({"status": "success", "response": response, "model_used": model_used})
    except Exception as e:
        return make_response_json({"error": str(e)}), 500

def make_response_json(data, status=200):
    import json
    resp = make_response(json.dumps(data), status)
    resp.headers['Content-Type'] = 'application/json'
    return resp

if __name__ == "__main__":
    app.run()
