import streamlit as st
import random
import time
import math

st.set_page_config(page_title="Impostor - Modo Avanzado", layout="wide")

# --- MEMORIA GLOBAL (SERVIDOR) ---
@st.cache_resource
def obtener_servidor():
    return {
        "roles": [], 
        "nombres": [],
        "activo": False, 
        "version": 0,
    }

datos = obtener_servidor()

# --- INTERFAZ ---
st.title("🕵️ El JIKmpostor")
st.write(f"🟢 Partida: {'Activa' if datos['activo'] else 'Esperando'} | Ronda: {datos['version']}")

# --- PANEL DE CONTROL ---
with st.expander("⚙️ CONFIGURACIÓN DEL MASTER", expanded=not datos['activo']):
    
    # Bloque de Jugadores
    with st.expander("👥 JUGADORES", expanded=False):
        num_jugadores = st.number_input("Nº de Jugadores", 3, 20, 5)
        
        # NUEVO: Toggle de múltiples impostores
        multi_impostor_toggle = st.toggle("Permitir múltiples impostores", value=False)
        if multi_impostor_toggle:
            max_posible = math.floor(num_jugadores * 0.25)
            st.caption(f"ℹ️ Con {num_jugadores} jugadores, puede haber hasta {max(1, max_posible)} impostores (10% de probabilidad).")
        
        st.divider()
        nombres_temporales = []
        for i in range(num_jugadores):
            n = st.text_input(f"Nombre Jugador {i+1}", value=f"Jugador {i+1}", key=f"input_{i}")
            nombres_temporales.append(n)
        
        if st.button("🆕 GENERAR PARTIDA NUEVA (Reset Rondas)"):
            datos["activo"] = False
            datos["roles"] = []
            datos["nombres"] = nombres_temporales
            datos["version"] = 0
            st.success("Configuración guardada. Contador de rondas a 0.")
            st.rerun()

    st.divider()
    
    # Bloque de Ronda
    palabra = st.text_input("Palabra Secreta", placeholder="Escribe la palabra de esta ronda...")
    
    if st.button("🚀 SIGUIENTE RONDA"):
        if palabra and datos["nombres"]:
            n = len(datos["nombres"])
            num_impostores = 1 # Por defecto siempre 1
            
            # Lógica de Múltiples Impostores
            if multi_impostor_toggle:
                # 10% de probabilidad de tener más de 1
                if random.random() < 0.10:
                    max_impostores = math.floor(n * 0.25)
                    if max_impostores > 1:
                        num_impostores = random.randint(2, max_impostores)
            
            # Crear la lista de roles
            lista_roles = [palabra] * (n - num_impostores)
            for _ in range(num_impostores):
                lista_roles.append("🚨 ¡ERES EL IMPOSTOR!")
            
            # Mezclar roles
            random.shuffle(lista_roles)
            
            datos["roles"] = lista_roles
            datos["activo"] = True
            datos["version"] += 1
            st.success(f"¡Ronda {datos['version']} iniciada! (Impostores secretos)")
            st.rerun()
        else:
            st.error("Asegúrate de haber 'Generado Partida' con nombres y escribir una palabra.")

st.divider()

# --- VISTA DE JUGADOR ---
if datos["activo"]:
    st.subheader(f"📍 Jugando Ronda: {datos['version']}")
    
    tabs = st.tabs(datos["nombres"])
    
    for i, tab in enumerate(tabs):
        with tab:
            st.write(f"### Hola, {datos['nombres'][i]}")
            
            # Botón de desvelar con temporizador de 5 segundos
            if st.button(f"👁️ Ver mi palabra", key=f"btn_v{datos['version']}_j{i}"):
                placeholder = st.empty()
                
                placeholder.markdown(f"""
                <div style="background-color: #262730; padding: 30px; border-radius: 15px; border: 3px solid #FF4B4B; text-align: center;">
                    <p style="color: #888; font-size: 18px;">Tu rol es:</p>
                    <h1 style="color: white; font-size: 50px;">{datos['roles'][i]}</h1>
                    <p style="color: #FF4B4B; font-size: 14px;">Se ocultará en 5 segundos...</p>
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(5)
                placeholder.empty()
                st.info("Palabra oculta. Puedes volver a pulsar para verla.")

else:
    st.info("Configura los jugadores y pulsa 'Siguiente Ronda' para empezar.")

# Autorefresco pasivo
time.sleep(3)
st.rerun()
