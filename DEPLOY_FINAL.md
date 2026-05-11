# 🚀 CLOUD-GUARDIAN QUICK DEPLOYMENT GUIDE
# ---------------------------------------------------

## 1. Prerequisite
- A Vercel or Google Cloud Functions account.
- A MongoDB Atlas Free Tier account.
- A Telegram Bot Token.

## 2. Step-by-Step Deployment

### Step A: Deploy Cloud Memory Mirror
1. Create a MongoDB Atlas cluster.
2. Create a collection `memory_mirror`.
3. Deploy a simple API (using the logic in `services/cloud_router.py`'s mirror section) to save/load JSON.

### Step B: Deploy Cloud Worker
1. Copy `services/cloud_worker_app.py` to a Vercel project.
2. Set Env Vars:
   - `CLOUD_MEMORY_MIRROR_URL`: URL of your MongoDB API.
   - `TELEGRAM_BOT_TOKEN`: Your bot token.
3. Deploy. Note the URL (e.g., `https://cloud-worker.vercel.app`).

### Step la Step C: Deploy Cloud Router
1. Copy `services/cloud_router_app.py` to a Vercel project.
2. Set Env Vars:
   - `LOCAL_SERVER_URL`: `https://tproopenclaw.tino.//request`
   - `CLOUD_WORKER_URL`: URL from Step B.
   - `TELEGRAM_BOT_TOKEN`: Your bot token.
3. Deploy. Note the URL (e.g., `https://cloud-router.vercel.app`).

### Step D: Final Activation
1. Update your Telegram Bot Webhook to point to the **Cloud Router URL**.
2. Update `services/heartbeat_manager.py` with the `CLOUD_ROUTER_URL`.
3. Restart `openclaw-coordinator.service`.

## 3. Verification
- **Test 1**: Send a message. It should route to Local $\rightarrow$ Response.
- **Test 2**: Run `sudo systemctl stop openclaw-coordinator.service`.
- **Test 3**: Send a message. You should receive a Telegram Alert and a response from the Cloud Worker.
