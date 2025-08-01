import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool
from openai.types.responses import ResponseTextDeltaEvent

# Load environment variables from .env file
load_dotenv(override=True)

# --- Agent Instructions ---
# Each agent has a unique persona and style for writing cold emails.
instructions1 = (
    "You are a professional sales representative at ComplAI — an AI-powered "
    "SaaS platform designed to streamline SOC 2 compliance and audit readiness. "
    "Your focus is on writing serious, polished cold emails tailored for a corporate audience."
)

instructions2 = (
    "You are a witty and charismatic sales agent at ComplAI, an AI-driven "
    "SaaS solution for SOC 2 compliance and audit prep. Your job is to craft cold emails "
    "that are clever, humorous, and attention-grabbing — the kind people actually want to read and reply to."
)

instructions3 = (
    "You are a time-conscious sales rep at ComplAI, a company offering an AI-based "
    "SaaS tool for SOC 2 compliance and audit preparation. Your cold emails are short, sharp, and straight to the point — no fluff, just value."
)

# Function to create the three sales agents
# Returns: Tuple of Agent objects

def create_agents():
    try:
        sales_agent1 = Agent(
            name="Agent1",
            model='gpt-4o-mini',
            instructions=instructions1
        )
        sales_agent2 = Agent(
            name="Agent2",
            model='gpt-4o-mini',
            instructions=instructions2
        )
        sales_agent3 = Agent(
            name="Agent3",
            model='gpt-4o-mini',
            instructions=instructions3
        )
        return sales_agent1, sales_agent2, sales_agent3
    except Exception as e:
        print(f"Error creating agents: {e}")
        raise

# The message prompt for all agents
default_message = "Write a cold email for sales"

# Asynchronously generate cold emails from all agents
# Returns: List of agent responses
async def generate_mails(sales_agent1, sales_agent2, sales_agent3):
    try:
        with trace("Parallel generate sales cold emails"):
            # Run all agents in parallel and gather their responses
            result = await asyncio.gather(
                Runner.run(sales_agent1, default_message),
                Runner.run(sales_agent2, default_message),
                Runner.run(sales_agent3, default_message),
            )
            return result
    except Exception as e:
        print(f"Error generating emails: {e}")
        raise

# Main program logic
def main():
    try:
        # Create the three sales agents
        sales_agent1, sales_agent2, sales_agent3 = create_agents()
        # Generate cold emails from all agents
        emails = asyncio.run(generate_mails(sales_agent1, sales_agent2, sales_agent3))
        # Build the output string with all generated emails
        output = 'Cold emails:\n'
        for email in emails:
            output += email.final_output + '\n\n'
        # Instructions for the sales manager agent
        manager_instruction = (
            "You are a sales force manager. You will be provided with 3 emails written by 3 agents. "
            "You need to choose the best email."
        )
        # Create the sales manager agent
        sales_manager_agent = Agent(
            name="Sales Manager",
            instructions=manager_instruction,
            model="gpt-4o-mini"
        )
        try:
            # Ask the manager agent to pick the best email
            with trace("Pick the final email"):
                final_email = Runner.run(sales_manager_agent, output)
            # Print the best email selected by the manager
            print(final_email.final_output)
        except Exception as e:
            print(f"Error picking the best email: {e}")
    except Exception as e:
        print(f"Fatal error in main: {e}")

# Entry point for the script
if __name__ == "__main__":
    main()






