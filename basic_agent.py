import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, trace

load_dotenv(override=True)

async def main():
    agent = Agent(
        name="Motivator",
        instructions="You are a greate philosophers",
        model="gpt-4o-mini"
    )
    with trace("Every Day Motivation"):
        result = await Runner.run(
            agent,
            "Tell me a quotation of the day for movtivation"
        )
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())


