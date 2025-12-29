import streamlit as st
import random
import time

# Configuración de página
st.set_page_config(page_title="Impostor - Nombres Individuales", layout="wide")

# --- MEMORIA GLOBAL (SERVIDOR) ---
@st.cache_resource
def obtener_servidor():
    return {
        "roles": [], 
        "nombres": [],
        "activo": False, 
        "version": 0, 
        "ultima_actualizacion": time.time()
    }

datos = obtener_servidor()

st.write(f"🟢 Estado: Conectado (Ronda {datos['version']})")
st.title("🕵️ El Impostor")

# --- PANEL DE CONTROL ---
with st.expander("🎮 CONFIGURACIÓN DE PARTIDA", expanded=not datos["activo"]):
    num_jugadores = st.number_input("Nº de Jugadores", 3, 20, 5)
    
    # Creamos campos de texto dinámicos para los nombres
    st.write("### Nombres de los jugadores:")
    nombres_temporales = []
    
    # Creamos columnas para que los campos de nombre no ocupen tanto espacio hacia abajo
    cols = st.columns(2) 
    for i in range(num_jugadores):
        # Repartimos los inputs en las dos columnas
        with cols[i % 2]:
            nombre = st.text_input(f"Jugador {i+1}", value=f"Jugador {i+1}", key=f"input_name_{i}")
            nombres_temporales.append(nombre)
    
    st.divider()
    palabra = st.text_input("Palabra Secreta", placeholder="Ej: Pizza")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 GENERAR JUEGO"):
            if palabra:
                # 1. Crear y mezclar roles
                lista_roles = [palabra] * (int(num_jugadores) - 1)
                lista_roles.append("🚨 ¡ERES EL IMPOSTOR!")
                random.shuffle(lista_roles)
                
                # 2. Guardar todo en el servidor (Global)
                datos["roles"] = lista_roles
                datos["nombres"] = nombres_temporales
                datos["activo"] = True
                datos["version"] += 1
                datos["ultima_actualizacion"] = time.time()
                st.rerun()
            else:
                st.error("Falta la palabra secreta")
    
    with c2:
        if st.button("🗑️ RESETEAR"):
            datos["activo"] = False
            st.rerun()

st.divider()

# --- VISTA DE JUGADOR ---
if datos["activo"]:
    st.subheader(f"📍 Partida en curso (Ronda #{datos['version']})")
    
    # Generar pestañas con los nombres guardados
    tabs = st.tabs(datos["nombres"])
    
    for i, tab in enumerate(tabs):
        with tab:
            st.subheader(f"Espacio de: {datos['nombres'][i]}")
            # Usamos la versión en la key para que el checkbox se resetee en cada ronda
            if st.checkbox(f"Soy {datos['nombres'][i]} (Ver rol)", key=f"v{datos['version']}_p{i}"):
                st.markdown(f"<h1 style='text-align: center; color: #FF4B4B;'>{datos['roles'][i]}</h1>", unsafe_allow_html=True)
            else:
                st.write("Haz click para revelar.")
else:
    st.info("Esperando a que el Master configure la partida...")

# Autorefresco cada 3 segundos para sincronizar móviles
time.sleep(3)
st.rerun()
