import streamlit as st
import random

# Configuración de página para móviles y escritorio
st.set_page_config(page_title="Impostor Game", layout="wide")

# Inicialización segura del estado del juego
if 'roles' not in st.session_state:
    st.session_state.roles = []
if 'activo' not in st.session_state:
    st.session_state.activo = False

st.title("🕵️ Juego del Impostor")

# --- ZONA DEL MASTER ---
with st.sidebar:
    st.header("⚙️ Panel de Control")
    password = st.text_input("Contraseña Master (para ocultar ajustes)", type="password")
    
    # Solo mostramos los controles si la contraseña es correcta (ej: '1234' o la que quieras)
    # Si no quieres contraseña, puedes quitar este 'if'
    if password == "admin": 
        num_jugadores = st.number_input("Número de jugadores", min_value=3, max_value=20, value=5)
        palabra_secreta = st.text_input("Palabra para el grupo")
        
        if st.button("🚀 INICIAR / REINICIAR JUEGO"):
            if palabra_secreta:
                # 1. Crear la lista de roles
                total = int(num_jugadores)
                roles = [palabra_secreta] * (total - 1)
                roles.append("🚨 ¡ERES EL IMPOSTOR!")
                
                # 2. Mezclar aleatoriamente
                random.shuffle(roles)
                
                # 3. Guardar en sesión
                st.session_state.roles = roles
                st.session_state.activo = True
                st.success("Juego generado con éxito")
                st.rerun()
            else:
                st.error("Introduce una palabra")
    else:
        st.warning("Introduce la contraseña 'admin' para configurar.")

# --- ZONA DE JUEGO (DASHBOARD) ---
if st.session_state.activo:
    st.info("¡La partida está en curso! Que cada jugador busque su pestaña.")
    
    # Generación dinámica de pestañas según el número de roles creados
    titulos_tabs = [f"Jugador {i+1}" for i in range(len(st.session_state.roles))]
    tabs = st.tabs(titulos_tabs)

    for i, tab in enumerate(tabs):
        with tab:
            st.subheader(f"Espacio del Jugador {i+1}")
            st.write("Asegúrate de que nadie esté mirando tu pantalla.")
            
            # Checkbox para ocultar/mostrar la palabra y que no se filtre al cambiar de pestaña
            revelar = st.checkbox("Revelar mi palabra secreta", key=f"tab_{i}")
            
            if revelar:
                st.divider()
                # Mostramos la palabra con un estilo llamativo
                st.markdown(f"### Tu palabra es:\n# {st.session_state.roles[i]}")
                st.divider()
            else:
                st.write("---")
                st.write("Haz click en el checkbox para ver tu rol.")

else:
    st.info("Esperando a que el Master configure la partida en la barra lateral.")

# Pie de página simple
st.markdown("<br><br><small>Refresca la página si necesitas reiniciar la vista.</small>", unsafe_allow_html=True)
