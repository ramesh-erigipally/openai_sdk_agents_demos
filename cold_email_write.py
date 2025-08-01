import os
import asyncio
from typing import List
from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv(override=True)

def get_sales_agents() -> List[Agent]:
    """Create and return a list of sales agents with different instructions."""
    instructions = [
        (
            "You are a professional sales representative at ComplAI — an AI-powered "
            "SaaS platform designed to streamline SOC 2 compliance and audit readiness. "
            "Your focus is on writing serious, polished cold emails tailored for a corporate audience."
        ),
        (
            "You are a witty and charismatic sales agent at ComplAI, an AI-driven "
            "SaaS solution for SOC 2 compliance and audit prep. Your job is to craft cold emails "
            "that are clever, humorous, and attention-grabbing — the kind people actually want to read and reply to."
        ),
        (
            "You are a time-conscious sales rep at ComplAI, a company offering an AI-based "
            "SaaS tool for SOC 2 compliance and audit preparation. Your cold emails are short, sharp, and straight to the point — no fluff, just value."
        ),
    ]
    return [
        Agent(name=f"Agent{i+1}", model="gpt-4o-mini", instructions=inst)
        for i, inst in enumerate(instructions)
    ]

def get_sales_manager_agent() -> Agent:
    """Create and return the sales manager agent."""
    manager_instruction = (
        "You are a sales force manager. You will be provided with 3 emails written by 3 agents. "
        "You need to choose the best email."
    )
    return Agent(
        name="Sales Manager",
        instructions=manager_instruction,
        model="gpt-4o-mini",
    )

async def generate_emails(agents: List[Agent], message: str) -> List[str]:
    """Generate cold emails from a list of agents."""
    with trace("Parallel generate sales cold emails"):
        results = await asyncio.gather(*(Runner.run(agent, message) for agent in agents))
        return [email.final_output for email in results]

async def pick_best_email(manager_agent: Agent, emails: List[str]) -> str:
    """Ask the manager agent to pick the best email from the list."""
    output = "Cold emails:\n" + "\n\n".join(emails) + "\n"
    with trace("Pick the final email"):
        final_email = await Runner.run(manager_agent, output)
    return final_email.final_output

async def main() -> None:
    """Main entry point for generating and selecting the best cold email."""
    agents = get_sales_agents()
    message = "Write a cold email for sales"
    emails = await generate_emails(agents, message)
    manager_agent = get_sales_manager_agent()
    best_email = await pick_best_email(manager_agent, emails)
    print("Best cold email:\n")
    print(best_email)

if __name__ == "__main__":
    asyncio.run(main())
