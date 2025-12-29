import streamlit as st
import random

st.set_page_config(page_title="Impostor Multi-Dispositivo", layout="wide")

# --- FUNCIÓN PARA COMPARTIR DATOS ENTRE TODOS ---
# Esto hace que los datos vivan en el servidor, no en el móvil de cada uno
@st.cache_resource
def get_global_game_data():
    return {
        "roles": [],
        "activo": False,
        "id_partida": 0
    }

game_data = get_global_game_data()

st.title("🕵️ Impostor Multi-Jugador")

# --- PANEL DEL MASTER ---
with st.sidebar:
    st.header("⚙️ Configuración")
    password = st.text_input("Contraseña Master", type="password")
    
    if password == "admin":
        num_jugadores = st.number_input("Jugadores", min_value=3, max_value=20, value=5)
        palabra = st.text_input("Palabra secreta")
        
        if st.button("🚀 LANZAR JUEGO PARA TODOS"):
            # Generar roles
            roles = [palabra] * (int(num_jugadores) - 1)
            roles.append("🚨 ¡ERES EL IMPOSTOR!")
            random.shuffle(roles)
            
            # Actualizar el diccionario GLOBAL
            game_data["roles"] = roles
            game_data["activo"] = True
            game_data["id_partida"] += 1 # Forzamos refresco
            st.success("¡Juego enviado a todos los móviles!")
            st.rerun()
            
        if st.button("🗑️ Resetear"):
            game_data["activo"] = False
            game_data["roles"] = []
            st.rerun()

# --- VISTA DEL JUGADOR ---
if game_data["activo"]:
    st.info(f"Partida en curso. Por favor, selecciona tu número de jugador.")
    
    # IMPORTANTE: En móviles, las pestañas (tabs) pueden ser difíciles de navegar 
    # si hay muchas. Usamos un selector mejorado.
    titulos = [f"Jugador {i+1}" for i in range(len(game_data["roles"]))]
    tabs = st.tabs(titulos)
    
    for i, tab in enumerate(tabs):
        with tab:
            st.write(f"### Pestaña {i+1}")
            # El checkbox asegura que no vean la palabra de otros por error al navegar
            if st.checkbox("Revelar mi rol", key=f"global_tab_{i}_{game_data['id_partida']}"):
                st.divider()
                st.markdown(f"<h1 style='text-align: center;'>{game_data['roles'][i]}</h1>", unsafe_allow_html=True)
                st.divider()
else:
    st.warning("Esperando a que el Master inicie la partida...")
    if st.button("🔄 Comprobar si ya empezó"):
        st.rerun()

st.caption("Nota: Si el Master ya inició el juego y no ves nada, pulsa el botón 'Comprobar'.")
