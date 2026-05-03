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

# 2. ПРЕМЬЕР-ДИЗАЙН (CSS)
st.markdown("""
    <style>
    /* Басты фон мен қаріптер */
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    
    /* Карточкаларға эффект (Glassmorphism) */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
    }
    
    /* Тақырыптар стилі */
    h1 { color: #1e3a8a; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Sidebar дизайны */
    .css-1d391kg { background-color: #1e3a8a !important; }
    
    /* Сәнді батырмалар */
    .stButton>button {
        border-radius: 50px;
        background: linear-gradient(45deg, #1e3a8a, #3b82f6);
        color: white;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (МӘЗІР)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/906/906343.png", width=120)
    st.title("SMART HQ v4.0")
    st.markdown("---")
    selected = st.selectbox("Навигация", 
        ["🏛 Басты панель", "🗓 Смарт-кесте & Кадрлар", "🔮 ЖИ Болжау Орталығы", "💡 Smart Экосистема", "🤖 AI Консультант"])
    st.markdown("---")
    st.write(f"📅 Күні: {datetime.now().strftime('%d.%m.%Y')}")
    st.write("🔴 Жүйе статусы: **ОНЛАЙН**")

# --- ФУНКЦИЯЛАР ---

# 1. БАСТЫ ПАНЕЛЬ
if selected == "🏛 Басты панель":
    st.title("🏛️ Мектептің цифрлық штаб-пәтері")
    
    # Жоғарғы көрсеткіштер
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Жалпы контингент", "1,520", "↑ 2.1%")
    with col2: st.metric("Білім сапасы (GPA)", "4.82", "↑ 0.15")
    with col3: st.metric("Бюджет үнемдеу", "₸ 420,000", "айына")
    with col4: st.metric("Ата-ана ризашылығы", "96%", "↑ 4%")

    st.markdown("---")
    
    # Графиктер (Интерактивті)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📊 Пәндер бойынша академиялық үлгерім")
        data = pd.DataFrame({
            'Пән': ['IT', 'Математика', 'Физика', 'English', 'Робототехника', 'Химия'],
            'Көрсеткіш': [98, 85, 78, 92, 95, 70]
        })
        fig = px.bar(data, x='Пән', y='Көрсеткіш', color='Көрсеткіш', 
                     color_continuous_scale='Viridis', text_auto=True)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.subheader("📍 Шұғыл жағдайлар")
        st.info("🕒 08:30 - Барлық мұғалімдер орнында.")
        st.error("📉 9-А: Математикадан 3 оқушы төмен балл алды.")
        st.success("🏆 Мектеп 'Ең үздік цифрлық мектеп' номинациясын иеленді.")

# 2. КЕСТЕ ЖӘНЕ КАДРЛАР
elif selected == "🗓 Смарт-кесте & Кадрлар":
    st.title("🗓 Смарт-кесте және Педагогтар")
    
    tab1, tab2 = st.tabs(["🕒 Сабақ кестесі", "👥 Мұғалімдер рейтингі"])
    
    with tab1:
        st.write("### AI негізіндегі автоматты кесте")
        sched = pd.DataFrame({
            'Уақыт': ['08:30', '09:25', '10:20', '11:15', '12:10'],
            '10-А (Smart)': ['IT (Кәрім А.)', 'Математика (Исаева)', 'Физика (Оспанов)', 'English', 'Спорт'],
            '11-Б (Smart)': ['Математика', 'Химия (AI Lab)', 'Қазақ тілі', 'IT', 'Тарих']
        })
        st.table(sched)
        if st.button("Кестені ЖИ арқылы қайта құру"):
            with st.spinner('Оңтайландыру жүруде...'):
                time.sleep(2)
                st.snow()
                st.success("Кесте мұғалімдердің шаршау деңгейіне қарай қайта түзілді!")

    with tab2:
        st.write("### Мұғалімдердің тиімділік картасы")
        teachers = pd.DataFrame({
            'Аты-жөні': ['Исаева М.', 'Оспанов Қ.', 'Кәрім А.', 'Сатыбалдиев С.'],
            'Тәжірибе': [15, 8, 12, 5],
            'Рейтинг': [4.9, 4.7, 4.9, 4.2]
        })
        st.plotly_chart(px.scatter(teachers, x='Тәжірибе', y='Рейтинг', size='Рейтинг', 
                                   hover_name='Аты-жөні', color='Аты-жөні', title="Тәжірибе vs Рейтинг"), use_container_width=True)

# 3. ЖИ БОЛЖАУ
elif selected == "🔮 ЖИ Болжау Орталығы":
    st.title("🔮 AI Predictive Center")
    st.write("Мұнда біз оқушының болашақтағы бағасын болжаймыз.")
    
    col_x, col_y = st.columns([1, 1])
    with col_x:
        st.subheader("Оқушы профилі")
        name = st.text_input("Есімі:", "Асель Мейремхан")
        attendance = st.slider("Сабаққа қатысу (%)", 0, 100, 95)
        homework = st.slider("Үй тапсырмасының сапасы (%)", 0, 100, 88)
        test = st.slider("Соңғы БЖБ бағасы", 0, 100, 92)
    
    with col_y:
        st.subheader("Талдау нәтижесі")
        # Болжам формуласы
        final = (attendance * 0.2) + (homework * 0.3) + (test * 0.5)
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = final,
            title = {'text': "Жетістік ықтималдығы (%)"},
            gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#1e3a8a"}}
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        if final > 90:
            st.success(f"🚀 {name} - Болжам: 'Алтын Белгі'. ЖИ бұл оқушыны мақтан тұтады!")
            st.balloons()

# 4. SMART ЭКОСИСТЕМА
elif selected == "💡 Smart Экосистема":
    st.title("💡 Smart Building & IoT")
    st.write("Мектеп ғимаратындағы ресурстарды басқару")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("💡 Электр қуаты", "Үнемдеу: 22%", "ЖИ режимі")
    c2.metric("🌡️ Температура", "21.5°C", "Норма")
    c3.metric("💧 Су шығыны", "450 л", "-10%")
    
    st.markdown("---")
    st.write("### 🏢 Мектеп картасы (Қауіпсіздік)")
    # Имитация карта
    img_data = np.random.randint(0, 255, (300, 700, 3), dtype=np.uint8)
    st.image(img_data, caption="Бейнебақылау ЖИ-аналитикасы: Күдікті әрекеттер жоқ", use_container_width=True)

# 5. AI КОНСУЛЬТАНТ
elif selected == "🤖 AI Консультант":
    st.title("🤖 Директордың ЖИ-Орынбасары")
    st.write("Кез келген басқарушылық сұрақ қойыңыз. Мен мектеп базасындағы барлық деректі білемін.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Чат интерфейсі
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if user_query := st.chat_input("Сұрақ жазыңыз (мысалы: Кесте қалай? Немесе Үнемдеу туралы...)"):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Дерекқорды талдау..."):
                time.sleep(1)
                q = user_query.lower()
                
                # Ақылды жауаптар
                if "кесте" in q:
                    ans = "Директор мырза, бүгінгі кесте толық оңтайландырылды. Мұғалімдердің 100%-ы өз орындарында. 'Смарт-кесте' бөлімінен толық көре аласыз."
                elif "ақша" in q or "бюджет" in q or "үнем" in q:
                    ans = "ЖИ-басқару арқылы осы айда ₸420,000 үнемдедік. Ең көп үнем жарық пен жылу жүйесінен келді."
                elif "сәлем" in q or "салем" in q:
                    ans = "Сәлеметсіз бе, Директор мырза! Қызметке дайынмын. Бүгін мектептегі білім сапасы 4.82 GPA-ға көтерілді."
                elif "оқушы" in q or "бала" in q:
                    ans = "Оқушылардың 95%-ы сабаққа қатысып жатыр. Тәртіп бойынша ешқандай шағым түскен жоқ."
                elif "мұғалім" in q or "педагог" in q:
                    ans = "Мұғалімдер рейтингінде Исаева М. көш бастап тұр. Оның сыныбындағы білім сапасы 98%."
                else:
                    ans = f"Директор мырза, '{user_query}' мәселесі бойынша нақты деректер жиналуда. Менің талдауымша, бұл мектептің жылдық даму жоспарына толық сәйкес келеді."
                
                st.write(ans)
                st.session_state.chat_history.append({"role": "assistant", "content": ans})