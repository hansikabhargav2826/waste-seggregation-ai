# ================= AI WASTE SEGREGATION APP =================
import streamlit as st
import plotly.express as px
from PIL import Image
import pandas as pd
import sqlite3

from utils.preprocessing import preprocess_image
from model.predict import predict_waste

from db import (
    init_database,
    authenticate_user,
    create_user,
    save_prediction,
    update_eco_score
)

# ================= CONFIG =================
st.set_page_config(page_title="♻️ AI Waste Segregation", layout="wide")
init_database()

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "home"

if "eco_score" not in st.session_state:
    st.session_state.eco_score = 0

# ================= NAVIGATION =================
def go(page):
    st.session_state.page = page

col1, col2, col3, col4, col5 = st.columns([1, 7, 1, 1, 1])

with col1:
    st.button("🏠 Home", on_click=go, args=("home",))
    if st.button("⚙️ Settings"):
        st.session_state.page = "settings"

with col3:
    st.button("🔐 Login", on_click=go, args=("login",))
with col4:
    st.button("📝 Register", on_click=go, args=("register",))

# LOGOUT
with col5:
    if st.session_state.user is not None:
        if st.button("🚪 Logout"):
            st.session_state.user = None
            st.session_state.eco_score = 0
            st.session_state.page = "home"
            st.success("Logged out successfully")
            st.rerun()

# HEADING
with col2:
    st.markdown(
        """
        <div style="
            background: linear-gradient(90deg, #16a34a, #22c55e);
            padding:20px;
            border-radius:15px;
            text-align:center;
            color:white;
            font-size:32px;
            font-weight:bold;
            border: 3px solid #14532d;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
            letter-spacing:1px;">
            ♻️ Waste Segregation Using AI
        </div>
        """,
        unsafe_allow_html=True
    )

page = st.session_state.page

# ================= HELPERS =================
def get_user_predictions(user_id):
    conn = sqlite3.connect("waste_segregation.db")
    df = pd.read_sql_query(
        "SELECT * FROM predictions WHERE user_id=?",
        conn,
        params=(user_id,)
    )
    conn.close()
    return df


