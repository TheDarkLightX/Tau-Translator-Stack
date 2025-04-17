import { useState, useCallback } from "react";
import { useEventSource } from "./hooks/useEventSource";
import { executeTau } from "./api";

export default function App() {
  const [english, setEnglish] = useState("");
  const [tau, setTau] = useState("");
  const [log, setLog] = useState("");
  const [esActive, setEsActive] = useState(false);

  const translate = async () => {
    setTau("");
    setLog("");
    setEsActive(true);
    const res = await fetch("/v1/translate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ english }),
    });
    if (res.status !== 200) {
      alert("Translate failed");
      setEsActive(false);
    }
  };

  useEventSource(esActive ? "/v1/translate" : "", (evt) => {
    const data = JSON.parse(evt.data);
    if (evt.type === "tau") {
      setTau((t) => t + data.chunk);
    } else if (evt.type === "done") {
      setEsActive(false);
    } else if (evt.type === "error") {
      alert(data);
      setEsActive(false);
    }
  });

  const runTau = useCallback(async () => {
    const body = await executeTau(tau);
    if (!body) return;
    const reader = body.getReader();
    const decoder = new TextDecoder();
    let txt = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      txt += decoder.decode(value);
      setLog(txt);
    }
  }, [tau]);

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: 20 }}>
      <textarea
        rows={3}
        style={{ width: '100%' }}
        placeholder="Describe behaviour..."
        value={english}
        onChange={(e) => setEnglish(e.target.value)}
      />
      <div>
        <button onClick={translate}>Translate</button>
        <button onClick={runTau}>Run on Tau</button>
      </div>
      <pre style={{ background: '#f0f0f0', padding: 10 }}>{tau}</pre>
      <pre style={{ background: '#000', color: '#0f0', padding: 10, height: 200, overflowY: 'auto' }}>{log}</pre>
    </div>
  );
}
