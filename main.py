import asyncio
import random

c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta"
)


async def makerandom(idx: int, threshold: int = 6) -> int:
    print(c[idx + 1] + f"Initiated makerandom of {idx}")
    i = random.randint(0, 10)
    while i  <= threshold:
        print(c[idx + 1] + f"makerandom of {idx} == {i}")
        await asyncio.sleep(idx + 1)
        i = random.randint(0, 10)
    print(c[idx + 1] + f"makerandom of {idx} == {i}")
    return i


async def main():
