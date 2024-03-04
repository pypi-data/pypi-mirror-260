from hyperchain.chain import FunctionChain
from time import sleep

import asyncio

async def sleep_and_x(x):
    print("SLEEP_START")
    await asyncio.sleep(1)
    print("SLEEP_END")
    return {"code": "SLEEP", "ab": "a"}

async def no_sleep_and_x(x):
    print("NOSLEEP")
    return {"code": "NO_SLEEP"}

async def edit_x(x):
    print("EDIT")
    return {"code": x["code"]+"!!"}

chain = FunctionChain(no_sleep_and_x, ["1"], ["code"]) + FunctionChain(sleep_and_x, ["code"], ["code"]) + FunctionChain(edit_x, ["code"], ["code"]) + FunctionChain(no_sleep_and_x, ["1"], ["code"])

chain_linear = FunctionChain(no_sleep_and_x) + FunctionChain(sleep_and_x) + FunctionChain(edit_x) + FunctionChain(no_sleep_and_x)

chain_alt = FunctionChain(no_sleep_and_x, ["code"], ["code"]) + FunctionChain(sleep_and_x, ["code"], ["code"]) + FunctionChain(edit_x, [], ["code"]) + FunctionChain(no_sleep_and_x, ["1"], ["code"])

print(chain.run(code="abc"))
print(chain_linear.run(code="abc"))
print(chain_alt.run(code="abc"))