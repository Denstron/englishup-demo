import random
import streamlit as st
import pandas as pd

st.set_page_config(page_title="EnglishUp Colombia", page_icon="🎓", layout="wide")

# ---------------- DATOS DEMO ----------------
NIVELES = ["A1", "A2", "B1", "B2"]

QUIZ = {
    "A1": [
        ("Choose the correct option: She ___ a student.", ["am", "is", "are"], "is"),
        ("What is the plural of 'book'?", ["books", "bookes", "bookies"], "books"),
        ("Hello! How ___ you?", ["is", "are", "am"], "are"),
    ],
    "A2": [
        ("Yesterday I ___ to the park.", ["go", "went", "gone"], "went"),
        ("There ___ two apples on the table.", ["is", "are", "be"], "are"),
        ("She is ___ than her sister.", ["tall", "taller", "tallest"], "taller"),
    ],
    "B1": [
        ("If it rains, we ___ at home.", ["stay", "will stay", "stayed"], "will stay"),
        ("I have lived here ___ 2020.", ["for", "since", "during"], "since"),
        ("The book ___ by a famous author.", ["wrote", "was written", "is writing"], "was written"),
    ],
    "B2": [
        ("If I had known, I ___ you.", ["would tell", "would have told", "told"], "would have told"),
        ("He suggested ___ earlier.", ["to leave", "leaving", "leave"], "leaving"),
        ("By next year she ___ her degree.", ["will finish", "will have finished", "finishes"], "will have finished"),
    ],
}

ICFES = {
    "Parte 1 · Avisos y letreros": ("A sign says: 'NO PARKING'. What does it mean?", ["You can park here", "You cannot park here", "Parking is free"], "You cannot park here"),
    "Parte 2 · Vocabulario / definiciones": ("A place where you borrow books:", ["Library", "Bakery", "Pharmacy"], "Library"),
    "Parte 3 · Conversaciones": ("A: 'How are you?'  B: '___'", ["I'm fine, thanks", "It's Monday", "At home"], "I'm fine, thanks"),
    "Parte 4 · Comprensión lectora corta": ("'Tom wakes up at 6 and runs before school.' When does Tom run?", ["After school", "Before school", "At night"], "Before school"),
    "Parte 5 · Gramática": ("She ___ TV every night.", ["watch", "watches", "watching"], "watches"),
    "Parte 6 · Cloze (completar texto)": ("'I ___ my homework before dinner.'", ["do", "does", "doing"], "do"),
    "Parte 7 · Lectura extensa": ("'Maria loves animals, so she works at a vet clinic.' Why does she work there?", ["She needs money only", "She loves animals", "She hates people"], "She loves animals"),
}

MALLAS = {
    "Primaria": {
        "Grado 1-3": ["Saludos y presentaciones", "Colores, números, animales", "Familia y objetos del salón"],
        "Grado 4-5": ["Rutinas diarias", "Comida y lugares de la ciudad", "Descripciones simples"],
    },
    "Secundaria": {
        "Grado 6-7": ["Presente y pasado simple", "Comparativos y superlativos", "Lectura de textos cortos"],
        "Grado 8-9": ["Futuro y condicionales", "Voz pasiva básica", "Escritura de párrafos"],
        "Grado 10-11": ["Preparación Saber 11 / Icfes", "Tiempos perfectos", "Comprensión lectora avanzada"],
    },
    "Universidad": {
        "Ciclo 1-2": ["Inglés académico básico", "Presentaciones orales", "Lectura de artículos"],
        "Ciclo 3-4": ["Redacción académica", "Preparación B2", "Inglés para la profesión"],
    },
}

PARES = {
    "A1": {"dog": "perro", "house": "casa", "book": "libro", "water": "agua"},
    "A2": {"travel": "viajar", "weather": "clima", "borrow": "pedir prestado", "habit": "hábito"},
    "B1": {"achieve": "lograr", "improve": "mejorar", "environment": "medio ambiente", "advice": "consejo"},
    "B2": {"reliable": "confiable", "overcome": "superar", "reach": "alcanzar", "although": "aunque"},
}

# ---------------- ESTADO ----------------
ss = st.session_state
ss.setdefault("puntos", 0)
ss.setdefault("equipos", {"Equipo Azul": 0, "Equipo Rojo": 0})


def quiz_ui(preguntas, key):
    respuestas = {}
    for i, (q, ops, ans) in enumerate(preguntas):
        respuestas[i] = st.radio(q, ops, index=None, key=f"{key}_{i}")
    if st.button("Calificar", key=f"{key}_btn"):
        ok = sum(1 for i, (_, _, ans) in enumerate(preguntas) if respuestas[i] == ans)
        st.success(f"Resultado: {ok}/{len(preguntas)}")
        ss.puntos += ok * 10
        if ok == len(preguntas):
            st.balloons()


# ---------------- SIDEBAR ----------------
st.sidebar.title("🎓 EnglishUp Colombia")
rol = st.sidebar.selectbox("Rol (demo)", ["Estudiante", "Docente", "Administrador institución"])
nivel = st.sidebar.selectbox("Nivel MCER", NIVELES)
st.sidebar.metric("⭐ Puntos", ss.puntos)

menu = ["🏠 Inicio", "📘 Actividades y evaluación", "🎮 Juegos", "📝 Icfes y simulacros", "📚 Mallas curriculares", "💳 Planes y pagos"]
if rol != "Estudiante":
    menu.append("📊 Panel docente / institución")
pagina = st.sidebar.radio("Menú", menu)

