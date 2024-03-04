from openai import OpenAI

from zshgpt.util.messages import messages


def model_selection(user_query: str) -> str:
    match user_query.strip()[:2]:
        case '#':
            return 'gpt-3.5-turbo'
        case '##':
            return 'gpt-4'
        case _:
            return 'gpt-3.5-turbo'


def get_message(user_query: str) -> str:
    client = OpenAI()
    model = model_selection(user_query)
    response = client.chat.completions.create(
        model=model, messages=[*messages, {'role': 'user', 'content': user_query}]
    )
    return response.choices[0].message
