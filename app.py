import streamlit as st
import time
import re
from coach import CoachAI

# Configuración de la pestaña del navegador
st.set_page_config(page_title="CoachAI - Tu Entrenador con IA", page_icon="🏋️‍♂️", layout="centered")

# --- VARIABLES DE ESTADO DE LA APLICACIÓN ---
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "puntos" not in st.session_state:
    st.session_state.puntos = 0
if "nivel" not in st.session_state:
    st.session_state.nivel = "Amateur"
if "habilidades" not in st.session_state:
    st.session_state.habilidades = {}
if "habilidad_actual" not in st.session_state:
    st.session_state.habilidad_actual = None

# --- VARIABLES DE ESTADO DEL CRONÓMETRO ---
if "timer_activo" not in st.session_state:
    st.session_state.timer_activo = False
if "timer_pausado" not in st.session_state:
    st.session_state.timer_pausado = False
if "segundos_restantes" not in st.session_state:
    st.session_state.segundos_restantes = 0
if "segundos_totales" not in st.session_state:
    st.session_state.segundos_totales = 0

# --- TÍTULO DE LA PÁGINA ---
st.title("🏋️‍♂️ CoachAI Pro")
st.subheader("Tu entrenador personal con Árbol de Habilidades")
st.write("Mejorá tus estadísticas entrenando habilidades específicas de tu deporte.")

st.divider()

# --- PASO 1: CREACIÓN DE PERFIL ---
if st.session_state.usuario is None:
    st.markdown("### 👤 Creá tu perfil de deportista")
    nombre = st.text_input("¿Cómo te llamás?", placeholder="Ej: Franco")
    deporte = st.text_input("¿Qué deporte practicás?", placeholder="Ej: Básquet, Fútbol, Calistenia, Boxeo")
    
    if st.button("Crear Perfil y Empezar 🚀", use_container_width=True):
        if nombre and deporte:
            st.session_state.usuario = CoachAI(nombre, deporte)
            st.session_state.habilidades = st.session_state.usuario.skills
            st.rerun()
        else:
            st.warning("Por favor, completa ambos campos.")
