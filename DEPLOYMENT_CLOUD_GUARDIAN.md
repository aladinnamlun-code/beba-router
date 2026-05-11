# 🚀 CLOUD-GUARDIAN DEPLOYMENT GUIDE (Phase 3)
# ---------------------------------------------------
# This guide explains how to deploy the Cloud-Guardian components to a serverless environment.

## 1. Components to Deploy
- **Cloud Router**: The entry point for all Telegram webhooks.
- **Cloud Worker**: The degraded mode handler.
- **Cloud Memory Mirror**: The synchronized copy of WAL and Core Memory.

## 2. Recommended Stack (Free Tier)
- **Compute**: Vercel / Google Cloud Functions / AWS Lambda (Node.js or Python).
- **Database**: MongoDB Atlas (Free Shared Cluster) for the Memory Mirror.
- **Network**: Cloudflare (for DNS and fast routing).

## 3. Setup Steps
1. **Setup MongoDB Atlas**: Create a cluster and a database `openclaw_mirror`.
2. **Deploy Cloud Router**: 
   - Deploy `services/cloud_router.py` as a serverless function.
   - Set Environment Variables:
     - `LOCAL_SERVER_URL`: URL of the local server (e.g., https://tproopenclaw.tino.page/request).
     - `CLOUD_WORKER_URL`: URL of the deployed Cloud Worker.
     - `MONGO_URI`: Connection string to MongoDB Atlas.
3. **Deploy Cloud Worker**:
   - Deploy `services/cloud_worker.py` as a serverless function.
   - Set Environment Variables:
     - `CLOUD_MEMORY_MIRROR_URL`: URL to fetch the latest context from MongoDB.
4. **Update Telegram Webhook**:
   - Change the Telegram bot webhook URL to point to the `Cloud Router` instead of the `Local Server`.

## 4. Validation
- **Normal Test**: Send a message $\rightarrow$ Cloud Router $\rightarrow$ Local Server $\rightarrow$ Response (OK).
- **Panic Test**: Stop `openclaw-coordinator.service` $\rightarrow$ Send message $\rightarrow$ Cloud Router $\rightarrow$ Cloud Worker $\rightarrow$ Response (Degraded Mode - OK).
