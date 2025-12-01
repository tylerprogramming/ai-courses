from agents import Agent, Runner, SQLiteSession

from dotenv import load_dotenv

load_dotenv()

# Create agent
agent = Agent(
    name="Assistant",
    instructions="Reply very concisely.",
)

# Create a session instance
session_alice = SQLiteSession("alice", "conversations.db")
session_bob = SQLiteSession("bob", "conversations.db")

# First turn
# result = Runner.run_sync(
#     agent,
#     "My name is Alice, I love hiking and photography.",
#     session=session_alice
# )
# print(result.final_output)  

# result = Runner.run_sync(
#     agent,
#     "My name is Bob, I love swimming and reading.",
#     session=session_bob
# )
# print(result.final_output)  


result = Runner.run_sync(
    agent,
    "What are Alice and Bob's hobbies?",
    session=session_bob
)
print(result.final_output) 

# Nice to meet you, Alice! Hiking and photography make a perfect combo for stunning adventure memories.
# Nice to meet you, Bob! Swimming and reading are great hobbies.
# Alice’s hobbies: hiking, photography.  
# Bob’s hobbies: (not specified).