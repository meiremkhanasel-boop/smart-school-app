import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# --- PDF ГЕНЕРАЦИЯЛАУ ФУНКЦИЯСЫ ---
def create_pdf(title, data_dict):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    font_path = "C:/Windows/Fonts/arial.ttf"
    if os.path.exists(font_path):
        font_name = "ArialCustom"
        pdfmetrics.registerFont(TTFont(font_name, font_path))
    else:
        font_name = "Helvetica"

    p.setFont(f"{font_name}-Bold" if font_name == "Helvetica" else font_name, 16)
    p.drawString(100, 800, f"REPORT: {title}")
    
    p.setFont(font_name, 12)
    p.drawString(100, 780, f"Күні: {datetime.now().strftime('%d.%m.%Y')}")
    
    y = 750
    for key, value in data_dict.items():
        p.drawString(100, y, f"{key}: {value}")
        y -= 20
        
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# 1. СТРАНИЦА БАПТАУЛАРЫ
st.set_page_config(
    page_title="AL-FARABI SMART ADMINISTRATION",
    page_icon="⚡",
    layout="wide"
)

# ПАЙДАЛАНУШЫ СЕССИЯСЫ
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Директор мырза"

# КЕҢЕЙТІЛГЕН ПӘНДЕР ТІЗІМІ
if 'subject_data' not in st.session_state:
    st.session_state.subject_data = pd.DataFrame({
        'Пән': [
            'Қазақ тілі', 'Қазақ әдебиеті', 'Қазақстан тарихы', 'Дүниежүзі тарихы', 
            'Математика', 'IT', 'Физика', 'Химия', 'Биология', 
            'English', 'География', 'Робототехника', 'Дене шынықтыру'
        ],
        'Көрсеткіш': [95, 92, 88, 85, 82, 98, 78, 75, 80, 90, 84, 94, 100]
    })

