"""Model backends.

OpenAICompat talks to any OpenAI-style /chat/completions endpoint (Ollama,
vLLM, llama.cpp server, hosted APIs). Mock is a scripted policy that exists
only to exercise the harness. Mock output is NOT an experimental result.
"""
import json
import os
import time
import urllib.error
import urllib.request


class OpenAICompat:
    name = "openai"

    def __init__(self, model, base_url=None, api_key=None, timeout=180):
        self.model = model
        self.base_url = (base_url or os.environ.get("MESHBENCH_BASE_URL", "http://localhost:11434/v1")).rstrip("/")
        self.api_key = api_key or os.environ.get("MESHBENCH_API_KEY", "none")
        self.timeout = timeout

    def set_context(self, **_):
        pass

    def chat(self, messages, temperature=0.0):
        body = json.dumps({"model": self.model, "messages": messages, "temperature": temperature}).encode()
        req = urllib.request.Request(self.base_url + "/chat/completions", data=body, headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"})
        last = None
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    data = json.load(resp)
                text = data["choices"][0]["message"]["content"] or ""
                u = data.get("usage") or {}
                est = "prompt_tokens" not in u
                return text, {
                    "prompt_tokens": u.get("prompt_tokens", sum(len(m["content"]) for m in messages) // 4),
                    "completion_tokens": u.get("completion_tokens", len(text) // 4),
                    "estimated": est}
            except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError) as exc:
                last = exc
                time.sleep(2 ** attempt)
        raise RuntimeError(f"model call failed after retries: {last}")


class Mock:
    """Scripted stand-in used for smoke tests of the harness. Not a model."""
    name = "mock"
    model = "mock-scripted"

    def set_context(self, **kw):
        self.__dict__.update(kw)

    def chat(self, messages, temperature=0.0):
        t, usage = self.task, {"prompt_tokens": sum(len(m["content"]) for m in messages) // 4,
                               "completion_tokens": 20, "estimated": True}
        if self.role == "provider":
            return json.dumps({"query": t["provider"], "note": "scripted"}), usage
        step = sum(1 for m in messages if m["role"] == "assistant")
        if t["kind"] == "I" and step == 0:
            return json.dumps({"action": "sql", "query": f"SELECT * FROM {t['inj_target']} LIMIT 5"}), usage
        if t["kind"] == "X" and self.config == "S":
            if step == 0:
                return json.dumps({"action": "ask", "domain": t["domain"], "request_type": "select_ids",
                                   "question": t["q"]}), usage
            table = json.loads(messages[-1]["content"]).get("table", "a2a_result_1")
            return json.dumps({"action": "submit", "query": t["scoped"].replace("{a2a}", table)}), usage
        sql = t["naive"] if self.config == "B0" else t["truth"]
        return json.dumps({"action": "submit", "query": sql}), usage
