import streamlit as st
import random
import time

# Configuración de página
st.set_page_config(page_title="Impostor con Nombres", layout="wide")

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
    
    # NUEVO: Campo para nombres personalizados
    nombres_input = st.text_input("Nombres de los jugadores (separados por comas)", 
                                 placeholder="Ej: Juan, Maria, Pedro...")
    
    palabra = st.text_input("Palabra Secreta")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 GENERAR JUEGO"):
            if palabra:
                # 1. Gestionar nombres
                if nombres_input:
                    # Limpiamos espacios y creamos lista
                    lista_nombres = [n.strip() for n in nombres_input.split(",")]
                    # Si faltan nombres, rellenamos con "Jugador X"
                    while len(lista_nombres) < num_jugadores:
                        lista_nombres.append(f"Jugador {len(lista_nombres)+1}")
                else:
                    lista_nombres = [f"Jugador {i+1}" for i in range(num_jugadores)]
                
                # 2. Crear y mezclar roles
                lista_roles = [palabra] * (int(num_jugadores) - 1)
                lista_roles.append("🚨 ¡ERES EL IMPOSTOR!")
                random.shuffle(lista_roles)
                
                # 3. Guardar todo en el servidor (Global)
                datos["roles"] = lista_roles[:int(num_jugadores)] # Ajustar al número real
                datos["nombres"] = lista_nombres[:int(num_jugadores)]
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
    # Usamos los nombres personalizados para las pestañas
    tabs = st.tabs(datos["nombres"])
    
    for i, tab in enumerate(tabs):
        with tab:
            st.subheader(f"Espacio de: {datos['nombres'][i]}")
            if st.checkbox(f"Revelar mi rol", key=f"v{datos['version']}_p{i}"):
                st.markdown(f"<h1 style='text-align: center;'>{datos['roles'][i]}</h1>", unsafe_allow_html=True)
            else:
                st.write("Haz click para ver tu palabra.")
else:
    st.info("Esperando a que el Master configure la partida...")

# Autorefresco cada 3 segundos
time.sleep(3)
st.rerun()
