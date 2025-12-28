import streamlit as st
import random

st.set_page_config(page_title="Juego del Impostor", layout="centered")

# Inicializar el estado global del juego
if 'roles' not in st.session_state:
    st.session_state.roles = []
if 'activo' not in st.session_state:
    st.session_state.activo = False

st.title("🕵️ Juego del Impostor")

# --- PANEL DE CONTROL (MASTER) ---
with st.expander("⚙️ Configuración del Master", expanded=not st.session_state.activo):
    num_jugadores = st.number_input("Número de jugadores", min_value=3, max_value=20, value=5)
    palabra_secreta = st.text_input("Palabra secreta", placeholder="Ej: Sushi")
    
    if st.button("🚀 GENERAR JUEGO NUEVO"):
        if palabra_secreta:
            # Crear y mezclar roles
            lista_roles = [palabra_secreta] * (num_jugadores - 1)
            lista_roles.append("🚨 ¡ERES EL IMPOSTOR!")
            random.shuffle(lista_roles)
            
            st.session_state.roles = lista_roles
            st.session_state.activo = True
            st.success(f"¡Juego listo con {num_jugadores} pestañas!")
        else:
            st.error("Escribe una palabra primero.")

st.divider() # Esta es la forma correcta de hacer la línea en Streamlit

# --- GENERACIÓN DINÁMICA DE PESTAÑAS ---
if st.session_state.activo:
    # Creamos una lista de nombres para las pestañas
    nombres_pestanas = [f"Jugador {i+1}" for i in range(len(st.session_state.roles))]
    
    # Generamos las pestañas dinámicamente
    tabs = st.tabs(nombres_pestanas)
    
    for i, tab in enumerate(tabs):
        with tab:
            st.write("### Toca el botón para ver tu palabra")
            # Usamos un checkbox o expander para que la palabra no sea visible de inmediato
            if st.checkbox(f"Revelar rol - Pestaña {i+1}", key=f"check_{i}"):
                st.info(f"Tu palabra es:")
                st.header(st.session_state.roles[i])
            else:
                st.write("*(Oculto)*")

    if st.button("Reiniciar Partida"):
        st.session_state.activo = False
        st.rerun()
else:
    st.info("Esperando a que el Master configure la partida...")
