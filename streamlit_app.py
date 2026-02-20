import streamlit as st
import requests

backend_url = "http://127.0.0.1:5000"
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MarketMind",
    page_icon="📊",
    layout="wide"
)

st.title("📊 MarketMind - AI Lead Intelligence Platform")

# Backend connection status
try:
    response = requests.get(f"{backend_url}/", timeout=2)
    if response.status_code == 404:  # 404 is expected for root endpoint
        st.success("✅ Backend Connected")
    else:
        st.warning("⚠ Backend Status Unknown")
except:
    st.error("❌ Backend Not Connected - Please start the Flask server")
    st.info("Run: `cd backend && python app.py`")

# ---------------- SIDEBAR SETTINGS ----------------
st.sidebar.title("⚙ AI Settings")

model_choice = st.sidebar.selectbox(
    "Select AI Provider",
    ["Grok", "Doodle"]
)



# ---------------- MAPPING DICTIONARIES ----------------
day_of_week_map = {
    "mon": 1, "tue": 2, "wed": 3,
    "thu": 4, "fri": 5, "sat": 6, "sun": 7
}

month_map = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "may": 5, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "oct": 10, "nov": 11, "dec": 12
}

# =========================================================
# 🔮 LEAD SCORING SECTION
# =========================================================
st.header("🔮 AI Lead Scoring")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 18, 100, 30)
    job = st.selectbox("Job", [
        "management", "technician", "entrepreneur",
        "blue-collar", "retired", "admin.", "services"
    ])
    marital = st.selectbox("Marital Status", ["married", "single", "divorced"])
    education = st.selectbox("Education", ["primary", "secondary", "tertiary"])
    balance = st.number_input("Account Balance", value=1000)

with col2:
    day_of_week = st.selectbox("Day of Week", list(day_of_week_map.keys()))
    month = st.selectbox("Month", list(month_map.keys()))
    duration = st.number_input("Call Duration (seconds)", 0, 5000, 200)
    campaign = st.number_input("Campaign Contacts", 1, 50, 1)
    previous = st.number_input("Previous Contacts", 0, 50, 0)

housing = st.selectbox("Housing Loan", ["yes", "no"])
loan = st.selectbox("Personal Loan", ["yes", "no"])
contact = st.selectbox("Contact Type", ["cellular", "telephone"])
poutcome = st.selectbox("Previous Outcome", ["unknown", "failure", "success"])

if st.button("Predict Conversion"):

    input_data = {
        "age": age,
        "job": job,
        "marital": marital,
        "education": education,
        "default": "no",
        "balance": balance,
        "housing": housing,
        "loan": loan,
        "contact": contact,
        "day_of_week": day_of_week_map[day_of_week],
        "month": month_map[month],
        "duration": duration,
        "campaign": campaign,
        "pdays": -1,
        "previous": previous,
        "poutcome": poutcome
    }

    with st.spinner("Analyzing lead..."):
        try:
            response = requests.post(
                f"{backend_url}/predict-lead",
                json=input_data,
                timeout=5
            )
            result = response.json()

            if "conversion_probability" in result:
                prob = result["conversion_probability"]
                message = result.get("message", "")

                st.subheader("Prediction Result")
                st.metric("Conversion Probability", f"{prob:.2%}")

                if prob > 0.5:
                    st.success(f"✅ {message}")
                else:
                    st.warning(f"⚠ {message}")
            else:
                st.error(result.get("error", "Unexpected response"))

        except requests.exceptions.RequestException as e:
            st.error(f"Connection Error: Unable to connect to backend server. Please make sure the Flask app is running on {backend_url}")
            st.info("To start the backend: `cd backend && python app.py`")
        except Exception as e:
            st.error(f"Unexpected Error: {e}")

# =========================================================
# ✍ MARKETING CONTENT GENERATOR
# =========================================================
st.divider()
st.header("✍ AI Marketing Content Generator")

marketing_prompt = st.text_area("Enter marketing prompt")

if st.button("Generate Content"):
    if marketing_prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating content..."):
            try:
                response = requests.post(
                    f"{backend_url}/generate-content",
                    json={"prompt": marketing_prompt}
                )
                result = response.json()

                st.success("Generated Content")
                st.write(result.get("content", result))

            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: Unable to connect to backend server. Please make sure the Flask app is running.")
                st.info("To start the backend: `cd backend && python app.py`")
            except Exception as e:
                st.error(f"Error: {e}")

# =========================================================
# 🤖 AI SALES ASSISTANT
# =========================================================
st.divider()
st.header("🤖 AI Sales Assistant")

user_question = st.text_input("Ask about sales trends, churn, campaigns...", key="sales_assistant_input")

if st.button("Ask AI Assistant", key="ask_ai_button"):
    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{backend_url}/agent",
                    json={
                        "query": user_question
                    }
                )
                result = response.json()

                st.success("AI Response")
                st.write(result.get("response", result))

            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: Unable to connect to backend server. Please make sure the Flask app is running.")
                st.info("To start the backend: `cd backend && python app.py`")
            except Exception as e:
                st.error(f"Error: {e}")
