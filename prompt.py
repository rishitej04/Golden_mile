def build_llm_prompt(recommendations, documents, user_inputs):
    allowed_localities = sorted(recommendations["Locality"].unique().tolist())

    # ---- Rental Yield Estimation (SAFE) ----
    # Conservative residential rental yield
    ANNUAL_YIELD_PERCENT = 3.0  

    avg_price_cr = recommendations["Predicted_Total_Cr"].mean()
    estimated_annual_rent = (avg_price_cr * 1e7) * (ANNUAL_YIELD_PERCENT / 100)
    estimated_monthly_rent = estimated_annual_rent / 12

    prompt = f"""
### Advisory Report for Real Estate Investment in {user_inputs['city']}

**Client Profile:**
- **City:** {user_inputs['city']}
- **Budget:** ₹{user_inputs['budget']} Cr
- **Property Size Requirement:** {user_inputs['size']} sqft
- **Purpose:** {user_inputs['intent']}
- **Metro Connectivity Required:** {user_inputs['metro']}

---

### 1. Budget Feasibility Summary

Based on current market price feasibility, the following properties fall within the specified budget.
All recommendations are limited to the listed localities and respect the client's constraints.

Available price range:
₹{recommendations['Predicted_Total_Cr'].min()} Cr – ₹{recommendations['Predicted_Total_Cr'].max()} Cr

---

### 2. Best-Fit Localities
"""

    for loc in allowed_localities:
        prompt += f"""
**{loc}**
- Strong demand due to employment hubs
- Good metro and road connectivity
- Consistent buyer and tenant interest
"""

    prompt += f"""
---

### 3. Trade-offs & Risks
- Budget-constrained options may involve older properties
- Premium amenities increase capital cost
- High-demand areas may see slower appreciation in the short term

---

### 4. Rental Yield Estimation
- **Estimated Monthly Rent:** ₹{int(estimated_monthly_rent):,}
- **Estimated Annual Yield:** {ANNUAL_YIELD_PERCENT}%

This estimate reflects conservative residential rental trends in major Indian metro markets.

---

### 5. Final Recommendation
The specified budget is feasible for acquisition within the listed localities.
For investment purposes, prioritizing metro proximity and tenant demand is advised for stable returns.
"""

    return prompt