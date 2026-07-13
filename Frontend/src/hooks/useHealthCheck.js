import { useEffect, useState } from "react";
import { checkHealth } from "../api/client.js";

export function useHealthCheck() {
  const [status, setStatus] = useState("checking");
  const [detail, setDetail] = useState(null);

  useEffect(() => {
    let cancelled = false;

    checkHealth()
      .then((data) => {
        if (cancelled) return;
        setDetail(data);
        setStatus(data.model_loaded ? "ready" : "loading");
      })
      .catch(() => {
        if (cancelled) return;
        setStatus("unreachable");
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return { status, detail };
}
