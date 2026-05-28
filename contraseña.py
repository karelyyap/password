import streamlit as st
import string
import secrets

# --- FUNCIONES DE LÓGICA ---

def generar_contrasenas(palabra_base):
    simbolos = "!@#$%&*+?"
    numeros = string.digits
    letras = string.ascii_letters
    opciones = []

    # Opción 1: Estilo "Frase Secreta" (Palabra base + Palabra extra + Números + Símbolo)
    palabras_random = ["Zorro", "Luna", "Nova", "Roca", "Cima", "Eco"]
    op1 = f"{palabra_base.capitalize()}{secrets.choice(palabras_random)}{secrets.choice(numeros)}{secrets.choice(numeros)}{secrets.choice(simbolos)}"
    # Asegurar longitud mínima de 12
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

    # Opción 3: Base encapsulada en caracteres aleatorios (Máxima seguridad)
    relleno_izq = "".join(secrets.choice(letras + numeros + simbolos) for _ in range(4))
    relleno_der = "".join(secrets.choice(letras + numeros + simbolos) for _ in range(4))
    op3 = f"{relleno_izq}{palabra_base}{relleno_der}"
    while len(op3) < 12:
        op3 += secrets.choice(simbolos)
    opciones.append(op3)

    return opciones

def evaluar_contrasena(pwd):
    errores = []
    if len(pwd) < 12:
        errores.append("❌ Longitud: Debe tener 12 caracteres o más.")
    if not any(c.isupper() for c in pwd) or not any(c.islower() for c in pwd):
        errores.append("❌ Variedad: Faltan letras mayúsculas o minúsculas.")
    if not any(c.isdigit() for c in pwd):
        errores.append("❌ Variedad: Faltan números.")
    
    simbolos_validos = set(string.punctuation)
    if not any(c in simbolos_validos for c in pwd):
        errores.append("❌ Variedad: Faltan símbolos (ej. @, #, $, !).")
        
    return errores

# --- INTERFAZ GRÁFICA (STREAMLIT) ---

st.set_page_config(page_title="Gestor de Contraseñas Seguras", page_icon="🔐")

st.title("🔐 Gestor de Contraseñas Seguras")
st.write("Genera contraseñas fuertes o evalúa las tuyas siguiendo los mejores estándares de ciberseguridad.")

st.divider()

# SECCIÓN 1: Generador
st.header("1. Generador de Contraseñas")
st.write("Ingresa una palabra fácil de recordar y generaremos 3 opciones seguras para ti.")

palabra_input = st.text_input("Ingresa tu palabra base:", placeholder="Ej. mariposa")

if st.button("Generar Opciones", type="primary"):
    if palabra_input:
        if len(palabra_input) < 3:
            st.warning("Por favor, ingresa una palabra de al menos 3 letras para mayor seguridad.")
        else:
            opciones = generar_contrasenas(palabra_input)
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
st.write("Prueba tu contraseña aquí. Verificaremos si cumple con los criterios recomendados.")

pwd_prueba = st.text_input("Ingresa la contraseña a probar:", type="password")

if st.button("Evaluar Seguridad"):
    if pwd_prueba:
        errores = evaluar_contrasena(pwd_prueba)
        if not errores:
            st.success("✅ ¡Excelente! Tu contraseña es segura, larga y tiene la variedad adecuada.")
            st.balloons()
        else:
            st.error("Tu contraseña necesita mejoras:")
            for error in errores:
                st.write(error)
            st.info("💡 Consejo: Evita usar información personal (fechas de nacimiento, nombres de mascotas) aunque cumplas con la longitud.")
    else:
        st.warning("Ingresa una contraseña para evaluar.")