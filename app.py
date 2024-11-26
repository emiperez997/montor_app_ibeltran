from datetime import datetime
import time
from libs.latest_announcement import fetch_latest_announcement
from libs.db import init_db, register_email
from monitor import monitor_page
import streamlit as st
import threading
from monitor import is_monitoring

def wait_until_february():
    while datetime.now().month != 2:
        time.sleep(86400) # Wait 1 day

if __name__ == "__main__": 
    init_db()

    st.title("Monitoreo de Anuncios")

    st.write("Ingresa tu email para recibir notificaciones de nuevos anuncios en la página de Alumnos de Instituto Beltrán")

    email = st.text_input("Ingresa tu email", key="email_input")
    if st.button("Registrar email"):
        if email:
            if "@" in email and "." in email:
                try:
                    result = register_email(email)
                    if result:
                        st.success("Email registrado correctamente")
                except Exception as e:
                    st.error(f"Error al registrar email: {e}")

            else:
                st.warning("Email inválido")
        else:
            st.warning("Debes ingresar un email")

    if st.button("Obtener último anuncio"):
        latest = fetch_latest_announcement()

        if latest:
            st.write(latest) 
    
    thread = threading.Thread(target=monitor_page)
    thread.start()
    
    
    st.markdown(f"""
    <div style="display: flex; align-items: center;">
        <div style="color: {'green' if is_monitoring else 'red'}; font-size: 24px; margin-right: 10px;">
            &#9679;  <!-- Círculo -->
        </div>
        <div>
            <strong>Estado del monitoreo:</strong> {'Activo' if is_monitoring else 'Inactivo'}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
    ) 