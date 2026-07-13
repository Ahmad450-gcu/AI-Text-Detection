const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

class ApiError extends Error {
    constructor(message, status) {
        super(message);
        this.name = "ApiError";
        this.status = status;
    }
}

export async function checkHealth() {
    const response = await fetch(`${API_BASE_URL}/api/v1/health`);
    if (!response.ok) {
        throw new ApiError(
            `Health check failed (${response.status})`,
            response.status,
        );
    }
    return response.json();
}

export async function predictText(text) {
    let response;
    try {
        response = await fetch(`${API_BASE_URL}/api/v1/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text }),
        });
    } catch {
        throw new ApiError(
            `Can't reach the backend at ${API_BASE_URL}. Make sure it's running.`,
            0,
        );
    }

    if (response.status === 200) {
        return response.json();
    }

    if (response.status === 422) {
        const body = await response.json().catch(() => null);
        const detail = body?.detail;
        const message = Array.isArray(detail)
            ? detail.map((item) => item.msg).join(", ")
            : "Please enter some text to analyze.";
        throw new ApiError(message, 422);
    }

    if (response.status === 503) {
        throw new ApiError(
            "The model is still loading on the backend. Try again in a few seconds.",
            503,
        );
    }

    const body = await response.json().catch(() => null);
    throw new ApiError(
        body?.detail || `Something went wrong (${response.status}).`,
        response.status,
    );
}

export { API_BASE_URL, ApiError };
