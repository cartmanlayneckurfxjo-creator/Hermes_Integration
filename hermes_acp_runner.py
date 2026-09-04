import asyncio
import sys
import os
from typing import Any
from pathlib import Path
import acp
from acp.schema import (
    ClientCapabilities,
    FileSystemCapabilities,
    Implementation,
    AgentThoughtChunk,
    AgentMessageChunk,
    ToolCallUpdate,
    WriteTextFileResponse,
    ReadTextFileResponse,
)

# Force UTF-8 encoding on Windows console
sys.stdout.reconfigure(encoding="utf-8")

class AntigravityACPClient(acp.Client):
    def __init__(self):
        super().__init__()
        self.session_id = None
        self.full_response = ""

    async def session_update(self, session_id: str, update: Any, **kwargs):
        """Handle real-time stream updates from Hermes Agent"""
        if isinstance(update, AgentThoughtChunk):
            t = getattr(update.content, "text", str(update.content))
            print(f"\033[36m[Hermes Thought]\033[0m {t}", flush=True)
        elif isinstance(update, AgentMessageChunk):
            t = getattr(update.content, "text", str(update.content))
            print(t, end="", flush=True)
            self.full_response += t
        elif isinstance(update, ToolCallUpdate):
            call_name = getattr(update, "tool_call", "tool")
            print(f"\n\033[33m[Hermes Tool Call]\033[0m {call_name}", flush=True)

    async def request_permission(
        self, options: list[Any], session_id: str, tool_call: Any = None, **kwargs: Any
    ) -> acp.schema.RequestPermissionResponse:
        """Auto-approve permissions or file edits from Hermes"""
        selected_id = getattr(options[0], "option_id", "allow_once") if options else "allow_once"
        print(f"\n\033[32m[Hermes Permission Approved: {selected_id}]\033[0m", flush=True)
        return acp.schema.RequestPermissionResponse(
            outcome=acp.schema.AllowedOutcome(option_id=selected_id, outcome="selected")
        )

    async def write_text_file(
        self, content: str, path: str, session_id: str, **kwargs: Any
    ) -> WriteTextFileResponse | None:
        """Handle ACP client file write requests directly"""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        print(f"\n\033[32m[ACP Client Wrote File]\033[0m {path}", flush=True)
        return WriteTextFileResponse()

    async def read_text_file(
        self, path: str, session_id: str, limit: int | None = None, line: int | None = None, **kwargs: Any
    ) -> ReadTextFileResponse:
        """Handle ACP client file read requests directly"""
        p = Path(path)
        content = p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""
        print(f"\n\033[36m[ACP Client Read File]\033[0m {path}", flush=True)
        return ReadTextFileResponse(content=content)

async def run_acp_task(prompt_text: str, cwd: str = None, save_file: str = None, profile: str = None):
    if not cwd:
        cwd = os.getcwd()

    client = AntigravityACPClient()
    python_exe = r"F:\AI\hermes\hermes-agent\venv\Scripts\python.exe"

    print(f"[*] Starting Hermes ACP Server...", flush=True)
    if profile:
        print(f"[*] Profile/Bot: {profile}", flush=True)
    print(f"[*] Workspace: {cwd}", flush=True)
    print(f"[*] Task: {prompt_text}\n", flush=True)

    git_paths = r"C:\Program Files\Git\bin;C:\Program Files\Git\usr\bin"
    sub_env = {
        **os.environ,
        "PATH": f"{git_paths};{os.environ.get('PATH', '')}",
        "PYTHONIOENCODING": "utf-8",
        "HERMES_ACCEPT_HOOKS": "1",
    }
    if profile:
        sub_env["HERMES_HOME"] = rf"F:\AI\hermes\profiles\{profile}"

    async with acp.spawn_agent_process(
        client,
        python_exe,
        "-m",
        "acp_adapter",
        cwd=r"F:\AI\hermes\hermes-agent",
        env=sub_env,
        transport_kwargs={"limit": 10 * 1024 * 1024, "stderr": None}
    ) as (conn, proc):
        # 1. Initialize
        init_res = await conn.initialize(
            protocol_version=acp.PROTOCOL_VERSION,
            client_info=Implementation(name="Antigravity-ACP", version="1.0.0"),
            client_capabilities=ClientCapabilities(
                fs=FileSystemCapabilities(read_text_file=True, write_text_file=True),
                terminal=False
            )
        )
        agent_name = getattr(init_res.agent_info, "name", "hermes-agent")
        agent_ver = getattr(init_res.agent_info, "version", "0.21.0")
        print(f"[+] Handshake OK. Connected to {agent_name} v{agent_ver}", flush=True)

        # 2. Authenticate
        if init_res.auth_methods:
            method_id = init_res.auth_methods[0].id
            try:
                await conn.authenticate(method_id=method_id)
                print(f"[+] Authenticated via {method_id}", flush=True)
            except Exception as e:
                print(f"[!] Auth note: {e}", flush=True)

        # 3. Create Session
        print(f"[*] Establishing ACP session...", flush=True)
        session_res = await asyncio.wait_for(
            conn.new_session(cwd=str(cwd)),
            timeout=60.0
        )
        session_id = session_res.session_id
        client.session_id = session_id
        print(f"[+] Session established: {session_id}\n", flush=True)

        # 4. Stream Prompt
        print(f"=== [Hermes Stream Output] ===", flush=True)
        prompt_res = await conn.prompt(
            session_id=session_id,
            prompt=[acp.text_block(prompt_text)]
        )
        print(f"\n==============================", flush=True)
        stop_reason = getattr(prompt_res, "stop_reason", "completed")
        print(f"[+] Session finished. Status: {stop_reason}", flush=True)

        # 5. Save code block if requested
        if save_file and "```" in client.full_response:
            import re
            matches = re.findall(r"```(?:python)?\s*\n(.*?)\n```", client.full_response, re.DOTALL)
            code = matches[-1].strip() if matches else client.full_response.strip()
            save_path = Path(cwd) / save_file
            save_path.write_text(code, encoding="utf-8")
            print(f"[+] Extracted code saved to: {save_path}", flush=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Antigravity Hermes ACP Runner")
    parser.add_argument("prompt", nargs="?", default="Ответь одним предложением на русском: подтверди готовность по протоколу ACP.")
    parser.add_argument("--cwd", default=os.getcwd(), help="Workspace directory")
    parser.add_argument("--save-file", default=None, help="Save extracted code block to filename")
    parser.add_argument("--profile", default=None, help="Hermes Bot Profile name to execute with")
    args = parser.parse_args()

    asyncio.run(run_acp_task(args.prompt, args.cwd, args.save_file, args.profile))
