import requests

def question(content):  
    url = "https://datugoku.chat/api/chat"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Accept": "*/*",
        "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": content}]
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            return response.text
    else:
        return {"error": f"Failed to fetch response from datugoku API, Status Code: {response.status_code}"}
