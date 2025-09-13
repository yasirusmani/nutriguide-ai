import streamlit as st
import google.generativeai as genai
import os
import matplotlib.pyplot as plt


API_KEY = os.getenv("GENAI_API_KEY")
if not API_KEY:
    st.error("❌ Please set your GENAI_API_KEY as an environment variable.")
else:
    genai.configure(api_key=API_KEY)


st.set_page_config(
    page_title="NutriGuide AI",
    page_icon="🥗",
    layout="centered"
)

st.title("🥗 NutriGuide AI")
st.write("Your personalized nutrition & meal planning assistant.")



st.sidebar.header("⚡ Quick Tools")

tool_choice = st.sidebar.radio(
    "Choose a feature:",
    ["💬 Chat with Nutrition Assistant", "🧮 Macro Calculator", "📅 Generate Meal Plan"]
)


if tool_choice == "🧮 Macro Calculator":
    st.subheader("Macro & Calorie Calculator")

    age = st.number_input("Age", 18, 100, 25)
    weight = st.number_input("Weight (kg)", 30, 200, 70)
    height = st.number_input("Height (cm)", 100, 220, 175)
    activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active"])
    goal = st.selectbox("Goal", ["Maintain Weight", "Lose Weight", "Gain Muscle"])

    if st.button("Calculate"):
        # Mifflin-St Jeor Equation for BMR
        bmr = 10 * weight + 6.25 * height - 5 * age + 5

        activity_factors = {
            "Sedentary": 1.2,
            "Light": 1.375,
            "Moderate": 1.55,
            "Active": 1.725
        }
        tdee = bmr * activity_factors[activity]

        if goal == "Lose Weight":
            calories = tdee - 500
        elif goal == "Gain Muscle":
            calories = tdee + 300
        else:
            calories = tdee

        protein = weight * 2  
        carbs = (calories - (protein * 4 + fat * 9)) / 4

        st.success(f"Estimated Calories: {int(calories)} kcal/day")
        st.write(f"**Protein:** {int(protein)} g | **Fat:** {int(fat)} g | **Carbs:** {int(carbs)} g")

        
        labels = ["Protein", "Fat", "Carbs"]
        values = [protein*4, fat*9, carbs*4]  

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

elif tool_choice == "📅 Generate Meal Plan":
    st.subheader("AI-Powered Meal Plan")

    target_calories = st.number_input("Target Calories (kcal)", 1200, 4000, 2000)
    diet_type = st.selectbox("Diet Preference", ["No Preference", "Vegetarian", "Vegan", "Keto"])
    days = st.slider("Number of Days", 1, 7, 3)

    if st.button("Generate Meal Plan"):
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        Create a {days}-day meal plan with ~{target_calories} kcal/day.
        Diet preference: {diet_type}.
        Include breakfast, lunch, dinner, and snacks.
        Show each day clearly separated.
        """
        response = model.generate_content(prompt)
        st.write(response.text)


else:
    st.subheader("Chat with NutriGuide AI")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for role, text in st.session_state.chat_history:
        st.chat_message(role).markdown(text)

    user_input = st.chat_input("Ask me anything about nutrition...")
    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        bot_reply = response.text
        st.session_state.chat_history.append(("assistant", bot_reply))
        st.chat_message("assistant").markdown(bot_reply)


st.markdown("---")
st.info("⚠️ This tool provides **general nutrition guidance only** and is not a substitute for professional medical advice.")