# ---------------- PÁGINAS ----------------
if pagina == "🏠 Inicio":
    st.title("EnglishUp Colombia")
    st.caption("Plataforma para aprender inglés · Colegios (primaria y secundaria) y universidades")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Niveles", "A1 – B2")
    c2.metric("Partes Icfes", "7")
    c3.metric("Capacidad", "800 usuarios")
    c4.metric("Juegos", "Individual y grupal")
    st.markdown("""
**Qué incluye**
- Actividades, talleres y evaluaciones por nivel (A1, A2, B1, B2)
- Juegos didácticos individuales y por equipos
- Preparación Icfes (7 partes) y simulacros por nivel
- Mallas curriculares alineadas a la normativa colombiana
- Panel para docentes e instituciones
- Planes mensual, trimestral, semestral y anual con descuentos
""")
    st.info("Esto es un demo de la idea. Los contenidos son de ejemplo.")

elif pagina == "📘 Actividades y evaluación":
    st.header(f"Nivel {nivel}")
    t1, t2, t3 = st.tabs(["Actividad", "Taller", "Evaluación"])
    with t1:
        st.subheader("Actividad rápida")
        quiz_ui(QUIZ[nivel][:2], f"act_{nivel}")
    with t2:
        st.subheader("Taller guiado")
        st.write("Escribe 3 frases usando el tema del nivel y guárdalas.")
        txt = st.text_area("Tu taller", key=f"taller_{nivel}")
        if st.button("Enviar taller"):
            st.success("Taller enviado al docente ✅" if txt.strip() else "Escribe algo primero.")
    with t3:
        st.subheader("Evaluación del nivel")
        quiz_ui(QUIZ[nivel], f"eval_{nivel}")

elif pagina == "🎮 Juegos":
    st.header("Juegos didácticos")
    modo = st.radio("Modo", ["Individual", "Grupal (equipos)"], horizontal=True)
    juego = st.selectbox("Juego", ["Emparejar palabras", "Trivia relámpago"])
    if juego == "Emparejar palabras":
        pares = PARES[nivel]
        esp = list(pares.values())
        random.Random(nivel).shuffle(esp)
        resp = {}
        for en in pares:
            resp[en] = st.selectbox(en, ["—"] + esp, key=f"par_{nivel}_{en}")
        if st.button("Verificar"):
            ok = sum(1 for en, v in resp.items() if v == pares[en])
            st.success(f"Aciertos: {ok}/{len(pares)}")
            if modo.startswith("Individual"):
                ss.puntos += ok * 5
            else:
                eq = st.session_state.get("eq_sel", "Equipo Azul")
                ss.equipos[eq] += ok * 5
    else:
        quiz_ui(QUIZ[nivel], f"trivia_{nivel}")
    if modo.startswith("Grupal"):
        st.selectbox("Equipo que juega", list(ss.equipos), key="eq_sel")
        st.subheader("🏆 Marcador")
        st.bar_chart(pd.Series(ss.equipos))

elif pagina == "📝 Icfes y simulacros":
    st.header("Preparación Icfes (Saber 11 – Inglés)")
    t1, t2 = st.tabs(["Práctica por parte", "Simulacro"])
    with t1:
        parte = st.selectbox("Parte", list(ICFES))
        q, ops, ans = ICFES[parte]
        quiz_ui([(q, ops, ans)], f"icfes_{parte}")
    with t2:
        st.write(f"Simulacro nivel **{nivel}** (1 pregunta por parte, con tiempo en la versión final).")
        preguntas = list(ICFES.values())
        quiz_ui(preguntas, f"sim_{nivel}")
    st.caption("Estructura de 7 partes de ejemplo; ajustar con el docente según el formato oficial vigente.")

elif pagina == "📚 Mallas curriculares":
    st.header("Mallas curriculares")
    st.caption("Alineadas a lineamientos del MEN (Estándares Básicos de Competencias en Lengua Extranjera: Inglés).")
    ciclo = st.selectbox("Institución", list(MALLAS))
    for grado, temas in MALLAS[ciclo].items():
        with st.expander(grado, expanded=True):
            for t in temas:
                st.markdown(f"- {t}")

elif pagina == "💳 Planes y pagos":
    st.header("Planes")
    precio = st.number_input("Precio mensual por usuario (COP)", 5000, 200000, 25000, step=1000)
    planes = [("Mensual", 1, 0), ("Trimestral", 3, 10), ("Semestral", 6, 15), ("Anual", 12, 25)]
    cols = st.columns(4)
    for col, (n, m, d) in zip(cols, planes):
        total = precio * m * (1 - d / 100)
        with col:
            st.subheader(n)
            st.metric("Total", f"${total:,.0f}")
            st.caption(f"{d}% descuento" if d else "Sin descuento")
            st.caption(f"≈ ${total/m:,.0f} / mes")
            st.button(f"Elegir {n}", key=f"plan_{n}")
    st.info("Pagos reales (Wompi / MercadoPago / PayU) se integran en la siguiente fase.")

elif pagina == "📊 Panel docente / institución":
    st.header("Panel")
    c1, c2, c3 = st.columns(3)
    c1.metric("Usuarios activos", "412 / 800")
    c2.metric("Docentes", "28")
    c3.metric("Estudiantes", "384")
    df = pd.DataFrame({
        "Estudiante": ["Ana", "Luis", "Sofía", "Juan", "Marta"],
        "Nivel": ["A1", "A2", "B1", "B2", "A2"],
        "Puntos": [120, 240, 310, 405, 190],
        "Último simulacro": [58, 64, 72, 81, 60],
    })
    st.dataframe(df, use_container_width=True)
    st.bar_chart(df.set_index("Estudiante")["Último simulacro"])
    st.caption("Datos de ejemplo. En producción: Google Sheets/Supabase con login por rol.")
