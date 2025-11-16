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
 
print(f"The square root of 625 is {response.output.value}")