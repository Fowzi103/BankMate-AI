# BankMate AI

A banking-question assistant with a Streamlit frontend and a separate GPU inference API. The language model is Qwen3-4B with a QLoRA adapter.

## Repository contents

- `app.py` — Streamlit frontend (deploy this on Streamlit Community Cloud).
- `requirements.txt` — frontend dependencies.
- `inference_api.py` — FastAPI backend that loads the Qwen3-4B base model and your LoRA adapter.
- `backend-requirements.txt` — GPU backend dependencies.
- `.streamlit/config.toml` — BankMate theme.

## Important deployment architecture

Streamlit Community Cloud hosts the frontend only. It is not suitable for reliably hosting this 4B model and its GPU inference. Host `inference_api.py` on a GPU machine/service that can access your adapter, then configure the frontend.

### Deploy the frontend

1. Push this repository to GitHub.
2. Open https://share.streamlit.io/ and create an app from this repository.
3. Set the main file path to `app.py`.
4. In the Streamlit app settings, add a secret:

```toml
BANKING_API_URL = "https://YOUR-GPU-SERVER-URL"
```

The URL should be the base URL of the backend, without `/chat`.

### Run the GPU backend

On a CUDA-enabled GPU machine, make the adapter folder available and install:

```bash
pip install -r backend-requirements.txt
```

Set the adapter path if it differs from the default:

```bash
export ADAPTER_DIR="/path/to/fast_finetuned_model"
```

Start the API:

```bash
uvicorn inference_api:app --host 0.0.0.0 --port 8000
```

The backend exposes:
- `GET /health`
- `POST /chat` with JSON `{"question": "..."}`

For a temporary demo, a Cloudflare Tunnel can expose port 8000, but the GPU machine and tunnel must remain running. A persistent deployment needs a persistent GPU host and appropriate access controls.

## Model files

Do not upload the base model or adapter weights to this repository. Keep the adapter in private storage or a model repository with appropriate access controls. Check the dataset and model licenses before redistributing anything.

## Safety

Use fictional data for testing. Never enter real PINs, passwords, CVVs, OTPs, or full card/account numbers. This chatbot provides general information and is not a bank's official support channel.
