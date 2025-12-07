import autogen
import dotenv
import os

from typing import Literal
from typing_extensions import Annotated
from autogen import AssistantAgent, UserProxyAgent, LLMConfig, register_function

dotenv.load_dotenv()

config_list = [
    {
        "model": os.getenv("model"),
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
]

llm_config = LLMConfig.from_json(path="OAI_CONFIG_LIST.json")

currency_bot = AssistantAgent(
    name="currency_bot",
    system_message="For currency exchange tasks, only use the functions you have been provided with. Reply TERMINATE "
                   "when the task is done.",
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config= {
        "work_dir": "code",
        "use_docker": False
    }
)

CurrencySymbol = Literal["USD", "EUR"]


def exchange_rate(base_currency: CurrencySymbol, quote_currency: CurrencySymbol) -> float:
    if base_currency == quote_currency:
        return 1.0
    elif base_currency == "USD" and quote_currency == "EUR":
        return 1 / 0.86
    elif base_currency == "EUR" and quote_currency == "USD":
        return 1.16
    else:
        raise ValueError(f"Unknown currencies {base_currency}, {quote_currency}")

def currency_calculator(
        base_amount: Annotated[float, "Amount of currency in base_currency"],
        base_currency: Annotated[CurrencySymbol, "Base currency"] = "USD",
        quote_currency: Annotated[CurrencySymbol, "Quote currency"] = "EUR",
) -> str:
    quote_amount = exchange_rate(base_currency, quote_currency) * base_amount
    return f"{quote_amount} {quote_currency}"

# Register tool
register_function(
    currency_calculator,
    caller=currency_bot,
    executor=user_proxy,
    description="Currency exchange calculator.",
)

# start the conversation
user_proxy.initiate_chat(
    currency_bot,
    message="How much is 123.45 USD in EUR?",
)