# ================= HOME =================
if page == "home":

    # ✅ SLIDESHOW (ONLY ADDED PART)
    st.markdown("""
    <style>
    .slider {
      width: 100%;
      height: 350px;
      overflow: hidden;
      border-radius: 15px;
      margin-top: 20px;
      margin-bottom: 20px;
    }

    .slides {
      display: flex;
      width: 300%;
      animation: slide 12s infinite;
    }

    .slides img {
      width: 100%;
      height: 350px;
      object-fit: cover;
    }

    @keyframes slide {
      0% { margin-left: 0%; }
      33% { margin-left: -100%; }
      66% { margin-left: -200%; }
      100% { margin-left: 0%; }
    }
    </style>

    <div class="slider">
      <div class="slides">
        <img src="https://images.unsplash.com/photo-1581578731548-c64695cc6952">
        <img src="https://images.unsplash.com/photo-1604187351574-c75ca79f5807">
        <img src="https://images.unsplash.com/photo-1501004318641-b39e6451bec6">
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
<div style="font-size:28px; line-height:1.8; padding:15px;">
<h2>🌱 About This Website</h2>
<h3>
This AI Waste Segregation System is designed to intelligently classify waste into Organic, Recyclable, E-Waste, and Residual categories using advanced machine learning techniques. The system analyzes uploaded images in real time to provide accurate predictions, helping users identify the correct method of disposal quickly and efficiently. By simplifying the waste segregation process, it encourages environmentally responsible behavior and promotes sustainable living in everyday life. Proper waste management is essential for reducing pollution, conserving natural resources, and minimizing landfill impact, and this platform aims to make that process easy, accessible, and effective for everyone. Through features like eco scoring and awareness insights, the system not only assists users but also motivates them to contribute towards a cleaner, greener, and more sustainable future.
</h3>
</div>
""", unsafe_allow_html=True)

    # GUIDELINES
    st.markdown("""
    <div style="font-size:24px; line-height:2;">
    <b>📌 Guidelines</b><br><br>
    1️⃣ Upload clear images<br>
    2️⃣ Good lighting<br>
    3️⃣ Separate wet & dry waste<br>
    4️⃣ Proper disposal<br>
    5️⃣ Reduce plastic usage<br>
    6️⃣ Track eco score<br>
    7️⃣ Follow rules<br>
    8️⃣ Keep environment clean<br>
    9️⃣ Recycle properly<br>
    🔟 Be responsible
    </div>
    """, unsafe_allow_html=True)

    # CATEGORY GRAPH
    st.subheader("📊 Waste Categories Overview")

    df_cat = pd.DataFrame({
        "Category": ["Organic", "Recyclable", "E-Waste", "Residual"],
        "Count": [120, 90, 40, 60]
    })

    fig1 = px.bar(df_cat, x="Category", y="Count", color="Category")
    st.plotly_chart(fig1, use_container_width=True)

    # INDIA MAP
    st.subheader("🗺️ India Waste Map (20 Cities)")

    cities = [
        "Delhi","Mumbai","Bangalore","Chennai","Kolkata",
        "Hyderabad","Pune","Ahmedabad","Jaipur","Lucknow",
        "Surat","Kanpur","Nagpur","Indore","Bhopal",
        "Patna","Chandigarh","Coimbatore","Kochi","Visakhapatnam"
    ]

    waste = [
        950,870,780,700,650,
        600,580,560,500,450,
        430,420,410,400,390,
        380,370,360,350,340
    ]

    fig_map = px.scatter_mapbox(
        lat=[28.6,19.0,12.9,13.0,22.5,17.3,18.5,23.0,26.9,22.7,21.1,26.4,21.1,22.7,23.2,25.6,30.7,11.0,9.9,17.7],
        lon=[77.2,72.8,77.5,80.2,88.3,78.5,73.8,72.6,75.8,75.8,72.8,80.3,79.1,75.9,77.4,85.1,76.8,76.9,76.3,83.3],
        size=waste,
        color=cities,
        hover_name=cities,
        zoom=4,
        mapbox_style="open-street-map"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # CITY GRAPH
    st.subheader("🏙️ Waste in 20 Indian Cities")

    city_df = pd.DataFrame({"City": cities, "Waste": waste})
    fig2 = px.bar(city_df, x="City", y="Waste", color="Waste")
    st.plotly_chart(fig2, use_container_width=True)

    # ARTICLES
    st.subheader("📚 Articles")
    st.markdown("""
- 🌿 https://en.wikipedia.org/wiki/Waste_management_in_India  
- 🇮🇳 https://swachhbharatmission.gov.in/  
- ♻️ https://cpcb.nic.in/plastic-waste/  
- 🌍 https://www.moef.gov.in/  
- 🔄 https://www.nationalgeographic.com/environment/article/recycling
""")

    # VIDEOS
    st.subheader("🎥 Awareness Videos")
    videos = [
        "https://www.youtube.com/watch?v=OasbYWF4_S8",
        "https://www.youtube.com/watch?v=6jQ7y_qQYUA"
    ]
    for v in videos:
        st.video(v)


# ================= SETTINGS =================
elif page == "settings":

    st.subheader("⚙️ Settings")

    if st.session_state.user is None:
        st.info("⚠️ Login to view profile/settings")
    else:
        st.markdown("### 👤 Profile")
        st.write(f"👤 Username: {st.session_state.user['username']}")
        st.write(f"🌱 Eco Score: {st.session_state.eco_score}")

        st.markdown("### 📂 Upload History")
        df = get_user_predictions(st.session_state.user["id"])

        if not df.empty:
            st.dataframe(df)
        else:
            st.warning("No uploads yet")


# ================= LOGIN =================
elif page == "login":

    st.subheader("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    st.image("logo.png",width=600)

    if st.button("Login"):
        if not u or not p:
            st.warning("⚠️ Enter username & password")
        else:
            user = authenticate_user(u, p)
            if user:
                st.session_state.user = user
                st.session_state.eco_score = user["eco_score"]
                st.session_state.page = "predict"
                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")


# ================= REGISTER =================
elif page == "register":

    st.subheader("📝 Register")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    st.image("logo.png",width=600)

    if st.button("Register"):
        if not u or not p:
            st.warn=ing("⚠️ Enter username & password")
        else:
            create_user(u, p)
            st.success("✅ Account created")


# ================= PREDICT =================
elif page == "predict":

    if st.session_state.user is None:
        st.warning("Login first")
        st.stop()

    st.success(f"Welcome {st.session_state.user['username']}")

    file = st.file_uploader("Upload Image")

    if file:
        img = Image.open(file)
        st.image(img, width=600)

        result = predict_waste(preprocess_image(img), file.name)

        category = result["category"]
        condition = result["condition"]
        instruction = result["instruction"]
        confidence = float(result["category_confidence"]) * 100

        eco_map = {"E-Waste":25,"Recyclable":20,"Organic":10,"Residual":5}
        points = eco_map.get(category, 0)

        st.session_state.eco_score += points

        update_eco_score(
            st.session_state.user["id"],
            st.session_state.eco_score
        )

        save_prediction(
            st.session_state.user["id"], file.name,
            category, condition, confidence, instruction
        )

        st.markdown("## ♻️ Prediction Result")

        st.markdown(f"""
        <div style="font-size:40px; padding:18px; background:#0f172a;
        border-radius:15px; color:white; line-height:2;">
        🗂️ Category: {category} <br>
        🧪 Condition: {condition} <br>
        📊 Confidence: {confidence:.2f}% <br>
        📌 Instruction: {instruction}
        </div>
        """, unsafe_allow_html=True)

        st.info(f"🌱 Eco Score: {st.session_state.eco_score}")

        df_all = get_user_predictions(st.session_state.user["id"])

        if not df_all.empty:

            bar_df = df_all.groupby("waste_category").size().reset_index(name="count")

            fig_bar = px.bar(bar_df, x="waste_category", y="count", color="waste_category")
            st.plotly_chart(fig_bar, use_container_width=True)

            fig_pie = px.pie(bar_df,names="waste_category",values="count",title="Waste Distribution")
            fig_pie.update_traces(textinfo="label+percent",textposition="inside",hole=0.4)
            fig_pie.update_layout(height=500,width=700,legend=dict(font=dict(size=14)))
            st.plotly_chart(fig_pie, use_container_width=True)