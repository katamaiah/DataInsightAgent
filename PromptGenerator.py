def generate_safe_prompt(lease):
    # Mask and categorize
    sector = infer_sector(lease["assetType"])
    utilization = "high" if lease["currentUtilization"] >= 85 else "moderate"
    crm_level = categorize_score(lease["crmEngagementScore"])

    prompt = f"""
A customer from the {sector} sector (Customer A) has a lease for a {lease['assetType']} expiring on {lease['leaseEndDate']}.
Utilization is {utilization} ({lease['currentUtilization']}%), payment behavior is {lease['paymentBehavior']},
CRM engagement is {crm_level} (score: {lease['crmEngagementScore']}).

Recommend a proactive sales message for this customer.
Suggested upgrade: {lease['recommendedUpgrade']}.
"""
    return prompt.strip()


def infer_sector(asset_type):
    mapping = {
        "Forklift": "manufacturing",
        "Mini Van": "logistics",
        "Excavator": "construction",
        "Truck": "transport"
    }
    return mapping.get(asset_type, "industrial")


def categorize_score(score):
    if score >= 8:
        return "high"
    elif score >= 5:
        return "medium"
    else:
        return "low"
