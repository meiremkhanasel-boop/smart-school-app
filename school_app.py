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
    
    # Қазақ тіліне арналған қаріп (Arial қолданылады)
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

# КЕҢЕЙТІЛГЕН ОҚУШЫЛАР МӘЛІМЕТТЕРІ
students_db = {
    "9-А": {
        "Аманжол Ернар": {"attendance": 88, "gpa": 75},
        "Серікболқызы Мадина": {"attendance": 94, "gpa": 91},
        "Тұрсынхан Әли": {"attendance": 70, "gpa": 62},
        "Берікқажы Айша": {"attendance": 96, "gpa": 89},
        "Жұмағұл Дамир": {"attendance": 82, "gpa": 70}
    },
    "10-А": {
        "Асель Мейремхан": {"attendance": 98, "gpa": 96},
        "Арман Болат": {"attendance": 85, "gpa": 78},
        "Диана Серік": {"attendance": 92, "gpa": 88},
        "Нұрланов Темірлан": {"attendance": 75, "gpa": 68},
        "Смағұл Ерасыл": {"attendance": 90, "gpa": 84}
    },
    "11-Б": {
        "Бауыржан Иса": {"attendance": 72, "gpa": 65},
        "Айлин Мұрат": {"attendance": 99, "gpa": 97},
        "Санжар Әли": {"attendance": 88, "gpa": 82},
        "Кәрімжан Меруерт": {"attendance": 95, "gpa": 93},
        "Оспанов Бахтияр": {"attendance": 80, "gpa": 74}
    },
    "11-В (Физ-Мат)": {
        "Байжанов Даурен": {"attendance": 91, "gpa": 85},
        "Ермекова Гүлназ": {"attendance": 97, "gpa": 94},
        "Сәкенұлы Расул": {"attendance": 84, "gpa": 79},
        "Әуесхан Сабина": {"attendance": 100, "gpa": 98}
    }
}

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