if 'teachers_list' not in st.session_state:
    st.session_state.teachers_list = pd.DataFrame({
        'Аты-жөні': ['Исаева М.', 'Оспанов Қ.', 'Кәрім А.', 'Сатыбалдиев С.'],
        'Пәні': ['Математика', 'Физика', 'IT', 'Қазақстан тарихы'],
        'Рейтинг': [4.9, 4.7, 4.9, 4.2]
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

# 1. БАСТЫ ПАНЕЛЬ
if selected == "🏛 Басты панель":
    st.title(f"🏛️ Қош келдіңіз, {st.session_state.user_name}!")
    
    pdf = create_pdf("Басты панель", {"Пайдаланушы": st.session_state.user_name, "GPA": "4.82", "Status": "Online"})
    st.download_button("📄 PDF Жүктеу", pdf, file_name="dashboard.pdf")

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
        
        # --- ЖАҢА: ПӘН ҚОСУ БАТЫРМАСЫ ---
        st.write("---")
        st.subheader("➕ Жаңа пән мәліметтерін енгізу")
        new_col1, new_col2, new_col3 = st.columns([2, 1, 1])
        with new_col1:
            new_subject = st.text_input("Пән атауы:", placeholder="Мысалы: Философия")
        with new_col2:
            new_score = st.number_input("Көрсеткіш:", min_value=0, max_value=100, value=85)
        with new_col3:
            st.write(" ") # Бос орын теңестіру үшін
            if st.button("Тізімге қосу"):
                if new_subject:
                    new_row = pd.DataFrame({'Пән': [new_subject], 'Көрсеткіш': [new_score]})
                    st.session_state.subject_data = pd.concat([st.session_state.subject_data, new_row], ignore_index=True)
                    st.success(f"{new_subject} сәтті қосылды!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("Пән атауын жазыңыз!")

    with c2:
        st.subheader("📍 Хабарламалар")
        st.info(f"Сәлем, {st.session_state.user_name}!")
        st.error("📉 9-А: Математика деңгейі төмен.")
        st.success("🏆 Цифрлық грант ұтып алынды.")

# 2. КЕСТЕ ЖӘНЕ КАДРЛАР
elif selected == "🗓 Смарт-кесте & Кадрлар":
    st.title("🗓 Кадрлар және Кесте")
    
    pdf = create_pdf("Кадрлық есеп", {"Мұғалімдер саны": len(st.session_state.teachers_list)})
    st.download_button("📄 PDF Жүктеу", pdf, file_name="staff.pdf")

    tab1, tab2 = st.tabs(["🕒 Сабақ кестесі", "👥 Мұғалімдер базасы"])
    
    with tab1:
        st.write("### AI Смарт-кесте құрастыру")
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            class_select = st.selectbox("Сыныпты таңдаңыз:", ["10-А", "11-Б", "9-В", "8-Г"])
        with c_col2:
            day_select = st.selectbox("Күнді таңдаңыз:", ["Дүйсенбі", "Сейсенбі", "Сәрсенбі", "Бейсенбі", "Жұма"])
        
        st.write("📖 **Кестеге қосылатын пәндерді таңдаңыз:**")
        available_subjects = st.session_state.subject_data['Пән'].tolist()
        selected_subjects = st.multiselect(
            "Пәндер тізімі (таңдалмаса, барлығы қолданылады):", 
            options=available_subjects,
            default=None
        )

        if st.button("ЖИ арқылы кестені құрастыру"):
            with st.spinner('Смарт-талдау жүргізілуде...'):
                time.sleep(1)
                target_list = selected_subjects if selected_subjects else available_subjects
                working_list = target_list.copy()
                np.random.shuffle(working_list)
                
                final_subjects = []
                for i in range(6):
                    if i < len(working_list):
                        final_subjects.append(working_list[i])
                    else:
                        final_subjects.append("-")

                sched = pd.DataFrame({
                    'Сабақ №': ['1', '2', '3', '4', '5', '6'],
                    'Уақыт': ['08:30', '09:25', '10:20', '11:15', '12:10', '13:05'],
                    f'{class_select} ({day_select})': final_subjects
                })
                
                st.success(f"Кесте сәтті құрастырылды!")
                st.table(sched)
                st.balloons()

    with tab2:
        st.write("### 🔎 Мұғалімдерді іздеу")
        search = st.text_input("Аты-жөні немесе пәні бойынша іздеу:")
        filtered_t = st.session_state.teachers_list[
            st.session_state.teachers_list['Аты-жөні'].str.contains(search, case=False) | 
            st.session_state.teachers_list['Пәні'].str.contains(search, case=False)
        ]
        st.dataframe(filtered_t, use_container_width=True)

# 3. ЖИ БОЛЖАУ
elif selected == "🔮 ЖИ Болжау Орталығы":
    st.title("🔮 AI Predictive Center")
    col_x, col_y = st.columns([1, 1])
    with col_x:
        st.subheader("Оқушы профилі")
        name = st.text_input("Есімі:", "Асель Мейремхан")
        attendance = st.slider("Қатысу (%)", 0, 100, 95)
        test = st.slider("БЖБ бағасы", 0, 100, 92)
        final = (attendance * 0.4) + (test * 0.6)
    with col_y:
        st.subheader(f"Болжам: {final:.1f}%")
        st.plotly_chart(go.Figure(go.Indicator(mode="gauge+number", value=final)), use_container_width=True)

# 4. SMART ЭКОСИСТЕМА
elif selected == "💡 Smart Экосистема":
    st.title("💡 Ресурстарды бақылау")
    c1, c2, c3 = st.columns(3)
    c1.metric("💡 Электр", "Үнем: 22%", "ЖИ")
    c2.metric("🌡️ Темп", "21.5°C", "Норма")
    c3.metric("💧 Су", "450 л", "-10%")

# 5. AI КОНСУЛЬТАНТ
elif selected == "🤖 AI Консультант":
    st.title(f"🤖 {st.session_state.user_name} үшін ЖИ-Көмекші")
    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]): st.write(message["content"])
    if user_query := st.chat_input("Сұрақ қойыңыз..."):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"): st.write(user_query)
        with st.chat_message("assistant"):
            ans = f"Құрметті {st.session_state.user_name}, деректер талдануда."
            st.write(ans)
            st.session_state.chat_history.append({"role": "assistant", "content": ans})
