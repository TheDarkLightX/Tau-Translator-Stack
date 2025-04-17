import os, asyncio, tempfile, subprocess, time
from openai import AsyncOpenAI

async def model_chain(client: AsyncOpenAI):
    avail = os.getenv("AVAILABLE_MODELS", "gpt-4o,gpt-4o-mini,o3").split(",")
    for model in avail:
        try:
            await client.models.retrieve(model)
            return model
        except Exception:
            continue
    raise RuntimeError("No OpenAI model available")

def parse_ok(tau_code: str) -> bool:
    proc = subprocess.run(["tau", "--parse"], input=tau_code.encode(), capture_output=True)
    return proc.returncode == 0

async def run_tau(tau_code: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tau") as tmp:
        tmp.write(tau_code.encode())
        tmp.flush()
        proc = await asyncio.create_subprocess_exec(
            "tau", tmp.name, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        async for line in proc.stdout:
            yield line.decode()
