import requests

ngrokURL = "https://4592-2402-d000-a500-56b9-a8ab-99d9-85b6-3f42.ngrok-free.app"
# ngrokURL = "http://localhost:8000"

# POST request data to be sent
classify = {
  "inputs": '''I am your enemy''',
  "parameters": {"temperature":0.1,
                 "max_new_tokens":200}
}

prompt = "Who is Isurika Ruwani Wickramasinghe?"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
]
generate = {
  "inputs": messages,
  "parameters": {"max_new_tokens":100}
}

# POST request
# response = requests.post(ngrokURL + "/classify/", json=classify)
response = requests.post(ngrokURL + "/generate/", json=generate)

# Response checker
if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print("Request failed with status code:", response.status_code)