# --- 1. БАСТЫ ПАНЕЛЬ ---
if selected == "🏛 Басты панель":
    st.title(f"🏛️ Қош келдіңіз, {st.session_state.user_name}!")
    
    pdf = create_pdf("Басты панель", {"Пайдаланушы": st.session_state.user_name, "GPA": "4.82", "Status": "Online"})
    st.download_button("📄 PDF Жүктеу", pdf, file_name="dashboard.pdf")

    col1, col2 = st.columns(2)
    with col1: st.metric("Білім сапасы (GPA)", "4.82", "↑ 0.15")
    with col2: st.metric("Ата-ана ризашылығы", "96%", "↑ 4%")
    st.markdown("---")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📊 Академиялық көрсеткіштер")
        fig = px.bar(st.session_state.subject_data, x='Пән', y='Көрсеткіш', color='Көрсеткіш', 
                     color_continuous_scale='Viridis', text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("---")
        
        # РЕДАКТОРЛАУ БӨЛІМІ (ҚОСУ ЖӘНЕ ӨШІРУ)
        edit_col1, edit_col2 = st.columns(2)
        
        with edit_col1:
            st.subheader("➕ Жаңа пән қосу")
            new_subject = st.text_input("Пән атауы:", placeholder="Мысалы: Философия")
            new_score = st.number_input("Көрсеткіш:", min_value=0, max_value=100, value=85, key="add_score")
            if st.button("Тізімге қосу"):
                if new_subject:
                    new_row = pd.DataFrame({'Пән': [new_subject], 'Көрсеткіш': [new_score]})
                    st.session_state.subject_data = pd.concat([st.session_state.subject_data, new_row], ignore_index=True)
                    st.success(f"{new_subject} сәтті қосылды!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("Пән атауын жазыңыз!")
                    
        with edit_col2:
            st.subheader("🗑️ Пәнді өшіру")
            subject_to_delete = st.selectbox("Өшірілетін пәнді таңдаңыз:", options=st.session_state.subject_data['Пән'].tolist())
            st.write(" ") # Арақашықтық үшін
            if st.button("Таңдалған пәнді жою"):
                st.session_state.subject_data = st.session_state.subject_data[st.session_state.subject_data['Пән'] != subject_to_delete]
                st.error(f"{subject_to_delete} тізімнен өшірілді!")
                time.sleep(1)
                st.rerun()

    with c2:
        st.subheader("📍 Хабарламалар")
        st.info(f"Сәлем, {st.session_state.user_name}!")
        st.error("📉 9-А: Математика деңгейі төмен.")
        st.success("🏆 Цифрлық грант ұтып алынды.")

# --- 2. КЕСТЕ ЖӘНЕ КАДРЛАР ---
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
        selected_subjects = st.multiselect("Пәндер тізімі:", options=available_subjects, default=None)

        if st.button("ЖИ арқылы кестені құрастыру"):
            with st.spinner('Смарт-талдау жүргізілуде...'):
                time.sleep(1)
                target_list = selected_subjects if selected_subjects else available_subjects
                working_list = target_list.copy()
                np.random.shuffle(working_list)
                
                final_subjects = [working_list[i] if i < len(working_list) else "-" for i in range(6)]
                sched = pd.DataFrame({
                    'Сабақ №': ['1', '2', '3', '4', '5', '6'],
                    'Уақыт': ['08:30', '09:25', '10:20', '11:15', '12:10', '13:05'],
                    f'{class_select} ({day_select})': final_subjects
                })
                st.success(f"Кесте сәтті құрастырылды!")
                st.table(sched)
                st.balloons()

    with tab2:
        st.write("### 👥 Мұғалімдерді басқару")
        with st.expander("➕ Жаңа мұғалім қосу"):
            t_col1, t_col2, t_col3 = st.columns([2, 2, 1])
            with t_col1:
                new_t_name = st.text_input("Аты-жөні:", placeholder="Мысалы: Ахметов А.")
            with t_col2:
                available_subs = st.session_state.subject_data['Пән'].tolist()
                new_t_subject = st.selectbox("Пәні:", options=available_subs)
            with t_col3:
                new_t_rating = st.number_input("Рейтинг:", min_value=0.0, max_value=5.0, value=5.0, step=0.1)
            
            if st.button("Мұғалімді базаға қосу"):
                if new_t_name:
                    new_teacher = pd.DataFrame({
                        'Аты-жөні': [new_t_name],
                        'Пәні': [new_t_subject],
                        'Рейтинг': [new_t_rating]
                    })
                    st.session_state.teachers_list = pd.concat([st.session_state.teachers_list, new_teacher], ignore_index=True)
                    st.success(f"{new_t_name} сәтті қосылды!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.warning("Мұғалімнің атын жазыңыз!")

        st.markdown("---")
        st.write("### 🔎 Мұғалімдерді іздеу")
        search = st.text_input("Аты-жөні немесе пәні бойынша іздеу:")
        filtered_t = st.session_state.teachers_list[
            st.session_state.teachers_list['Аты-жөні'].str.contains(search, case=False) | 
            st.session_state.teachers_list['Пәні'].str.contains(search, case=False)
        ]
        st.dataframe(filtered_t, use_container_width=True)

        # МҰҒАЛІМДІ ӨШІРУ БӨЛІМІ (ЖАҢА)
        st.markdown("---")
        st.write("### 🗑️ Мұғалімді базадан өшіру")
        del_col1, del_col2 = st.columns([2, 1])
        with del_col1:
            teacher_to_delete = st.selectbox("Өшірілетін мұғалімді таңдаңыз:", 
                                             options=st.session_state.teachers_list['Аты-жөні'].tolist())
        with del_col2:
            st.write(" ") # Визуалды теңестіру
            if st.button("Таңдалғанды жою"):
                st.session_state.teachers_list = st.session_state.teachers_list[
                    st.session_state.teachers_list['Аты-жөні'] != teacher_to_delete
                ]
                st.error(f"{teacher_to_delete} базадан өшірілді!")
                time.sleep(1)
                st.rerun()

# --- 3. ЖИ БОЛЖАУ ---
elif selected == "🔮 ЖИ Болжау Орталығы":
    st.title("🔮 AI Student Performance Analytics")
    st.markdown("---")
    
    col_x, col_y = st.columns([1, 1])
    with col_x:
        st.subheader("📋 Оқушы таңдау панелі")
        selected_class = st.selectbox("Сыныпты таңдаңыз:", list(students_db.keys()))
        available_students = list(students_db[selected_class].keys())
        selected_student = st.selectbox("Оқушының аты-жөні:", available_students)
        student_info = students_db[selected_class][selected_student]
        
        st.write("---")
        st.subheader("⚙️ Болжамды модельдеу")
        curr_attendance = st.slider("Қатысу көрсеткіші (%)", 0, 100, student_info["attendance"])
        curr_gpa = st.slider("Академиялық үлгерім (0-100)", 0, 100, student_info["gpa"])
        prediction = (curr_attendance * 0.35) + (curr_gpa * 0.65)

    with col_y:
        st.subheader(f"📊 Болжамдық есеп: {selected_student}")
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=prediction,
            delta={'reference': 85},
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Жалпы үлгерім индексі", 'font': {'size': 18}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#1e3a8a"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': '#ffcfcf'},
                    {'range': [50, 80], 'color': '#fff4cf'},
                    {'range': [80, 100], 'color': '#cfffcf'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 95
                }
            }
        ))
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 🤖 ЖИ Сараптамасы:")
        if prediction >= 90:
            st.success(f"**ҚОРЫТЫНДЫ:** {selected_student} жоғары академиялық потенциалға ие. Жобалық жұмыстарға тарту ұсынылады.")
        elif prediction >= 75:
            st.info(f"**ҚОРЫТЫНДЫ:** Оқушының көрсеткіштері тұрақты. Пәндік олимпиадаларға дайындық бастауға болады.")
        elif prediction >= 50:
            st.warning(f"**ҚОРЫТЫНДЫ:** Орташа деңгей. Қатысу көрсеткішін көтеріп, бақылау жұмыстарына көңіл бөлу керек.")
        else:
            st.error(f"**ҚАТЕР:** Төмен нәтиже. Ата-анамен психологиялық кеңес өткізу қажет.")

