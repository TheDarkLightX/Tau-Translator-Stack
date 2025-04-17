export async function executeTau(tau: string) {
  const res = await fetch("/v1/execute", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tau })
  });
  return res.body;
}
