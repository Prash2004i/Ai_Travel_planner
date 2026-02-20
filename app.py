import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

# Page settings
st.set_page_config(page_title="AI Travel Planner", page_icon="🎒", layout="wide")

st.title("🎒 AI Travel Planner for Students")
st.write("Plan budget-friendly trips using AI ✨")

# ------------------ USER INPUTS ------------------

col1, col2 = st.columns(2)

with col1:
    destination = st.text_input("Destination City")
    days = st.slider("Number of Days", 1, 30, 5)
    budget = st.number_input("Total Budget", min_value=50, step=50)
    currency = st.selectbox("Currency", ["USD", "EUR", "INR", "GBP"])
    group_size = st.number_input("Number of Travelers", min_value=1, max_value=10, value=1)

with col2:
    travel_style = st.selectbox(
        "Travel Style",
        ["Backpacking", "Comfort Budget", "Local Experience"]
    )

    pace = st.selectbox(
        "Trip Pace",
        ["Relaxed", "Balanced", "Fast-paced"]
    )

    accommodation = st.selectbox(
        "Accommodation Type",
        ["Hostel", "Budget Hotel", "Airbnb", "Couchsurfing"]
    )

    transport_pref = st.selectbox(
        "Transport Preference",
        ["Public Transport", "Walk/Bike", "Rideshare", "Mixed"]
    )

interests = st.multiselect(
    "Select Interests",
    ["Adventure", "Food", "History", "Nature", "Shopping", "Nightlife", "Museums"]
)

# ------------------ GENERATE PLAN ------------------

if st.button("Generate Travel Plan ✈️"):

    if not destination or not interests:
        st.warning("Please fill all required fields.")
    else:

        daily_budget = round(budget / days, 2)

        prompt = f"""
        Create a detailed {days}-day student-friendly travel itinerary for {destination}.

        Total Budget: {budget} {currency}
        Daily Budget: {daily_budget} {currency}
        Number of Travelers: {group_size}
        Travel Style: {travel_style}
        Trip Pace: {pace}
        Accommodation Preference: {accommodation}
        Transport Preference: {transport_pref}
        Interests: {', '.join(interests)}

        Include:
        - Budget accommodation suggestions
        - Cheapest transport options
        - Free/low-cost attractions
        - Daily food suggestions (budget-friendly)
        - Clear daily cost breakdown table
        - Total estimated cost summary
        - Smart money-saving tips
        - Local student hacks

        Format nicely with headings.
        """

        with st.spinner("Generating your itinerary..."):
            response = model.generate_content(prompt)

        st.subheader("📍 Your Travel Plan")
        st.markdown(response.text)

        # ------------------ COST VISUALIZATION ------------------

        st.subheader("💰 Budget Overview")

        data = {
            "Category": ["Accommodation", "Food", "Transport", "Activities"],
            "Estimated Cost": [
                daily_budget * 0.4 * days,
                daily_budget * 0.25 * days,
                daily_budget * 0.2 * days,
                daily_budget * 0.15 * days
            ]
        }

        df = pd.DataFrame(data)
        st.bar_chart(df.set_index("Category"))

        # ------------------ DOWNLOAD OPTION ------------------

        st.download_button(
            label="📥 Download Itinerary",
            data=response.text,
            file_name="travel_plan.txt",
            mime="text/plain"
        )