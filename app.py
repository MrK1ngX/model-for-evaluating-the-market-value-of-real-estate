import streamlit as st
from predict import predict_price
import plotly.graph_objects as go
import subprocess

PORT = 80
APP_FILE = "app.py"

subprocess.run([
    "streamlit",
    "run",
    APP_FILE,
    f"--server.port={PORT}"
])
# 1. Настройка страницы
st.set_page_config(page_title="Модель для оценки рыночной стоимости недвижимости", page_icon="🏠", layout="wide")

# 2. Инициализация памяти
if 'lang' not in st.session_state: st.session_state.lang = None  
if 'theme' not in st.session_state: st.session_state.theme = 'light'
if 'history' not in st.session_state: st.session_state.history = []

# --- ФУНКЦИИ ---
def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

# 3. ПЕРЕВОДЫ
translations = {
    "ru": {
        "title": "Оценка недвижимости",
        "theme_btn": "СМЕНИТЬ ТЕМУ 🌗",
        "area": "Площадь (м²)", "rooms": "Комнат", "floor": "Этаж", "max_floor": "Всего этажей",
        "age": "Возраст дома", "wall": "Тип стен",
        "renov": "Евроремонт ✨", "balcony": "Балкон", "elevator": "Лифт",
        "calc_btn": "РАССЧИТАТЬ СТОИМОСТЬ", "result": "ИТОГО",
        "currency": "₽",
        "welcome": "Модель для оценки рыночной стоимости",
        "welcome_sub": "Выберите язык для начала работы",
        "history_title": "📜 Последние расчеты",
        "chart_impact": "Влияние факторов", "chart_compare": "Сравнение с рынком",
        "infra_chart": "Инфраструктура", "state_chart": "Состояние",
        "your_price": "Ваша оценка", "avg_price": "Средняя по рынку",
        "hero_title": "Точная оценка за пару кликов",
        "hero_sub": "Основано на машинном обучении и реальных данных",
        "walls": ["Кирпичные", "Панельные", "Монолитные", "Смешанные"],
        "extra_params": "Дополнительные параметры",
        "infra": {
            "schools": "Школы", "kinder": "Детсады", "grocery": "Продуктовые", 
            "transp": "Остановки", "banks": "Банки", "subway": "Метро",
            "cafes": "Кафе", "bars": "Бары", "pizza": "Пиццерии",
            "clothes": "Магазины одежды", "malls": "ТЦ", "cinema": "Кинотеатры",
            "parks": "Парки", "univer": "ВУЗы", "clinics": "Детск. поликлиники",
            "dental": "Стоматологии", "post": "Почта", "filling": "Заправки"
        }
    },
    "en": {
        "title": "Property Valuation",
        "theme_btn": "CHANGE THEME 🌗",
        "area": "Area (m²)", "rooms": "Rooms", "floor": "Floor", "max_floor": "Total floors",
        "age": "Building Age", "wall": "Wall Type",
        "renov": "Renovation ✨", "balcony": "Balcony", "elevator": "Elevator",
        "calc_btn": "CALCULATE PRICE", "result": "TOTAL",
        "currency": "₽",
        "welcome": "Model for market value assessment",
        "welcome_sub": "Select a language to start",
        "history_title": "📜 Recent Activity",
        "chart_impact": "Feature Impact", "chart_compare": "Market Comparison",
        "infra_chart": "Infrastructure", "state_chart": "Condition",
        "your_price": "Your Price", "avg_price": "Market Average",
        "hero_title": "Accurate valuation in a few clicks",
        "hero_sub": "Based on machine learning and real data",
        "walls": ["Brick", "Panel", "Monolithic", "Mixed"],
        "extra_params": "Additional parameters",
        "infra": {
            "schools": "Schools", "kinder": "Kindergartens", "grocery": "Grocery Stores", 
            "transp": "Transport Stops", "banks": "Banks", "subway": "Subway",
            "cafes": "Cafes", "bars": "Bars", "pizza": "Pizzerias",
            "clothes": "Clothing Stores", "malls": "Shopping Malls", "cinema": "Cinemas",
            "parks": "Parks", "univer": "Universities", "clinics": "Child Clinics",
            "dental": "Dental Clinics", "post": "Post Offices", "filling": "Gas Stations"
        }
    }
}

# 4. ЦВЕТОВАЯ ПАЛИТРА
pastel_pink = "#FCE4EC"
accent_purple = "#CE93D8" 
accent_pink = "#F06292"   
dark_text = "#2C3E50"     

if st.session_state.theme == 'light':
    bg_style = "linear-gradient(135deg, #E0F2F1 0%, #E1BEE7 100%)"
    input_bg, text_color, renov_text_color = pastel_pink, dark_text, dark_text
    shadow_soft = "rgba(103, 58, 183, 0.15)"