# --- 4. SMART ЭКОСИСТЕМА ---
elif selected == "💡 Smart Экосистема":
    st.title("💡 Ресурстарды бақылау және Экология")
    
    with st.expander("⚙️ Экосистема параметрлерін реттеу"):
        set_col1, set_col2, set_col3 = st.columns(3)
        with set_col1:
            power_save = st.slider("Электр үнемдеу (%)", 0, 100, 22)
            temp_val = st.number_input("Орташа температура (°C)", 15.0, 30.0, 21.5)
        with set_col2:
            water_cons = st.number_input("Су шығыны (литр)", 0, 2000, 450)
            co2_input = st.slider("CO2 деңгейі (ppm)", 300, 1500, 720)
        with set_col3:
            paper_w = st.number_input("Қағаз қалдығы (кг)", 0, 200, 55)
            plastic_w = st.number_input("Пластик қалдығы (кг)", 0, 200, 20)

    st.markdown("---")
    col_res1, col_res2, col_res3 = st.columns(3)
    col_res1.metric("💡 Электр", f"Үнем: {power_save}%", "ЖИ Бақылау")
    col_res2.metric("🌡️ Орташа темп.", f"{temp_val}°C", "Қалыпты" if 18 <= temp_val <= 24 else "Ауытқу")
    col_res3.metric("💧 Су шығыны", f"{water_cons} л", f"{450 - water_cons} л айырма")
    
    st.markdown("---")
    st.subheader("🍃 Мектеп атмосферасы мен Экология")
    col_air, col_waste = st.columns(2)
    
    with col_air:
        st.write("### 🌬️ Ауа сапасы (CO2)")
        st.progress(co2_input / 1500)
        if co2_input < 800:
            st.success(f"✅ Деңгей: {co2_input} ppm. Ауа таза!")
        elif co2_input < 1000:
            st.warning(f"⚠️ Деңгей: {co2_input} ppm. Орташа, желдету ұсынылады.")
        else:
            st.error(f"🚨 Деңгей: {co2_input} ppm. Критикалық! Тез арада желдетіңіз!")
            
    with col_waste:
        st.write("### ♻️ Қалдықтарды сұрыптау (кг)")
        waste_df = pd.DataFrame({
            'Түрі': ['Қағаз', 'Пластик', 'Басқа'],
            'Көлемі': [paper_w, plastic_w, 10]
        })
        fig_waste = px.pie(waste_df, values='Көлемі', names='Түрі', 
                            hole=0.4, color_discrete_sequence=px.colors.sequential.Tealgrn)
        fig_waste.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_waste, use_container_width=True)

    efficiency = (power_save + (100 - (co2_input/15)) + (100 - (abs(21-temp_val)*10))) / 3
    st.info(f"💡 **ЖИ Кеңесі:** Соңғы деректер бойынша мектептің экологиялық тиімділігі {max(0, min(100, efficiency)):.1f}% құрады.")

# --- 5. AI КОНСУЛЬТАНТ ---
elif selected == "🤖 AI Консультант":
    st.title(f"🤖 {st.session_state.user_name} үшін ЖИ-Көмекші")
    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]): st.write(message["content"])
    if user_query := st.chat_input("Сұрақ қойыңыз..."):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"): st.write(user_query)
        with st.chat_message("assistant"):
            ans = f"Құрметті {st.session_state.user_name}, деректер талдануда. Сіздің '{user_query}' сұрағыңыз бойынша есеп дайындалуда."
            st.write(ans)
            st.session_state.chat_history.append({"role": "assistant", "content": ans})
            
