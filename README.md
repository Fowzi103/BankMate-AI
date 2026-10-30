# BankMate AI – AI-Powered Banking Chatbot

BankMate AI is a banking question-answering chatbot built with a fine-tuned Qwen3-4B model using QLoRA/LoRA. The Streamlit frontend communicates with a separate FastAPI inference backend.

## Architecture

1. User enters a banking question in Streamlit.
2. Streamlit sends the question to the FastAPI `/chat` endpoint.
3. FastAPI runs the Qwen3-4B base model with the saved LoRA adapter.
4. The answer is returned to Streamlit.

## Repository files

- `app.py` – Streamlit frontend.
- `requirements.txt` – dependencies for Streamlit Cloud.
- `backend-requirements.txt` – dependencies for the GPU inference backend.
- `.streamlit/config.toml` – visual theme.

## Deploy the frontend on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Open https://share.streamlit.io/ and sign in with GitHub.
3. Select this repository, branch, and `app.py`.
4. Deploy the app.
5. In the deployed app, open **Settings → Secrets** and add:

```toml
BANKING_API_URL = "https://YOUR-CURRENT-BACKEND-TUNNEL-URL"
```

6. Save the secret and reboot the app.

## Backend requirement

The model backend must be running separately on a machine with sufficient GPU memory. The Colab notebook loads the Qwen3-4B base model and the saved adapter, then exposes FastAPI on port `8000`. A tunnel URL must point to that API.

The Colab runtime must remain active while using a Colab-hosted backend. A temporary Cloudflare quick tunnel URL changes when restarted; update `BANKING_API_URL` in Streamlit Secrets whenever that happens.

## Model files

Do not commit model weights, adapter files, datasets, or checkpoints to this GitHub repository. Keep the trained adapter in Google Drive or another suitable model storage location and load it in the backend.

## Important limitations and safety

- This demo provides general banking information, not official financial advice.
- Never enter real account numbers, PINs, passwords, CVVs, or OTPs.
- The demo backend should be protected with authentication, rate limiting, and privacy controls before production use.
- The training notebook's quick demonstration run used a subset of up to 300 training examples and 30 steps; it did not train on the entire dataset.
