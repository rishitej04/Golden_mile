from retriever import retrieve_docs
from recommender import recommend_properties
from prompt import build_response

print("Select mode:")
print("1. Budget-based Recommendation")
print("2. Market Insight Q&A")

choice = input("Enter choice (1/2): ").strip()

# ---------------------------------
# MODE 1: Budget-based Recommendation
# ---------------------------------
if choice == "1":
    budget = float(input("Enter budget (Cr): "))
    size = int(input("Enter size (sqft): "))
    metro = input("Near metro? (yes/no): ").lower() == "yes"

    # Optional city preference
    city_pref = input("Preferred city (Hyderabad/Bengaluru/Pune or press Enter for any): ").strip()
    city_pref = city_pref if city_pref else None

    # Get recommendations
    recs = recommend_properties(
        budget_cr=budget,
        size_sqft=size,
        near_metro=metro,
        preferred_city=city_pref
    )

    if recs.empty:
        print("\n❌ No properties found within the given criteria.")
    else:
        # 🔑 Dynamically determine city from top recommendation
        top_city = recs.iloc[0]["City"]

        # City-aware retrieval query
        retrieval_query = (
            f"{top_city} rent demand metro connectivity zoning regulations 2024"
        )

        docs = retrieve_docs(retrieval_query)

        # Final response
        print(build_response(recs, docs))


# ---------------------------------
# MODE 2: Market Insight Q&A
# ---------------------------------
elif choice == "2":
    query = input("Ask your question: ").strip()

    docs = retrieve_docs(query)

    print("\n📊 Market & Regulatory Insights:\n")
    for d in docs:
        print("-" * 60)
        print(d["text"][:400])

else:
    print("❌ Invalid choice. Please enter 1 or 2.")