import streamlit as st
import random
import time

st.set_page_config(page_title="Impostor Pro", layout="wide")

# --- MEMORIA GLOBAL (SERVIDOR) ---
@st.cache_resource
def obtener_servidor():
    return {
        "roles": [], 
        "nombres": [],
        "activo": False, 
        "version": 0,  # Este es el contador de rondas
    }

datos = obtener_servidor()

# --- INTERFAZ ---
st.write(f"🟢 Partida: {'Activa' if datos['activo'] else 'Esperando'} | Ronda: {datos['version']}")
st.title("🕵️ El Impostor")

# --- PANEL DE CONTROL ---
with st.expander("🎮 PANEL DEL MASTER", expanded=True):
    
    # 1. Sección de Jugadores (Cerrada por defecto)
    with st.expander("👥 CONFIGURAR JUGADORES", expanded=False):
        num_jugadores = st.number_input("Nº de Jugadores", 3, 20, 5)
        st.write("### Edición de Nombres:")
        nombres_temporales = []
        for i in range(num_jugadores):
            n = st.text_input(f"Jugador {i+1}", value=f"Jugador {i+1}", key=f"input_{i}")
            nombres_temporales.append(n)

    st.divider()
    
    # 2. Configuración de Ronda
    palabra = st.text_input("Palabra Secreta para esta ronda")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 SIGUIENTE RONDA (Nueva Palabra)"):
            if palabra:
                # Generar y mezclar
                lista_roles = [palabra] * (int(num_jugadores) - 1)
                lista_roles.append("🚨 ¡ERES EL IMPOSTOR!")
                random.shuffle(lista_roles)
                
                # Actualizar datos globales
                datos["roles"] = lista_roles
                datos["nombres"] = nombres_temporales
                datos["activo"] = True
                datos["version"] += 1 # Aumenta la ronda y limpia checkboxes
                st.success(f"¡Ronda {datos['version']} generada!")
                st.rerun()
            else:
                st.error("Introduce la palabra secreta")

    with col2:
        if st.button("🧹 RESET TOTAL (Nueva Partida)"):
            datos["activo"] = False
            datos["roles"] = []
            datos["nombres"] = []
            datos["version"] = 0 # Resetea el contador
            st.warning("Juego reseteado desde cero.")
            st.rerun()

st.divider()

# --- VISTA DE JUGADOR ---
if datos["activo"]:
    st.subheader(f"📍 Ronda actual: {datos['version']}")
    
    tabs = st.tabs(datos["nombres"])
    
    for i, tab in enumerate(tabs):
        with tab:
            st.write(f"### Hola, {datos['nombres'][i]}")
            # La key ligada a la versión hace que al cambiar de ronda, se desmarque solo
            if st.checkbox(f"Ver mi palabra", key=f"ronda_{datos['version']}_j_{i}"):
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 2px solid #FF4B4B; text-align: center;">
                    <h1 style="color: #FF4B4B;">{datos['roles'][i]}</h1>
                </div>
                """, unsafe_allow_html=True)
else:
    st.info("El Master debe configurar los jugadores y la palabra para empezar.")

# Autorefresco cada 3 segundos
time.sleep(3)
st.rerun()
