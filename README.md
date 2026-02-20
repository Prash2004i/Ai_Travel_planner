🎒 AI Travel Planner for Students

An AI-powered web application that generates personalized, budget-friendly travel itineraries for students based on destination, budget, duration, interests, and travel style.

Built using Streamlit + Google Gemini API, this project focuses on smart, cost-optimized trip planning tailored specifically for student travelers.

🚀 Features:

🗺️ Personalized day-wise travel itinerary

💰 Budget-based trip planning

🏨 Accommodation suggestions

🚇 Cheap transport recommendations

🍜 Food and local experience suggestions

📊 Expense breakdown and total budget summary

💡 Money-saving travel tips

🎨 Clean and interactive Streamlit UI

🧠 Tech Stack:
Layer	Technology
💻 Language	Python
🌐 Frontend	Streamlit
🤖 AI Model	Google Gemini API
🛠️ IDE	Visual Studio Code
⚙️ How It Works

User enters destination, number of days, budget, interests, and travel style.

Input is converted into a structured prompt.

Prompt is sent to Google Gemini API.

AI generates a detailed travel plan.

The itinerary is displayed in a structured format in the web interface.

▶️ Run Locally
pip install -r requirements.txt
streamlit run app.py
