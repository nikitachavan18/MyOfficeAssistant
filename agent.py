"""Agent loop using Groq's free, OpenAI-compatible API.
Flow: send message -> model may call tools -> run tools -> repeat."""
import json
import os
 
from dotenv import load_dotenv
from openai import OpenAI
 
from tools import FUNCTIONS, TOOL_SCHEMAS
 
load_dotenv(override=True)
 
API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://api.groq.com/openai/v1")
MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")
MAX_STEPS = 8  # safety limit on tool-call rounds
 
SYSTEM_PROMPT = """You are an Office Assistant AI agent.
You help with: managing tasks, scheduling meetings, saving and searching notes,
drafting professional emails, and summarizing text.
Rules:
- Call get_datetime first when the user uses relative dates like 'tomorrow'.
- Use tools to read or change tasks, meetings and notes. Never invent their contents.
- Draft emails and summaries yourself in your reply (no tool needed).
- Be concise and professional. Confirm what you did after using a tool."""
 
# Convert our tool schemas to the OpenAI/Groq format
OPENAI_TOOLS = [
    {"type": "function",
     "function": {"name": t["name"],
                  "description": t["description"],
                  "parameters": t["input_schema"]}}
    for t in TOOL_SCHEMAS
]
 
 
class MyOfficeAgent:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
 
    def chat(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})
 
        for _ in range(MAX_STEPS):
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=self.history,
                tools=OPENAI_TOOLS,
                max_tokens=1000,
            )
            msg = response.choices[0].message
 
            # Save the assistant turn (text and/or tool calls)
            assistant = {"role": "assistant", "content": msg.content or ""}
            if msg.tool_calls:
                assistant["tool_calls"] = [
                    {"id": tc.id, "type": "function",
                     "function": {"name": tc.function.name,
                                  "arguments": tc.function.arguments}}
                    for tc in msg.tool_calls
                ]
            self.history.append(assistant)
 
            # No tool requested -> this is the final answer
            if not msg.tool_calls:
                return msg.content or ""
 
            # Run every requested tool and send results back
            for tc in msg.tool_calls:
                try:
                    args = json.loads(tc.function.arguments or "{}")
                    output = FUNCTIONS[tc.function.name](**args)
                except Exception as e:
                    output = {"error": str(e)}
                print(f"  [tool] {tc.function.name}({tc.function.arguments})")
                self.history.append({"role": "tool",
                                     "tool_call_id": tc.id,
                                     "content": json.dumps(output)})
 
        return "Sorry, I hit my step limit. Please try a simpler request."
 