import json
from datetime import datetime, timedelta

# === Insight Agent Logic ===
def insight_agent(lease):
    utilization = lease.get("currentUtilization", 0)
    crm_score = lease.get("crmEngagementScore", 0)
    lease_end = datetime.strptime(lease["leaseEndDate"], "%Y-%m-%d")
    days_remaining = (lease_end - datetime.today()).days

    insight = {
        "customerType": "High usage, loyal" if utilization > 85 and crm_score > 8 else "Moderate",
        "upgradePropensity": round(min(1.0, (utilization / 100) * (crm_score / 10)), 2),
        "churnRisk": round(max(0.1, 1 - crm_score / 10), 2),
        "prioritySegment": "Platinum" if crm_score > 8 else "Silver",
        "daysToLeaseEnd": days_remaining,
        # Pass assetType forward for next agent
        "assetType": lease.get("assetType", "Unknown")
    }
    return insight

# === Opportunity Agent Logic ===
def opportunity_agent(insight):
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
    return opportunity

# === Engagement Agent Logic (Simplified) ===
def engagement_agent(combined_data):
    prompt = f"""
You are a proactive sales assistant.
Generate a personalized message for a business customer leasing a {combined_data['assetType']}.
Their lease ends in {combined_data['daysToLeaseEnd']} days.
They have a high usage pattern and CRM score.
Recommended product: {combined_data['recommendedProduct']}.
Justification: {combined_data['justification']}.
Keep the tone professional and brief.
"""

    # Simulate LLM response (replace with Bedrock call in prod)
    simulated_response = f"Hi! Your current {combined_data['assetType']} lease is ending soon. Based on your high usage, we recommend our {combined_data['recommendedProduct']}. Let's discuss how to keep your operations running smoothly!"

    return simulated_response.strip()


# === Main Simulation ===
if __name__ == "__main__":
    # Mock input data (one lease)
    sample_lease = {
        "customerId": "CUST003",
        "assetType": "Excavator",
        "leaseEndDate": (datetime.today() + timedelta(days=30)).strftime("%Y-%m-%d"),
        "currentUtilization": 92,
        "paymentBehavior": "on-time",
        "crmEngagementScore": 9.1,
        "recommendedUpgrade": "Excavator X-Series Bundle"
    }

    print("=== Starting Proactive Sales Agent Workflow Simulation ===\n")

    # Step 1: Insight Agent
    insight = insight_agent(sample_lease)
    print("Insight Agent Output:")
    print(json.dumps(insight, indent=2), "\n")

    # Step 2: Opportunity Agent
    opportunity = opportunity_agent(insight)
    print("Opportunity Agent Output:")
    print(json.dumps(opportunity, indent=2), "\n")

    # Step 3: Combine data and run Engagement Agent
    combined = {**insight, **opportunity}
    message = engagement_agent(combined)
    print("Engagement Agent Output (Sales Message):")
    print(message)
