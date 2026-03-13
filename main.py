from openai import OpenAI


def main():
    client = OpenAI(
        base_url="http://localhost:11434/v1/",
        api_key="ollama",  # not required for local ollama
    )

    response = client.chat.completions.create(
        model="qwen3.5:9b",
        messages=[{"role": "user", "content": "Say this is a test"}],
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
