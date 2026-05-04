import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# 1. СТРАНИЦА БАПТАУЛАРЫ
st.set_page_config(
    page_title="AL-FARABI SMART ADMINISTRATION",
    page_icon="⚡",
    layout="wide"
)

# ПАЙДАЛАНУШЫ СЕССИЯСЫ (ЕСІМ ЖӘНЕ ДЕРЕКТЕР)
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Директор мырза"

if 'subject_data' not in st.session_state:
    st.session_state.subject_data = pd.DataFrame({
        'Пән': ['IT', 'Математика', 'Физика', 'English', 'Робототехника', 'Химия'],
        'Көрсеткіш': [98, 85, 78, 92, 95, 70]
    })

# 2. ПРЕМЬЕР-ДИЗАЙН (CSS)
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
    }
    h1 { color: #1e3a8a; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; }
    .stButton>button {
        border-radius: 50px;
        background: linear-gradient(45deg, #1e3a8a, #3b82f6);
        color: white;
        padding: 10px 24px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (МӘЗІР)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/906/906343.png", width=120)
    st.title("SMART HQ v4.0")
    
    st.markdown("---")
    st.session_state.user_name = st.text_input("👤 Пайдаланушы:", st.session_state.user_name)
    
    selected = st.selectbox("Навигация", 
        ["🏛 Басты панель", "🗓 Смарт-кесте & Кадрлар", "🔮 ЖИ Болжау Орталығы", "💡 Smart Экосистема", "🤖 AI Консультант"])
    
    st.markdown("---")
    st.write(f"📅 {datetime.now().strftime('%d.%m.%Y')}")
    st.success("🔴 Жүйе: ОНЛАЙН")

# --- ФУНКЦИЯЛАР ---

# 1. БАСТЫ ПАНЕЛЬ (ЖЕТІЛДІРІЛГЕН: ПӘН ҚОСУ)
if selected == "🏛 Басты панель":
    st.title(f"🏛️ Қош келдіңіз, {st.session_state.user_name}!")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Жалпы контингент", "1,520", "↑ 2.1%")
    with col2: st.metric("Білім сапасы (GPA)", "4.82", "↑ 0.15")
    with col3: st.metric("Бюджет үнемдеу", "₸ 420,000", "айына")
    with col4: st.metric("Ата-ана ризашылығы", "96%", "↑ 4%")

    st.markdown("---")
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("📊 Академиялық көрсеткіштер")
        fig = px.bar(st.session_state.subject_data, x='Пән', y='Көрсеткіш', color='Көрсеткіш', 
                     color_continuous_scale='Viridis', text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
        
        # ЖАҢА: ПӘН ҚОСУ ФУНКЦИЯСЫ
        with st.expander("➕ Жаңа пән қосу немесе деректі өзгерту"):
            new_sub = st.text_input("Пән атауы:")
            new_val = st.slider("Көрсеткіш (0-100):", 0, 100, 85)
            if st.button("Деректерді жаңарту"):
                new_row = pd.DataFrame({'Пән': [new_sub], 'Көрсеткіш': [new_val]})
                st.session_state.subject_data = pd.concat([st.session_state.subject_data, new_row]).drop_duplicates('Пән', keep='last')
                st.rerun()

    with c2:
        st.subheader("📍 Хабарламалар")
        st.info(f"Сәлем, {st.session_state.user_name}! Барлық жүйе қалыпты.")
        st.error("📉 9-А: Математикадан төмен көрсеткіш.")
        st.success("🏆 Мектепке жаңа грант бөлінді.")

# 2. КЕСТЕ ЖӘНЕ КАДРЛАР (ЖЕТІЛДІРІЛГЕН: МҰҒАЛІМДЕРДІ ІЗДЕУ)
elif selected == "🗓 Смарт-кесте & Кадрлар":
    st.title("🗓 Кадрлар және Кесте")
    
    tab1, tab2 = st.tabs(["🕒 Сабақ кестесі", "👥 Мұғалімдер базасы"])
    
    with tab1:
        st.write("### AI негізіндегі оңтайландыру")
        sched = pd.DataFrame({
            'Уақыт': ['08:30', '09:25', '10:20', '11:15', '12:10'],
            '10-А': ['IT', 'Математика', 'Физика', 'English', 'Спорт'],
            '11-Б': ['Математика', 'Химия', 'Қазақ тілі', 'IT', 'Тарих']
        })
        st.table(sched)
        if st.button("ЖИ арқылы қайта есептеу"):
            with st.spinner('Жүктелуде...'):
                time.sleep(2)
                st.balloons()

    with tab2:
        st.write("### 🔎 Мұғалімдерді іздеу")
        teachers = pd.DataFrame({
            'Аты-жөні': ['Исаева М.', 'Оспанов Қ.', 'Кәрім А.', 'Сатыбалдиев С.', 'Ахметова Г.', 'Берікұлы Ж.'],
            'Пәні': ['Математика', 'Физика', 'IT', 'Тарих', 'English', 'Химия'],
            'Рейтинг': [4.9, 4.7, 4.9, 4.2, 4.8, 4.5]
        })
        
        # ЖАҢА: ІЗДЕУ ФУНКЦИЯСЫ
        search_term = st.text_input("Мұғалімнің атын немесе пәнін жазыңыз:")
        filtered_df = teachers[teachers['Аты-жөні'].str.contains(search_term, case=False) | 
                               teachers['Пәні'].str.contains(search_term, case=False)]
        
        st.dataframe(filtered_df, use_container_width=True)
        st.plotly_chart(px.bar(filtered_df, x='Аты-жөні', y='Рейтинг', color='Пәні'), use_container_width=True)

# 3. ЖИ БОЛЖАУ
elif selected == "🔮 ЖИ Болжау Орталығы":
    st.title("🔮 AI Predictive Center")
    col_x, col_y = st.columns([1, 1])
    with col_x:
        st.subheader("Оқушы профилі")
        name = st.text_input("Есімі:", "Асель Мейремхан")
        attendance = st.slider("Қатысу (%)", 0, 100, 95)
        homework = st.slider("Үй тапсырмасы (%)", 0, 100, 88)
        test = st.slider("БЖБ бағасы", 0, 100, 92)
    
    with col_y:
        final = (attendance * 0.2) + (homework * 0.3) + (test * 0.5)
        st.subheader(f"Болжам: {final:.1f}%")
        st.plotly_chart(go.Figure(go.Indicator(mode="gauge+number", value=final, gauge={'bar': {'color': "#1e3a8a"}})), use_container_width=True)
        if final > 90: st.success(f"🚀 {name} - Керемет көрсеткіш!")

# 4. SMART ЭКОСИСТЕМА
elif selected == "💡 Smart Экосистема":
    st.title("💡 Ресурстарды бақылау")
    c1, c2, c3 = st.columns(3)
    c1.metric("💡 Электр", "Үнемдеу: 22%", "ЖИ")
    c2.metric("🌡️ Темп", "21.5°C", "Норма")
    c3.metric("💧 Су", "450 л", "-10%")
    img_data = np.random.randint(0, 255, (300, 700, 3), dtype=np.uint8)
    st.image(img_data, caption="ЖИ Аналитикасы: Қауіпсіздік деңгейі жоғары", use_container_width=True)

# 5. AI КОНСУЛЬТАНТ
elif selected == "🤖 AI Консультант":
    st.title(f"🤖 {st.session_state.user_name} үшін ЖИ-Көмекші")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]): st.write(message["content"])

    if user_query := st.chat_input("Сұрақ қойыңыз..."):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"): st.write(user_query)

        with st.chat_message("assistant"):
            q = user_query.lower()
            if "сәлем" in q: ans = f"Сәлеметсіз бе, {st.session_state.user_name}!"
            elif "кесте" in q: ans = "Кесте оңтайландырылды, Директор мырза."
            elif "мұғалім" in q: ans = "Ең жоғары рейтингті мұғалім - Исаева М. (4.9)."
            else: ans = f"Құрметті {st.session_state.user_name}, бұл сұрақ бойынша деректер өңделуде."
            
            st.write(ans)
            st.session_state.chat_history.append({"role": "assistant", "content": ans})
