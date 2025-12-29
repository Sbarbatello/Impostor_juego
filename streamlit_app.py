import streamlit as st
import random
import time

# Configuración de página
st.set_page_config(page_title="Impostor - Ordenado", layout="wide")

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
    
    st.write("### Nombres de los jugadores:")
    nombres_temporales = []
    
    # Eliminamos las columnas aquí para que en el móvil el orden sea 1, 2, 3...
    # Esto garantiza que el orden visual sea siempre el mismo que el de las pestañas.
    for i in range(num_jugadores):
        nombre = st.text_input(f"Nombre Jugador {i+1}", value=f"Jugador {i+1}", key=f"input_name_{i}")
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
            # El checkbox se resetea con la versión
            if st.checkbox(f"Soy {datos['nombres'][i]} (Ver rol)", key=f"v{datos['version']}_p{i}"):
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 2px solid #FF4B4B; text-align: center;">
                    <p style="color: grey; margin-bottom: 5px;">Tu palabra es:</p>
                    <h1 style="color: #FF4B4B; margin-top: 0;">{datos['roles'][i]}</h1>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.write("Haz click para revelar.")
else:
    st.info("Esperando a que el Master configure la partida...")

# Autorefresco cada 3 segundos para sincronizar móviles
time.sleep(3)
st.rerun()
