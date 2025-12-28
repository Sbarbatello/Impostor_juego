import streamlit as st
import random

# Configuración inicial de la página
st.set_page_config(page_title="Juego del Impostor", layout="centered")

# Inicializar el estado del juego si no existe
if 'game_data' not in st.session_state:
    st.session_state.game_data = {
        'roles': {},
        'palabra': "",
        'jugadores': 0,
        'activo': False
    }

st.title("🕵️ El Impostor")

# --- PANEL DE CONTROL (MASTER) ---
with st.expander("⚙️ Panel del Master", expanded=not st.session_state.game_data['activo']):
    num_jugadores = st.number_input("Número de jugadores", min_value=3, max_value=20, value=5)
    palabra_secreta = st.text_input("Palabra secreta", placeholder="Ej: Manzana")
    
    if st.button("🚀 GENERAR JUEGO NUEVO"):
        if palabra_secreta:
            # Crear lista de roles
            roles = [palabra_secreta] * int(num_jugadores)
            impostor_idx = random.randint(0, num_jugadores - 1)
            roles[impostor_idx] = "🚨 ¡ERES EL IMPOSTOR!"
            
            # Guardar en el estado de la sesión
            st.session_state.game_data = {
                'roles': {f"Jugador {i+1}": roles[i] for i in range(num_jugadores)},
                'palabra': palabra_secreta,
                'jugadores': num_jugadores,
                'activo': True
            }
            st.success("¡Juego generado! Dile a cada uno que elija su número.")
        else:
            st.error("Por favor, introduce una palabra secreta.")

---

# --- VISTA DE JUGADOR ---
if st.session_state.game_data['activo']:
    st.subheader("📱 Sección de Jugador")
    opciones = ["Selecciona quién eres..."] + list(st.session_state.game_data['roles'].keys())
    user_choice = st.selectbox("¿Qué número de jugador eres?", opciones)

    if user_choice != "Selecciona quién eres...":
        st.info("Tu palabra secreta es:")
        # El uso de markdown grande para que se vea bien en el móvil
        st.markdown(f"<h1 style='text-align: center;'>{st.session_state.game_data['roles'][user_choice]}</h1>", unsafe_allow_html=True)
        
        st.warning("⚠️ No dejes que nadie vea tu pantalla. Refresca o cambia de jugador para ocultar.")
else:
    st.info("Esperando a que el Master inicie el juego...")

# Botón para resetear todo
if st.sidebar.button("Limpiar todo"):
    st.session_state.game_data = {'roles': {}, 'palabra': "", 'jugadores': 0, 'activo': False}
    st.rerun()