else:
    bg_style = "linear-gradient(135deg, #1A237E 0%, #4A148C 100%)"
    input_bg, text_color, renov_text_color = "#2D2D44", "#FFFFFF", "#000000"
    shadow_soft = "rgba(0, 0, 0, 0.3)"

# 5. CSS
st.markdown(f"""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css');
    [data-testid="stHeader"], .stDeployButton, [data-testid="stNotification"] {{ display: none !important; }}
    .stApp {{ background: {bg_style} !important; background-attachment: fixed !important; }}
    
    label, p {{
    color: {text_color} !important;
    font-weight: 800 !important;
    font-family: 'Segoe UI', sans-serif !important;
    }}
    div[data-testid="stCheckbox"] label p {{ color: {renov_text_color} !important; font-weight: 900 !important; }}

    /* ЭКРАН ЯЗЫКА С ФОНОМ МНОГОЭТАЖЕК */
    .language-screen {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7)), url('https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?q=80&w=2070&auto=format&fit=crop');
        background-size: cover; background-position: center; border-radius: 30px; 
        padding: 100px 20px; text-align: center; margin-top: 50px; 
        box-shadow: 10px 10px 30px rgba(0,0,0,0.5);
    }}
    .lang-title {{ color: #FFFFFF !important; font-size: 3.5rem !important; font-weight: 900 !important; text-shadow: 2px 2px 10px rgba(0,0,0,0.8); margin-bottom: 10px; }}
    .lang-sub {{ color: #E3F2FD !important; font-size: 1.5rem !important; font-weight: 600 !important; margin-bottom: 40px; }}

    /* HERO */
    .hero-banner {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.6)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070&auto=format&fit=crop');
        background-size: cover; background-position: center; border-radius: 24px;
        padding: 80px 20px; text-align: center; margin-top: 10px; margin-bottom: 30px;
        box-shadow: 8px 8px 20px {shadow_soft};
        animation: fadeInDown 1s;
    }}

    /* ПОЛЯ ВВОДА */
    button, input, div[data-baseweb="select"] > div {{ border: none !important; outline: none !important; }}
    div[data-baseweb="base-input"], div[data-baseweb="select"] > div:first-child {{
        background-color: {input_bg} !important; border-radius: 14px !important;
        box-shadow: inset 4px 4px 10px {shadow_soft} !important;
    }}
    input, div[data-baseweb="select"] * {{ color: {text_color} !important; -webkit-text-fill-color: {text_color} !important; }}

    /* КНОПКИ +/- */
    div[data-testid="stNumberInput"] button {{
        background-color: {accent_purple} !important; color: white !important; border-radius: 12px !important;
        box-shadow: 4px 4px 8px {shadow_soft} !important; margin: 0 1px !important; width: 42px !important; height: 42px !important; font-size: 24px !important;
    }}
    div[data-testid="stNumberInput"] > div > div {{ display: flex; justify-content: center; gap: 2px; }}

    /* --- КНОПКА ДОП ПАРАМЕТРОВ --- */
    details[data-testid="stExpander"] {{
        background-color: {accent_pink} !important;
        border-radius: 18px !important;
        box-shadow: 6px 6px 15px {shadow_soft} !important;
        border: none !important;
        margin-bottom: 25px !important;
    }}
    
    details[data-testid="stExpander"] summary [data-testid="stIconMaterial"],
    details[data-testid="stExpander"] summary svg,
    details[data-testid="stExpander"] summary .material-icons,
    details[data-testid="stExpander"] summary i {{
        display: none !important; opacity: 0 !important; font-size: 0px !important; color: transparent !important; width: 0px !important; height: 0px !important; content: "" !important;
    }}
    
    details[data-testid="stExpander"] summary {{
        color: transparent !important; list-style: none !important; display: block !important; text-align: center !important; padding: 15px !important;
    }}
    details[data-testid="stExpander"] summary::-webkit-details-marker {{ display: none !important; }}
    
    details[data-testid="stExpander"] summary p {{
        color: white !important; font-size: 20px !important; font-weight: bold !important; margin: 0 auto !important; display: block !important; text-align: center !important;
    }}

    /* ВНУТРЕННЯЯ ПАНЕЛЬ ПАРАМЕТРОВ */
    div[data-testid="stExpanderDetails"] {{
        background-color: {input_bg} !important; border-radius: 0 0 18px 18px !important; padding: 20px !important;
    }}
    div[data-testid="stExpanderDetails"] p, div[data-testid="stExpanderDetails"] label {{
        color: {text_color} !important;
    }}

    /* ГЛАВНАЯ КНОПКА */
    div.stButton > button {{
        background: {accent_pink} !important; color: white !important; border-radius: 18px !important;
        box-shadow: 6px 6px 15px {shadow_soft} !important; height: 65px; font-size: 22px !important; font-weight: bold !important;
    }}

    /* ГРАФИКИ (ИСПРАВЛЕНО СМЕЩЕНИЕ ВПРАВО) */
    div[data-testid="stPlotlyChart"] {{
        background-color: rgba(255, 255, 255, 0.15); 
        border-radius: 24px; 
        /* УБРАН PADDING: 15px; так как он ломал ширину и сдвигал график вправо */
        box-shadow: 10px 10px 25px {shadow_soft} !important; 
        backdrop-filter: blur(10px);
        overflow: hidden;
    }}

    /* ИСТОРИЯ */
    .history-card {{
        background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(5px); border-radius: 18px; padding: 15px; margin-bottom: 10px; color: {text_color} !important;
        border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 6px 6px 12px {shadow_soft}; text-align: center;
    }}
    </style>
""", unsafe_allow_html=True)

