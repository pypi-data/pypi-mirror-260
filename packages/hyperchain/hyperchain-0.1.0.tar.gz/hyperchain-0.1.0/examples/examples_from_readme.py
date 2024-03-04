from hyperchain.prompt_templates import ChatTemplate

template = ChatTemplate(
    [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "{question}"},
    ],
)

from hyperchain.prompt_templates import MaskToSentinelTemplate

template = MaskToSentinelTemplate("{masked_code}")

print(template.format(masked_code="def greet_user(<mask>: User):\n  print('Hi,' + <mask>)\n"))

from hyperchain.llm_runners import OpenAIRunner

llm_runner = OpenAIRunner(
    model="MODEL",
    api_key="OPENAI_API_KEY",
    model_params={"max_tokens": 500},
)

from hyperchain.chain import LLMChain

chain = LLMChain(
   template=template,
   llm_runner=llm_runner,
   output_name="answer",
)