else:
    # Sincronizamos los datos del objeto con el estado de Streamlit para no perder el progreso
    usuario = st.session_state.usuario
    usuario.streak_points = st.session_state.puntos
    usuario.level = st.session_state.nivel
    usuario.skills = st.session_state.habilidades

    # --- SIDEBAR (Panel de estadísticas del Jugador) ---
    with st.sidebar:
        st.header("🏆 Mi Personaje")
        st.write(f"**Usuario:** {usuario.username}")
        st.write(f"**Deporte:** {usuario.sport.capitalize()}")
        st.divider()
        st.metric(label="Puntos Totales", value=st.session_state.puntos)
        st.metric(label="Rango / Nivel", value=st.session_state.nivel)
        
        st.divider()
        st.subheader("📊 Habilidades de Deporte")
        
        # Renderizamos dinámicamente las barras de progreso de sus habilidades
        for skill, puntos_skill in st.session_state.habilidades.items():
            # Mostramos el nombre de la habilidad y su valor de progreso (0% a 100%)
            st.write(f"**{skill}** ({puntos_skill}/100 pts)")
            st.progress(puntos_skill / 100.0)
        
        st.divider()
        if st.button("Cerrar Sesión ❌", use_container_width=True):
            st.session_state.usuario = None
            st.session_state.puntos = 0
            st.session_state.nivel = "Amateur"
            st.session_state.habilidades = {}
            st.session_state.timer_activo = False
            st.rerun()

    # --- CUERPO PRINCIPAL (La app) ---
    st.markdown(f"### 👋 ¡Hola, {usuario.username}! ¿Qué habilidad querés entrenar hoy?")
    
    # Solo permitimos pedir rutina si el cronómetro no está corriendo
    if not st.session_state.timer_activo:
        estado = st.text_input(
            "Contale a la IA tu plan de hoy (Especificá qué querés trabajar):", 
            placeholder="Ej: Quiero practicar mi dribbling por 15 minutos, pero me duele la rodilla izquierda"
        )

        if st.button("Generar Rutina Personalizada 🤖✨", use_container_width=True):
            if estado:
                # 1. Buscamos el tiempo con Regex
                minutos_estimados = 30
                numeros_encontrados = re.findall(r'\d+', estado)
                if numeros_encontrados:
                    minutos_estimados = int(numeros_encontrados[0])
                
                # 2. Detectamos automáticamente qué habilidad se va a entrenar
                habilidad_detectada = usuario.detectar_habilidad_entrenada(estado)
                st.session_state.habilidad_actual = habilidad_detectada
                
                st.session_state.segundos_totales = minutos_estimados 
                st.session_state.segundos_restantes = minutos_estimados
                
                with st.spinner("🧠 Diseñando tu rutina enfocada en tu habilidad..."):
                    rutina_generada = usuario.generar_rutina_ia(estado)
                    st.session_state.rutina = rutina_generada
                    st.rerun()
            else:
                st.error("Por favor, escribí tu estado para que podamos diseñar tu entrenamiento.")

    # Si ya hay una rutina generada, la mostramos con su cronómetro
    if "rutina" in st.session_state:
        st.markdown("#### 📋 Tu Rutina Enfocada")
        st.success(f"🎯 **Habilidad objetivo detectada:** {st.session_state.habilidad_actual}")
        st.info(st.session_state.rutina)
        
        st.divider()
        st.markdown("### ⏱️ Cronómetro de Entrenamiento")
        
        # --- LÓGICA VISUAL DEL CRONÓMETRO ---
        if not st.session_state.timer_activo:
            st.write(f"Tiempo sugerido: **{st.session_state.segundos_totales} minutos** (Modo Demo: {st.session_state.segundos_totales} segundos).")
            if st.button("▶️ Iniciar Entrenamiento", use_container_width=True):
                st.session_state.timer_activo = True
                st.session_state.timer_pausado = False
                st.rerun()
        else:
            # Calculamos porcentaje para la barra de progreso del reloj
            progreso_actual = st.session_state.segundos_totales - st.session_state.segundos_restantes
            porcentaje = int((progreso_actual / st.session_state.segundos_totales) * 100)
            
            st.progress(porcentaje)
            st.write(f"⏳ Tiempo restante: **{st.session_state.segundos_restantes} min**")

            # Botones de control
            col1, col2 = st.columns(2)
            
            with col1:
                if st.session_state.timer_pausado:
                    if st.button("▶️ Reanudar", use_container_width=True):
                        st.session_state.timer_pausado = False
                        st.rerun()
                else:
                    if st.button("⏸️ Pausar", use_container_width=True):
                        st.session_state.timer_pausado = True
                        st.rerun()
                        
            with col2:
                if st.button("⏹️ Finalizar Antes", use_container_width=True):
                    minutos_entrenados = progreso_actual if progreso_actual > 0 else 1
                    puntos_ganados = usuario.registrar_entrenamiento(minutos_entrenados, st.session_state.habilidad_actual)
                    
                    st.session_state.puntos = usuario.streak_points
                    st.session_state.nivel = usuario.level
                    st.session_state.habilidades = usuario.skills
                    st.session_state.timer_activo = False
                    
                    st.warning(f"💪 Entrenamiento guardado. ¡Súmaste {puntos_ganados} puntos a {st.session_state.habilidad_actual}!")
                    del st.session_state.rutina
                    time.sleep(3)
                    st.rerun()

            # Lógica del motor del tiempo
            if not st.session_state.timer_pausado and st.session_state.segundos_restantes > 0:
                time.sleep(1)
                st.session_state.segundos_restantes -= 1
                st.rerun()
                
            elif st.session_state.segundos_restantes == 0:
                puntos_ganados = usuario.registrar_entrenamiento(st.session_state.segundos_totales, st.session_state.habilidad_actual)
                
                st.session_state.puntos = usuario.streak_points
                st.session_state.nivel = usuario.level
                st.session_state.habilidades = usuario.skills
                st.session_state.timer_activo = False
                
                st.balloons() 
                st.success(f"🎉 ¡Espectacular! Completaste el entrenamiento. ¡Sumaste {puntos_ganados} puntos a **{st.session_state.habilidad_actual}**!")
                del st.session_state.rutina
                time.sleep(3)
                st.rerun()