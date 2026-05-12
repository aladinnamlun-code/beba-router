import os, requests, json, traceback, time, socket, ssl
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

        if resp.status_code != 200:
            return {"success": False, "status": resp.status_code, "error": "API Error", "raw": resp.text}

        data = resp.json()
        if provider == "google":
            candidates = data.get("candidates", [])
            if not candidates: return {"success": False, "error": "No candidates", "data": data}
            text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text")
        elif provider == "openai" or provider == "groq":
            choices = data.get("choices", [])
            if not choices: return {"success": False, "error": "No choices", "data": data}
            text = choices[0].get("message", {}).get("content")
        else:
            return {"success": False, "error": "Unsupported provider parsing"}

        return {"success": True, "text": text, "status": 200} if text else {"success": False, "error": "Empty text"}

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

        if not key: continue

        provider = "google" if "gemini" in target else "openai" if "gpt" in target else "groq" if "llama" in target else "unknown"
        result = call_api(provider, target, key, full_prompt)
        if result["success"]: return result["text"], target
        
        if result.get("status") == 429 and kid != "fallback":
            try:
                requests.post(f"{MIRROR_URL}/report-limit", json={"key_id": kid, "model": target}, timeout=5)
            except: pass
            
        continue
            
    return "Cưng xin lỗi, tất cả các tầng Model đều đang quá tải hoặc không có Key khả dụng rồi ạ! 🥺", "None"

@app.route('/test-api', methods=['GET'])
def test_api():
    results = {}
    providers = [
        {
            "name": "google",
            "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
            "headers": {"Content-Type": "application/json"},
            "params": {"key": os.getenv("FALLBACK_KEY_GEMINI_FLASH")},
            "json": {"contents": [{"parts": [{"text": "Hello"}]}]}
        },
        {
            "name": "openai",
            "url": "https://api.openai.com/v1/chat/completions",
            "headers": {
                "Authorization": f"Bearer {os.getenv('FALLBACK_KEY_GPT_5_4')}",
                "Content-Type": "application/json"
            },
            "json": {"model": "gpt-4o", "messages": [{"role": "user", "content": "Hello"}]}
        },
        {
            "name": "groq",
            "url": "https://api.groq.com/openai/v1/chat/completions",
            "headers": {
                "Authorization": f"Bearer {os.getenv('FALLBACK_KEY_LLAMA')}",
                "Content-Type": "application/json"
            },
            "json": {"model": "llama-3.1-70b-versatile", "messages": [{"role": "user", "content": "Hello"}]}
        }
    ]

    try:
        r = requests.get("https://httpbin.org/get", timeout=(20, 60))
        results["internet_test"] = {"success": True, "status": r.status_code}
    except Exception as e:
        results["internet_test"] = {"success": False, "error": str(e), "traceback": traceback.format_exc()}

    dns_tests = {}
    for host in ["api.openai.com", "generativelanguage.googleapis.com", "api.groq.com"]:
        try:
            ip = socket.gethostbyname(host)
            dns_tests[host] = {"success": True, "ip": ip}
        except Exception as e:
            dns_tests[host] = {"success": False, "error": str(e)}
    results["dns"] = dns_tests

    results["env_check"] = {
        "gemini_exists": bool(os.getenv("FALLBACK_KEY_GEMINI_FLASH")),
        "gemini_len": len(os.getenv("FALLBACK_KEY_GEMINI_FLASH", "")),
        "openai_exists": bool(os.getenv("FALLBACK_KEY_GPT_5_4")),
        "openai_len": len(os.getenv("FALLBACK_KEY_GPT_5_4", "")),
        "groq_exists": bool(os.getenv("FALLBACK_KEY_LLAMA")),
        "groq_len": len(os.getenv("FALLBACK_KEY_LLAMA", ""))
    }

    provider_results = {}
    for p in providers:
        try:
            start = time.time()
            resp = requests.post(
                p["url"], 
                headers=p["headers"], 
                params=p.get("params"), 
                json=p["json"], 
                timeout=(20, 90)
            )
            elapsed = round(time.time() - start, 2)
            provider_results[p["name"]] = {
                "success": resp.status_code == 200,
                "status_code": resp.status_code,
                "elapsed": elapsed,
                "response_text": resp.text[:2000]
            }
        except Exception as e:
            provider_results[p["name"]] = {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }
    results["providers"] = provider_results

    return make_response(json.dumps(results, indent=2), 200, {"Content-Type": "application/json"})

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
def handle(path):
    if request.method == 'OPTIONS':
        return make_response_json({"status": "ok"}), 200
    
    if path == "test-api":
        return test_api()

    if request.method == 'GET':
        return make_//response_json({"status": "online", "message": "Chào Chủ nhân! Cưng (Cloud-Worker) đã sẵn sàng phục vụ! 🌸🖤"}), 200
    
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
            user_prompt = user_//prompt.replace("@llama", "").strip()
            
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
