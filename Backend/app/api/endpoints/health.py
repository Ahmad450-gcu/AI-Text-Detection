import socket
import requests
from fastapi import APIRouter
from app.core.config import settings
from app.models.response_models import HealthResponse
from app.services.model_loader import get_device, get_model_display_name, is_ready

router = APIRouter()


@router.get(
    "/debug/dns",
    summary="Diagnostic: check outbound DNS resolution",
    description="Temporary debugging endpoint to isolate DNS/egress issues.",
)
async def debug_dns() -> dict:
    hosts_to_check = [
        "google.com",
        "huggingface.co",
        "router.huggingface.co",
    ]
    results = {}
    for host in hosts_to_check:
        try:
            addr_info = socket.getaddrinfo(host, 443)
            ip = addr_info[0][4][0]
            results[host] = {"resolved": True, "ip": ip}
        except Exception as exc:
            results[host] = {"resolved": False, "error": str(exc)}
    return results


@router.get(
    "/debug/hf-call",
    summary="Diagnostic: make the exact HF inference call the app makes",
    description="Temporary debugging endpoint to see the real request/response.",
)
async def debug_hf_call() -> dict:
    from app.services.model_loader import API_URL

    headers = {}
    token_present = bool(settings.HF_API_TOKEN)
    if token_present:
        headers["Authorization"] = f"Bearer {settings.HF_API_TOKEN}"

    result = {
        "api_url": API_URL,
        "token_present": token_present,
        "token_prefix": settings.HF_API_TOKEN[:6] if token_present else None,
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": "hello world", "options": {"wait_for_model": True}},
            timeout=30,
        )
        result["status_code"] = response.status_code
        result["response_body"] = response.text[:1000]
    except Exception as exc:
        result["exception"] = str(exc)

    return result


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns whether the model/tokenizer have finished loading and are ready to serve predictions.",
)
async def health() -> HealthResponse:
    ready = is_ready()
    return HealthResponse(
        status="ok" if ready else "loading",
        model_loaded=ready,
        model_name=get_model_display_name() if ready else "unknown",
        device=str(get_device()) if ready else "unknown",
    )