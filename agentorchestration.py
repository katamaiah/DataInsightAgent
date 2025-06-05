from langchain.agents import Tool, initialize_agent
from langchain.llms import OpenAI

# Your Insight Agent as a Tool (Python function)
def insight_tool_fn(lease):
    utilization = lease.get("currentUtilization", 0)
    crm_score = lease.get("crmEngagementScore", 0)
    days_to_end = 30
    return f"Insight: utilization={utilization}, crm_score={crm_score}, days_to_end={days_to_end}"

insight_tool = Tool(
    name="Insight Agent",
    func=insight_tool_fn,
    description="Generate leasing usage and engagement insights"
)

# Opportunity Agent Tool
def opportunity_tool_fn(insight_str):
    # Parse insight_str or assume inputs; simplified here
    return "Opportunity: Recommend 'Excavator X-Series Bundle' due to high usage."

opportunity_tool = Tool(
    name="Opportunity Agent",
    func=opportunity_tool_fn,
    description="Generate product upgrade opportunities based on insights"
)

# Engagement Agent Tool (calls LLM with prompt)
llm = OpenAI(temperature=0)

def engagement_tool_fn(input_str):
    prompt = f"Generate a sales message based on: {input_str}"
    return llm(prompt)

engagement_tool = Tool(
    name="Engagement Agent",
    func=engagement_tool_fn,
    description="Generate a personalized sales message"
)

tools = [insight_tool, opportunity_tool, engagement_tool]

# Initialize an agent that can pick tools dynamically
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Example input (lease data as string or dict)
lease_data_str = '{"assetType":"Excavator","currentUtilization":92,"crmEngagementScore":9.1}'

# Run agent with input
response = agent.run(lease_data_str)
print(response)
