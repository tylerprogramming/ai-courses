from arcadepy import Arcade
from dotenv import load_dotenv
import os

load_dotenv()

user_id = "tylerreedytlearning@gmail.com"

client = Arcade(api_key=os.getenv("ARCADE_API_KEY"))

response = client.tools.execute(
    tool_name="Math.Sqrt",
    input={"a": '625'},
    user_id=user_id,
)

# auth_response = client.tools.authorize(
#     tool_name="GitHub.SetStarred",
#     user_id=user_id,
# )
 
# if auth_response.status != "completed":
#     print(f"Click this link to authorize: `{auth_response.url}`. The process will continue once you have authorized the app." ) # Wait for the user to authorize the app
#     client.auth.wait_for_completion(auth_response.id);
 
# response = client.tools.execute(
#     tool_name="GitHub.SetStarred",
#     input={
#         "owner": "ArcadeAI",
#         "name": "arcade-mcp",
#         "starred": True,
#     },
#     user_id=user_id,
# )
 
# print(response.output.value)
 
print(f"The square root of 625 is {response.output.value}")