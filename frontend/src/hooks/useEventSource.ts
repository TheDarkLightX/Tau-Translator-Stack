import { useEffect, useRef } from "react";
export function useEventSource(url: string, onMessage: (ev: MessageEvent) => void) {
  const ref = useRef<EventSource | null>(null);
  useEffect(() => {
    if (!url) return;
    ref.current?.close();
    const es = new EventSource(url);
    es.onmessage = onMessage;
    ref.current = es;
    return () => es.close();
  }, [url, onMessage]);
}
