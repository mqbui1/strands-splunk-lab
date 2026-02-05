from strands import Agent

# Initialize the agent
agent = Agent()

# Example: send a test request
if __name__ == "__main__":
    response = agent("Hello from Strands Agent!")
    print("Agent response:", response)
