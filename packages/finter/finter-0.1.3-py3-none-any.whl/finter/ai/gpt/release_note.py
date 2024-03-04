import os
import sys

import requests


def get_logs():
    diff_script_path = os.path.join(os.path.dirname(__file__), "tag_diff_logs.sh")
    with os.popen(f"bash {diff_script_path}") as p:
        output = p.read()
    return output


def generate_release_note(user_prompt=""):
    url = "http://localhost:8282/release_note"
    data = {"logs": get_logs(), "user_prompt": user_prompt}
    response = requests.post(url, json=data)
    return response.json()["result"]


if __name__ == "__main__":
    user_prompt = sys.argv[1] if len(sys.argv) > 1 else ""
    rel = generate_release_note(user_prompt)
    print(rel)
