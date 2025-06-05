from langchain.agents import Tool, initialize_agent
from langchain.llms import OpenAI
import json
from datetime import datetime

# --- Insight Agent as a Tool ---
def insight_agent_tool_fn(lease_json_str: str) -> str:
    lease = json.loads(lease_json_str)
    utilization = lease.get("currentUtilization", 0)
    crm_score = lease.get("crmEngagementScore", 0)
    lease_end_date = lease.get("leaseEndDate", "2025-12-31")
    lease_end = datetime.strptime(lease_end_date, "%Y-%m-%d")
    days_remaining = (lease_end - datetime.today()).days

    insight = {
        "customerType": "High usage, loyal" if utilization > 85 and crm_score > 8 else "Moderate",
        "upgradePropensity": round(min(1.0, (utilization / 100) * (crm_score / 10)), 2),
        "churnRisk": round(max(0.1, 1 - crm_score / 10), 2),
        "prioritySegment": "Platinum" if crm_score > 8 else "Silver",
        "daysToLeaseEnd": days_remaining,
        "assetType": lease.get("assetType", "Unknown")
    }
    return json.dumps(insight)

insight_tool = Tool(
    name="Insight Agent",
    func=insight_agent_tool_fn,
    description="Generates leasing usage and engagement insights from customer lease data in JSON string format."
)

# --- Opportunity Agent as a Tool ---
def opportunity_agent_tool_fn(insight_json_str: str) -> str:
    insight = json.loads(insight_json_str)
    asset_type = insight.get("assetType", "")
    upgrade_propensity = insight.get("upgradePropensity", 0)
    days_to_end = insight.get("daysToLeaseEnd", 90)

    offers = {
        "Forklift": "Forklift Premium Plan",
        "Excavator": "Excavator X-Series Bundle",
        "Mini Van": "Fleet Flex Lease Plan",
        "Truck": "Truck Performance Plus Plan"
    }

    product = offers.get(asset_type, "Standard Lease Upgrade")

    opportunity = {
        "recommendedProduct": product,
        "justification": "High utilization and engagement" if upgrade_propensity > 0.8 else "Moderate likelihood to upgrade",
        "urgency": f"Lease ends in {days_to_end} days",
        "assetType": asset_type,
        "daysToLeaseEnd": days_to_end
    }
    return json.dumps(opportunity)

opportunity_tool = Tool(
    name="Opportunity Agent",
    func=opportunity_agent_tool_fn,
    description="Generates product upgrade opportunity based on insights in JSON string format."
)

# --- Engagement Agent as a Tool ---
llm = OpenAI(temperature=0)

def engagement_agent_tool_fn(opportunity_json_str: str) -> str:
    opportunity = json.loads(opportunity_json_str)
    prompt = f"""
You are a proactive sales assistant.
Generate a personalized message for a business customer leasing a {opportunity['assetType']}.
Their lease ends in {opportunity['daysToLeaseEnd']} days.
Recommended product: {opportunity['recommendedProduct']}.
Justification: {opportunity['justification']}.
Keep the tone professional and brief.
"""
    response = llm(prompt)
    return response

engagement_tool = Tool(
    name="Engagement Agent",
    func=engagement_agent_tool_fn,
    description="Generates a personalized sales message given opportunity details in JSON string format."
)

# --- Initialize Agent with tools ---
tools = [insight_tool, opportunity_tool, engagement_tool]

agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

# --- Example input ---
lease_data = {
    "customerId": "CUST1001",
    "assetType": "Excavator",
    "leaseEndDate": "2025-06-20",
    "currentUtilization": 92,
    "paymentBehavior": "on-time",
    "crmEngagementScore": 9.1
}

lease_data_str = json.dumps(lease_data)

# --- Run the agent ---
if __name__ == "__main__":
    print("Running LangChain Agent with leasing data...\n")
    result = agent.run(lease_data_str)
    print("\nFinal Sales Message:")
    print(result)
