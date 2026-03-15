from openai import OpenAI
import json

from tools import (
    search_work_orders,
    get_work_order_details,
    get_available_technicians,
    search_parts,
    get_customer_details,
    get_customer_equipment,
    get_equipment_details,
)

from tool_definitions import TOOLS

TOOL_FUNCTIONS = {
    "search_work_orders": search_work_orders,
    "get_work_order_details": get_work_order_details,
    "get_available_technicians": get_available_technicians,
    "search_parts": search_parts,
    "get_customer_details": get_customer_details,
    "get_customer_equipment": get_customer_equipment,
    "get_equipment_details": get_equipment_details,
}

client = OpenAI(
    base_url="http://localhost:11434/v1/",
    api_key="ollama",  # not required for local ollama
)

MODEL = "qwen3.5:9b"

SYSTEM_PROMPT = """You are an expert field service technician assistant working 
in Queensland, Australia. You support HVAC, electrical, plumbing, and 
refrigeration technicians in the field.

Your responsibilities:
- Provide step-by-step troubleshooting procedures
- Always prioritize safety — mention relevant safety procedures first
- Reference Australian standards (AS/NZS) when applicable
- Recommend escalation to a senior technician when appropriate
- Be concise and practical — technicians are on-site and need actionable advice

Safety rules you must always follow:
- For gas leaks: always instruct to evacuate first, call 000, never operate electrical switches
- For electrical work: always mention lockout/tagout before any procedure
- For refrigerant handling: always note that ARCtick licence is required in Australia
- For working at heights: always reference fall protection requirements

You work for a company that services commercial buildings, industrial facilities, 
and residential properties across the Brisbane metropolitan area.
"""


def call_tool(tool_name: str, arguments: dict) -> str:
    tool = TOOL_FUNCTIONS.get(tool_name)
    if not tool:
        return f"Error: Unknown tool '{tool_name}'"

    try:
        result = tool(**arguments)
        return result
    except Exception as e:
        return f"Error calling {tool_name}: {str(e)}"


def get_response(history: list) -> str:

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=history,
            tools=TOOLS,
        )

        message = response.choices[0].message

        if message.tool_calls:
            history.append(
                {
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in message.tool_calls
                    ],
                }
            )

            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                print(f"Calling tool: {func_name}({arguments})")

                result = call_tool(func_name, arguments)

                history.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )

            continue

        else:
            assistant_text = message.content
            history.append({"role": "assistant", "content": assistant_text})
            return assistant_text


def chat():
    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    print()
    print("Type 'bye' to exit, 'history' to view chat history, 'clear' to reset.")
    print()
    print("Hi! I'm your Field Service AI Assistant. How can I help you today?")
    print()

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() == "bye":
            print()
            print("Goodbye!")
            print()
            break

        if user_input.lower() == "history":
            for msg in history:
                print(f"{msg['role']}: \n{msg.get('content', '')}\n")
            continue

        if user_input.lower() == "clear":
            history = [{"role": "system", "content": SYSTEM_PROMPT}]
            continue

        history.append({"role": "user", "content": user_input})

        print()
        assistant_response = get_response(history)
        print(f"Assistant: {assistant_response}\n")


if __name__ == "__main__":
    chat()
