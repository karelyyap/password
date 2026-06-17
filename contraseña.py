import streamlit as st
import string
import secrets
from st_keyup import st_keyup

# --- FUNCIONES DE LÓGICA ---

def generar_contrasenas(palabra_base):
    # Separamos por espacios para identificar si hay múltiples palabras
    palabras = palabra_base.split() 
    
    if len(palabras) > 1:
        # Si hay varias, toma las primeras 2 letras de cada una y las une
        palabra_base = "".join(p[:2] for p in palabras)[:5]
    else:
        # Si es una sola palabra, nos aseguramos de quitar los espacios
        palabra_base = palabra_base.replace(" ", "")[:5] 
    
    simbolos = "!@#$%&*+?"
    numeros = string.digits
    letras = string.ascii_letters
    opciones = []

    # Generamos 3 contraseñas distintas usando la lógica encapsulada
    for _ in range(3):
        relleno_izq = "".join(secrets.choice(letras + numeros + simbolos) for _ in range(3))
        pwd = f"{relleno_izq}{palabra_base}{secrets.choice(simbolos)}{secrets.choice(numeros)}"
        
        while len(pwd) < 12:
            pwd += secrets.choice(letras + numeros + simbolos)
            
        opciones.append(pwd[:12])

    return opciones

def evaluar_criterios(pwd):
    simbolos_validos = set(string.punctuation)
    
    if not pwd:
        return {
            "Longitud de 12 caracteres o más": False,
            "Al menos una letra mayúscula": False,
            "Al menos una letra minúscula": False,
            "Al menos un número": False,
            "Al menos un símbolo (ej. @, #, $, !)": False
        }
        
    return {
        "Longitud de 12 caracteres o más": len(pwd) >= 12,
        "Al menos una letra mayúscula": any(c.isupper() for c in pwd),
        "Al menos una letra minúscula": any(c.islower() for c in pwd),
        "Al menos un número": any(c.isdigit() for c in pwd),
        "Al menos un símbolo (ej. @, #, $, !)": any(c in simbolos_validos for c in pwd)
    }

# --- INTERFAZ GRÁFICA (STREAMLIT) ---

st.set_page_config(page_title="Gestor de Contraseñas - Karely Aragón", page_icon="🔐")

st.title("🔐 Gestor de Contraseñas Seguras")
st.markdown("### Desarrollado por: Karely Aragón")
st.write("Genera contraseñas fuertes o evalúa las tuyas siguiendo los mejores estándares de ciberseguridad.")

st.divider()

# SECCIÓN 1: Generador
st.header("1. Generador de Contraseñas")
palabra_input = st.text_input("Ingresa tu palabra o frase base (Máximo 50 caracteres):", max_chars=50)

if st.button("Generar Opciones", type="primary"):
    # Validamos usando la entrada sin espacios
    palabra_limpia = palabra_input.replace(" ", "")
    
    if palabra_limpia:
        if len(palabra_limpia) < 3:
            st.warning("Por favor, ingresa suficientes letras para generar algo seguro.")
        else:
            opciones = generar_contrasenas(palabra_input)
            st.success("¡Opciones generadas con éxito! Todas utilizan seguridad encapsulada de 12 caracteres.")
            
            st.code(opciones[0], language="text")
            st.caption("Variación 1 (Base encapsulada de máxima seguridad)")
            
            st.code(opciones[1], language="text")
            st.caption("Variación 2 (Base encapsulada de máxima seguridad)")
            
            st.code(opciones[2], language="text")
            st.caption("Variación 3 (Base encapsulada de máxima seguridad)")
    else:
        st.error("Debes ingresar una palabra o frase base primero.")

st.divider()

# SECCIÓN 2: Evaluador
st.header("2. Evaluador de Contraseñas (En vivo)")
st.write("Escribe tu contraseña y la evaluación se actualizará mientras tecleas.")

# SOLUCIÓN AL BUG: Declarar explícitamente label y value para que no se pierdan en el rerun
pwd_prueba = st_keyup(
    label="Ingresa la contraseña a probar:", 
    value="", 
    max_chars=50, 
    key="eval_input"
) or ""

criterios = evaluar_criterios(pwd_prueba)

st.markdown("### Progreso de seguridad:")
for criterio, cumplido in criterios.items():
    icono = "✅" if cumplido else "❌"
    color = "green" if cumplido else "red"
    st.markdown(f":{color}[{icono} {criterio}]")

if pwd_prueba:
    if all(criterios.values()):
        st.success("¡Excelente! Tu contraseña es 100% segura y cumple con los requisitos de longitud.")
        st.balloons()
        
        st.markdown("**Copia tu nueva contraseña aquí (ícono a la derecha):**")
        st.code(pwd_prueba, language="text")
    else:
        st.info("💡 Sigue escribiendo hasta que todos los requisitos estén en verde.")
