import requests

url = "https://linkedin-content-creator-v1-0b978965-52ca-4-c0653850.crewai.com/kickoff"
# headers = {"Authorization": "Bearer d959c6af8d91"}

# response = requests.get(url, headers=headers)
# print(response.json())


headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer d959c6af8d91"
}
# data = {
#     "inputs": {
#         "topic": "AI Agent Frameworks"
#     }
# }

# response = requests.post(url, headers=headers, json=data)
# print(response.json())

url = "https://linkedin-content-creator-v1-0b978965-52ca-4-c0653850.crewai.com/status/1725ec4f-f798-4b59-b646-e864d9493933"
response = requests.get(url, headers=headers)
print(response.json())