def main():
    if st.session_state.lang is None:
        st.markdown(f"""
        <div class="language-screen animate__animated animate__fadeIn">
            <div class="lang-title">{translations['ru']['welcome']}</div>
            <div class="lang-sub">{translations['ru']['welcome_sub']}</div>
        </div>
        """, unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            col_ru, col_en = st.columns(2)
            if col_ru.button("РУССКИЙ 🇷🇺", use_container_width=True): st.session_state.lang = 'ru'; st.rerun()
            if col_en.button("ENGLISH 🇺🇸", use_container_width=True): st.session_state.lang = 'en'; st.rerun()
        return

    t = translations[st.session_state.lang]

    col_t1, col_t2 = st.columns([8, 2])
    with col_t2:
        st.button(t["theme_btn"], on_click=toggle_theme)
        if st.button("🌐 LANG"): st.session_state.lang = None; st.rerun()

    st.markdown(f"""<div class="hero-banner"><div style="color:white; font-size:3.5rem; font-weight:900; text-shadow: 2px 2px 10px rgba(0,0,0,0.8);">{t['hero_title']}</div><div style="color:#E3F2FD; font-size:1.5rem;">{t['hero_sub']}</div></div>""", unsafe_allow_html=True)

    # ОСНОВНЫЕ ПАРАМЕТРЫ
    col_params, col_img = st.columns([1, 1], gap="small")
    with col_params:
        in_col1, in_col2 = st.columns(2)
        with in_col1:
            area = st.number_input(t["area"], 10.0, 500.0, 45.0)
            rooms = st.number_input(t["rooms"], 1, 10, 2)
            floor = st.number_input(t["floor"], 1, 100, 5)
            max_floor = st.number_input(t["max_floor"], 1, 100, 9)
            age = st.number_input(t["age"], 0, 200, 15)
        with in_col2:
            wall_type = st.selectbox(t["wall"], t["walls"])
            st.markdown("<br>", unsafe_allow_html=True)
            renov = st.checkbox(t["renov"], value=True)
            balcony = st.checkbox(t["balcony"], value=True)
            elevator = st.checkbox(t["elevator"], value=True)

    with col_img:
        st.image("https://images.unsplash.com/photo-1523217582562-09d0def993a6?auto=format&fit=crop&w=1200&q=80", use_container_width=True)

    # ДОП ПАРАМЕТРЫ
    infra = t["infra"]
    with st.expander(t["extra_params"]):
        i_col1, i_col2, i_col3 = st.columns(3)
        with i_col1:
            schools = st.number_input(infra["schools"], 0, 50, 2)
            kinder = st.number_input(infra["kinder"], 0, 50, 3)
            grocery = st.number_input(infra["grocery"], 0, 50, 5)
            transp = st.number_input(infra["transp"], 0, 50, 4)
            banks = st.number_input(infra["banks"], 0, 50, 2)
            subway = st.number_input(infra["subway"], 0, 10, 0)
        with i_col2:
            cafes = st.number_input(infra["cafes"], 0, 50, 2)
            bars = st.number_input(infra["bars"], 0, 50, 1)
            pizza = st.number_input(infra["pizza"], 0, 50, 1)
            clothes = st.number_input(infra["clothes"], 0, 50, 1)
            malls = st.number_input(infra["malls"], 0, 20, 1)
            cinema = st.number_input(infra["cinema"], 0, 10, 0)
        with i_col3:
            parks = st.number_input(infra["parks"], 0, 20, 0)
            univer = st.number_input(infra["univer"], 0, 20, 0)
            clinics = st.number_input(infra["clinics"], 0, 20, 1)
            dental = st.number_input(infra["dental"], 0, 30, 1)
            post = st.number_input(infra["post"], 0, 20, 1)
            filling = st.number_input(infra["filling"], 0, 20, 1)

    # РАСЧЕТ
    if st.button(t["calc_btn"], use_container_width=True):
        try:
            wall_mapping = {"Brick": "Кирпичные", "Panel": "Панельные", "Monolithic": "Монолитные", "Mixed": "Смешанные"}
            w_model = wall_mapping.get(wall_type, wall_type)
            
            price = predict_price(
                RoomsCount=int(rooms), TotalArea=float(area), BuildingAge=int(age),
                FloorType="Первый" if floor == 1 else "Последний" if floor == max_floor else "Не первый и не последний",
                WallType=w_model, RepairType="Евроремонт" if renov else "Косметический ремонт",
                BalconyBlockPresence="Да" if balcony else "Нет", ElevatorPresence="Да" if elevator else "Нет",
                BanksCount=int(banks), BarsCount=int(bars), KindergartensCount=int(kinder),
                FillingStationsCount=int(filling), CafesCount=int(cafes), CinemasCount=int(cinema),
                SubwayStationcCount=int(subway), ClothingStoresCount=int(clothes),
                PublicTransportStopsCount=int(transp), CulturalParksCount=int(parks),
                PizzeriasCount=int(pizza), ChildsClinicsCount=int(clinics),
                PostOfficesCount=int(post), DentalClinicsCount=int(dental),
                GroceryStoresCount=int(grocery), ShoppingMallsCount=int(malls),
                UniversitiesCount=int(univer), SchoolsCount=int(schools)
            )
            
            p_str = f"{price:,.0f}".replace(",", " ")
            st.session_state.history.insert(0, {"p": p_str, "a": area, "r": rooms})
            if len(st.session_state.history) > 4: st.session_state.history.pop()

            st.markdown(f"<div class='animate__animated animate__zoomIn' style='text-align:center; padding:25px; border-radius:20px; background:{pastel_pink}; color:{accent_pink}; font-size:36px; font-weight:bold; box-shadow:inset 4px 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px;'>{t['result']}: {p_str} {t['currency']}</div>", unsafe_allow_html=True)
            
            # ИДЕАЛЬНО ОТЦЕНТРОВАННЫЕ ГРАФИКИ
            c1, c2 = st.columns(2)
            with c1:
                fig1 = go.Figure(data=[go.Pie(
                    labels=[t['area'], t['infra_chart'], t['state_chart']], values=[50, 30, 20], 
                    hole=.3, pull=[0.05, 0.05, 0.05], 
                    marker=dict(colors=[accent_pink, accent_purple, "#81D4FA"], line=dict(color='white', width=3)),
                    insidetextfont=dict(size=16, color='white', family='Segoe UI')
                )])
                # Выравнивание x=0.5 и margin=20 удерживает график ровно по центру холста
                fig1.update_layout(
                    title=dict(text=t['chart_impact'], font=dict(color=text_color, size=20), x=0.5, xanchor='center'), 
                    paper_bgcolor='rgba(0,0,0,0)', showlegend=False,
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                st.plotly_chart(fig1, use_container_width=True)
            with c2:
                fig2 = go.Figure(data=[
                    go.Bar(name=t['your_price'], x=[t['your_price']], y=[price], marker=dict(color=accent_pink, line=dict(color='white', width=3))),
                    go.Bar(name=t['avg_price'], x=[t['avg_price']], y=[price*0.92], marker=dict(color=accent_purple, line=dict(color='white', width=3)))
                ])
                fig2.update_layout(
                    title=dict(text=t['chart_compare'], font=dict(color=text_color, size=20), x=0.5, xanchor='center'), 
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, 
                    xaxis=dict(tickfont=dict(color=text_color)), yaxis=dict(tickfont=dict(color=text_color)), barmode='group',
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                st.plotly_chart(fig2, use_container_width=True)

        except Exception as e: st.error(f"Error: {e}")

    # ИСТОРИЯ
    if st.session_state.history:
        st.markdown(f"<br><h3 style='color:{text_color}; text-align:center;'>{t['history_title']}</h3>", unsafe_allow_html=True)
        h_cols = st.columns(len(st.session_state.history))
        for i, item in enumerate(st.session_state.history):
            with h_cols[i]:
                st.markdown(f"<div class='history-card'><b>{item['p']} {t['currency']}</b><br><span>{item['a']} м² • {item['r']} комн.</span></div>", unsafe_allow_html=True)

if __name__ == "__main__": main()