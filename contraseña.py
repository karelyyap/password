import streamlit as st
import string
import secrets

# --- FUNCIONES DE LÓGICA ---

def generar_contrasenas(palabra_base):
    # Eliminar espacios en blanco de la palabra base
    palabra_base = palabra_base.replace(" ", "")
    
    simbolos = "!@#$%&*+?"
    numeros = string.digits
    letras = string.ascii_letters
    opciones = []

    # Opción 1: Estilo "Frase Secreta"
    palabras_random = ["Zorro", "Luna", "Nova", "Roca", "Cima", "Eco"]
    op1 = f"{palabra_base.capitalize()}{secrets.choice(palabras_random)}{secrets.choice(numeros)}{secrets.choice(numeros)}{secrets.choice(simbolos)}"
    while len(op1) < 12:
        op1 += secrets.choice(simbolos + numeros)
    opciones.append(op1)

    # Opción 2: Sustitución (Leetspeak) + Alta Entropía
    leet = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
    op2_base = "".join(leet.get(c.lower(), c) for c in palabra_base)
    op2 = f"{op2_base.capitalize()}{secrets.choice(simbolos)}{secrets.choice(simbolos)}"
    while len(op2) < 12:
        op2 += secrets.choice(letras + numeros)
    opciones.append(op2)

    # Opción 3: Base encapsulada en caracteres aleatorios
    relleno_izq = "".join(secrets.choice(letras + numeros + simbolos) for _ in range(4))
    relleno_der = "".join(secrets.choice(letras + numeros + simbolos) for _ in range(4))
    op3 = f"{relleno_izq}{palabra_base}{relleno_der}"
    while len(op3) < 12:
        op3 += secrets.choice(simbolos)
    opciones.append(op3)

    return opciones

def evaluar_criterios(pwd):
    """Devuelve un diccionario con cada criterio y un booleano indicando si se cumple."""
    simbolos_validos = set(string.punctuation)
    return {
        "Longitud de 12 caracteres o más": len(pwd) >= 12,
        "Al menos una letra mayúscula": any(c.isupper() for c in pwd),
        "Al menos una letra minúscula": any(c.islower() for c in pwd),
        "Al menos un número": any(c.isdigit() for c in pwd),
        "Al menos un símbolo (ej. @, #, $, !)": any(c in simbolos_validos for c in pwd)
    }

# --- INTERFAZ GRÁFICA (STREAMLIT) ---

st.set_page_config(page_title="Gestor de Contraseñas Seguras", page_icon="🔐")

st.title("🔐 Gestor de Contraseñas Seguras")
st.write("Genera contraseñas fuertes o evalúa las tuyas siguiendo los mejores estándares de ciberseguridad.")

st.divider()

# SECCIÓN 1: Generador
st.header("1. Generador de Contraseñas")
st.write("Ingresa una palabra fácil de recordar y generaremos 3 opciones seguras para ti.")

palabra_input = st.text_input("Ingresa tu palabra base:", placeholder="Ej. la niña")

if st.button("Generar Opciones", type="primary"):
    palabra_limpia = palabra_input.replace(" ", "")
    
    if palabra_limpia:
        if len(palabra_limpia) < 3:
            st.warning("Por favor, ingresa una palabra de al menos 3 letras (sin contar espacios).")
        else:
            opciones = generar_contrasenas(palabra_limpia)
            st.success("¡Opciones generadas con éxito!")
            
            st.code(opciones[0], language="text")
            st.caption("Opción 1: Estilo 'Frase Secreta'. Fácil de memorizar.")
            
            st.code(opciones[1], language="text")
            st.caption("Opción 2: Sustitución de caracteres. Difícil de adivinar.")
            
            st.code(opciones[2], language="text")
            st.caption("Opción 3: Aleatoria. Máxima seguridad para gestores de contraseñas.")
    else:
        st.error("Debes ingresar una palabra base primero.")

st.divider()

# SECCIÓN 2: Evaluador
st.header("2. Evaluador de Contraseñas")
st.write("Escribe tu contraseña y presiona **Enter** para ver el progreso de los criterios.")

pwd_prueba = st.text_input("Ingresa la contraseña a probar:", type="password")

# Evaluar siempre el texto actual en el input
criterios = evaluar_criterios(pwd_prueba)

# Mostrar la lista de verificación (Checklist)
st.markdown("### Progreso de seguridad:")
for criterio, cumplido in criterios.items():
    icono = "✅" if cumplido else "❌"
    color = "green" if cumplido else "red"
    st.markdown(f":{color}[{icono} {criterio}]")

# Si se ingresó texto y todos los criterios son True
if pwd_prueba:
    if all(criterios.values()):
        st.success("¡Excelente! Tu contraseña es segura, larga y tiene la variedad adecuada.")
        st.balloons()
    else:
        st.info("💡 Consejo: Evita usar información personal (fechas de nacimiento, nombres de mascotas) aunque cumplas con todos los requisitos visuales.")
