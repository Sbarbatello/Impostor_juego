import streamlit as st
import random
import time

# Configuración de página
st.set_page_config(page_title="Impostor Sincronizado", layout="wide")

# --- MEMORIA GLOBAL (SERVIDOR) ---
# Esto es lo que comparten todos los móviles que entren a la URL
@st.cache_resource
def obtener_servidor():
    return {"roles": [], "activo": False, "version": 0, "ultima_actualizacion": time.time()}

datos = obtener_servidor()

# --- AUTOREFRESCO ---
# Esto hace que la app se actualice sola cada 3 segundos para ver si hay cambios
st.empty() 
st.write(f"🟢 Estado: Conectado (Versión {datos['version']})")

st.title("🕵️ El Impostor")

# --- PANEL DE CONTROL (Cualquiera puede ser Master) ---
with st.expander("🎮 PANEL DE CONTROL", expanded=not datos["activo"]):
    num_jugadores = st.number_input("Nº de Jugadores", 3, 20, 5)
    palabra = st.text_input("Palabra Secreta", placeholder="Ej: Pizza")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 GENERAR JUEGO NUEVO"):
            if palabra:
                # Crear y mezclar roles
                lista = [palabra] * (int(num_jugadores) - 1)
                lista.append("🚨 ¡ERES EL IMPOSTOR!")
                random.shuffle(lista)
                
                # Guardar en el servidor para todos
                datos["roles"] = lista
                datos["activo"] = True
                datos["version"] += 1
                datos["ultima_actualizacion"] = time.time()
                st.rerun()
            else:
                st.error("Escribe una palabra")
    
    with c2:
        if st.button("🗑️ RESETEAR"):
            datos["activo"] = False
            datos["roles"] = []
            datos["version"] += 1
            st.rerun()

st.divider()

# --- VISTA DE JUGADOR ---
if datos["activo"]:
    st.subheader(f"📍 Partida en curso (Ronda #{datos['version']})")
    
    # Generar pestañas dinámicas
    titulos = [f"Jugador {i+1}" for i in range(len(datos["roles"]))]
    tabs = st.tabs(titulos)
    
    for i, tab in enumerate(tabs):
        with tab:
            # La key usa la versión para resetear los checkboxes automáticamente
            if st.checkbox(f"Soy el Jugador {i+1} (Revelar)", key=f"v{datos['version']}_p{i}"):
                st.markdown(f"<h1 style='text-align: center;'>{datos['roles'][i]}</h1>", unsafe_allow_html=True)
            else:
                st.write("Haz click para ver tu palabra secreta.")
else:
    st.info("Esperando a que alguien configure la partida...")

# Lógica de autorefresco: la app se recarga cada 3 segundos
time.sleep(3)
st.rerun()
