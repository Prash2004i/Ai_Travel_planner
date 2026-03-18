import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

# Page settings
st.set_page_config(page_title="AI Travel Planner", page_icon="🎒", layout="wide")

st.title("🎒 WanderAI - AI Travel Planner for Students")
st.write("Plan budget-friendly trips using AI ✨")

# ------------------ SESSION STATE INIT ------------------

if "travel_plan" not in st.session_state:
    st.session_state.travel_plan = None

if "trip_context" not in st.session_state:
    st.session_state.trip_context = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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

        # Save plan and context to session state
        st.session_state.travel_plan = response.text
        st.session_state.trip_context = {
            "destination": destination,
            "days": days,
            "budget": budget,
            "currency": currency,
            "group_size": group_size,
            "travel_style": travel_style,
            "pace": pace,
            "accommodation": accommodation,
            "transport_pref": transport_pref,
            "interests": interests,
        }
        # Reset chat history when a new plan is generated
        st.session_state.chat_history = []

# ------------------ DISPLAY PLAN ------------------

if st.session_state.travel_plan:
    st.subheader("📍 Your Travel Plan")
    st.markdown(st.session_state.travel_plan)

    # ------------------ COST VISUALIZATION ------------------

    ctx = st.session_state.trip_context
    daily_budget = round(ctx["budget"] / ctx["days"], 2)

    st.subheader("💰 Budget Overview")
    data = {
        "Category": ["Accommodation", "Food", "Transport", "Activities"],
        "Estimated Cost": [
            daily_budget * 0.4 * ctx["days"],
            daily_budget * 0.25 * ctx["days"],
            daily_budget * 0.2 * ctx["days"],
            daily_budget * 0.15 * ctx["days"],
        ]
    }
    df = pd.DataFrame(data)
    st.bar_chart(df.set_index("Category"))

    # ------------------ DOWNLOAD OPTION ------------------

    st.download_button(
        label="📥 Download Itinerary",
        data=st.session_state.travel_plan,
        file_name="travel_plan.txt",
        mime="text/plain"
    )

    # ==================== POST-PLANNING CHATBOT ====================

    st.divider()
    st.subheader("🤖 Trip Support Assistant")
    st.write(
        "Need to adjust your plan? Ask me anything — sudden changes, alternatives, "
        "budget tweaks, or quick questions about your trip!"
    )

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("e.g. My hostel is full on Day 2, suggest alternatives...")

    if user_input:
        # Show user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Build context-aware system prompt
        ctx = st.session_state.trip_context
        system_context = f"""
You are a helpful travel support assistant for a student trip.
Here is the original trip plan context:
- Destination: {ctx['destination']}
- Duration: {ctx['days']} days
- Total Budget: {ctx['budget']} {ctx['currency']}
- Group Size: {ctx['group_size']} traveler(s)
- Travel Style: {ctx['travel_style']}
- Trip Pace: {ctx['pace']}
- Accommodation: {ctx['accommodation']}
- Transport: {ctx['transport_pref']}
- Interests: {', '.join(ctx['interests'])}

Here is the full itinerary that was generated:
{st.session_state.travel_plan}

Your role:
- Help the traveler handle last-minute changes, emergencies, or new preferences
- Suggest alternatives that fit within their remaining budget
- Keep answers practical, concise, and student-friendly
- If they ask to modify a day, provide a revised version of just that day
- Always be encouraging and calm even in stressful situations
"""

        # Build conversation history for multi-turn chat
        messages_for_api = [{"role": "user", "parts": [system_context + "\n\nUser: " + user_input]}]

        # Include prior chat turns (skip the first user message we already embedded)
        if len(st.session_state.chat_history) > 1:
            messages_for_api = []
            # Reconstruct full conversation with system context in the first message
            for i, msg in enumerate(st.session_state.chat_history):
                if i == 0:
                    messages_for_api.append({
                        "role": "user",
                        "parts": [system_context + "\n\nUser: " + msg["content"]]
                    })
                elif msg["role"] == "user":
                    messages_for_api.append({"role": "user", "parts": [msg["content"]]})
                else:
                    messages_for_api.append({"role": "model", "parts": [msg["content"]]})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chat = model.start_chat(history=messages_for_api[:-1])
                response = chat.send_message(messages_for_api[-1]["parts"][0])
                assistant_reply = response.text
            st.markdown(assistant_reply)

        st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
