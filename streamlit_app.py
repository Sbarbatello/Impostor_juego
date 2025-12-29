import streamlit as st
import random
import time
import math

st.set_page_config(page_title="Impostor - Control de Rachas", layout="wide")

# --- MEMORIA GLOBAL (SERVIDOR) ---
@st.cache_resource
def obtener_servidor():
    return {
        "roles": [], 
        "nombres": [],
        "activo": False, 
        "version": 0,
        "rondas_desde_multi": 7  # Inicializamos en 7 para que pueda salir en la primera
    }

datos = obtener_servidor()

st.title("🕵️ El Impostor")
st.write(f"🟢 Ronda: {datos['version']} | Rondas de enfriamiento: {datos['rondas_desde_multi']}/7")

# --- PANEL DE CONTROL ---
with st.expander("⚙️ CONFIGURACIÓN DEL MASTER", expanded=not datos['activo']):
    
    with st.expander("👥 JUGADORES", expanded=False):
        num_jugadores = st.number_input("Nº de Jugadores", 3, 20, 5)
        multi_impostor_toggle = st.toggle("Permitir múltiples impostores", value=False)
        
        st.divider()
        nombres_temporales = []
        for i in range(num_jugadores):
            n = st.text_input(f"Nombre Jugador {i+1}", value=f"Jugador {i+1}", key=f"input_{i}")
            nombres_temporales.append(n)
        
        if st.button("🆕 GENERAR PARTIDA NUEVA"):
            datos["activo"] = False
            datos["roles"] = []
            datos["nombres"] = nombres_temporales
            datos["version"] = 0
            datos["rondas_desde_multi"] = 7 # Reset de enfriamiento
            st.rerun()

    st.divider()
    palabra = st.text_input("Palabra Secreta")
    
    if st.button("🚀 SIGUIENTE RONDA"):
        if palabra and datos["nombres"]:
            n = len(datos["nombres"])
            probabilidad = random.random()
            
            # --- LÓGICA DE PROBABILIDAD + CONTADOR DE ENFRIAMIENTO ---
            num_impostores = 1 # Por defecto
            
            # Solo intentamos múltiples si el toggle está ON y el azar da < 0.10
            if multi_impostor_toggle and probabilidad <= 0.10:
                # RESTRICCIÓN EXTRA: ¿Han pasado ya 7 rondas?
                if datos["rondas_desde_multi"] >= 7:
                    max_posible = math.floor(n * 0.25)
                    if max_posible >= 2:
                        num_impostores = random.randint(2, max_posible)
                        datos["rondas_desde_multi"] = 0 # Reiniciamos contador de enfriamiento
                else:
                    # El azar dijo SÍ, pero el enfriador dice NO
                    num_impostores = 1
            
            # Si no ha salido multi-impostor en esta ronda, sumamos 1 al contador
            if num_impostores == 1:
                datos["rondas_desde_multi"] += 1
            
            # Crear y mezclar
            lista_roles = [palabra] * (n - num_impostores)
            for _ in range(num_impostores):
                lista_roles.append("🚨 ¡ERES EL IMPOSTOR!")
            random.shuffle(lista_roles)
            
            datos["roles"] = lista_roles
            datos["activo"] = True
            datos["version"] += 1
            st.success(f"Ronda {datos['version']} lista. (Impostores: {num_impostores})")
            st.rerun()

st.divider()

# --- VISTA JUGADOR ---
if datos["activo"]:
    tabs = st.tabs(datos["nombres"])
    for i, tab in enumerate(tabs):
        with tab:
            if st.button(f"👁️ Ver mi palabra", key=f"btn_v{datos['version']}_j{i}"):
                placeholder = st.empty()
                placeholder.markdown(f"""
                <div style="background-color: #262730; padding: 30px; border-radius: 15px; border: 3px solid #FF4B4B; text-align: center;">
                    <h1 style="color: white; font-size: 50px;">{datos['roles'][i]}</h1>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(5)
                placeholder.empty()
else:
    st.info("Configura y dale a Siguiente Ronda.")

time.sleep(3)
st.rerun()
