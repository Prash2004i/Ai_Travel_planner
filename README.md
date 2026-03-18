
 🎒 WanderAI – AI Travel Planner for Students

An AI-powered travel planning web app that creates personalized, budget-friendly itineraries for students — now enhanced with a context-aware trip assistant for real-time adjustments.

Built using Streamlit + Google Gemini API, this project focuses on smart, flexible, and cost-optimized trip planning tailored specifically for student travelers.



## 🚀 Features

### 🗺️ Smart Travel Planning

* Personalized day-wise itinerary generation
* Budget-based trip optimization
* Accommodation recommendations (hostels, Airbnb, etc.)
* Cheap transport suggestions
* Local food and experience recommendations

### 💰 Budget Intelligence

* Daily and total expense breakdown
* Visual budget distribution chart
* Cost-optimized suggestions for students
* Money-saving travel tips and local hacks

### 🤖 Context-Aware Trip Assistant 

* Interactive chatbot after itinerary generation
* Understands your entire trip context
* Handles:

  * Last-minute changes
  * Plan modifications
  * Budget adjustments
  * Emergency alternatives
* Maintains conversation memory for multi-turn chat
* Gives practical, student-friendly responses

### 📊 Additional Features

* Download itinerary as a file
* Clean and interactive UI using Streamlit
* Session-based trip memory handling

---

## 🧠 Tech Stack

Layer        Technology
💻 Language  Python
🌐 Frontend  Streamlit
🤖 AI Model  Google Gemini 2.5 Flash
📊 Data      Pandas (for charts)
🛠️ IDE       Visual Studio Code

---

## ⚙️ How It Works

1. User enters:

   * Destination
   * Budget
   * Duration
   * Preferences (style, pace, transport, etc.)

2. Input is converted into a structured AI prompt

3. Prompt is sent to Google Gemini API

4. AI generates a detailed travel itinerary

5. App stores:

   * Travel plan
   * Trip context (for future interaction)

6. User can interact with the Trip Support Assistant, which:

   * Uses the stored context
   * Adapts responses based on previous conversation
   * Provides dynamic updates to the plan

---

## 🧩 Context-Aware System 

The app now includes a stateful AI system:

* Stores trip details in session state
* Embeds full itinerary into chatbot context
* Reconstructs conversation history for multi-turn interactions
* Generates context-aware responses instead of generic replies

This makes the assistant behave like a real travel companion, not just a one-time planner.

---

## ▶️ Run Locally

```
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

* app.py – Main Streamlit application
* .env – API key configuration
* requirements.txt – Dependencies

---

## 💡 Future Improvements

* Live pricing APIs (flights, hotels)
* Map integration
* Multi-city trip planning
* User login and saved trips
* Offline itinerary mode

