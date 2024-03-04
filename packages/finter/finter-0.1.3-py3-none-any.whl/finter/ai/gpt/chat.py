import requests


def chat_gpt(input_text):
    url = "http://localhost:8282/gpt"
    data = {"input": input_text}

    response = requests.post(url, json=data)
    return response.json()["result"]


if __name__ == "__main__":
    input_text = "Hello, how are you?"
    chat_gpt(input_text)
