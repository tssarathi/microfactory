from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1/",
    api_key="ollama",  # not required for local ollama
)


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


def main():

    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        if user_input.lower() == "history":
            print("\nHistory")
            for message in history:
                print(f"{message['role']}: \n{message['content']}\n")
            continue

        if user_input.lower() == "clear":
            history = [{"role": "system", "content": "you're a helpful assistant."}]
            continue

        history.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gemma3:4b",
            messages=history,
        )

        assistant_message = response.choices[0].message.content

        history.append({"role": "assistant", "content": assistant_message})

        print(f"\nAssistant: {assistant_message}\n")


if __name__ == "__main__":
    main()
