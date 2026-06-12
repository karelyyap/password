import streamlit as st
import string
import secrets
from st_keyup import st_keyup

# --- FUNCIONES DE LÓGICA ---

def generar_contrasenas(palabra_base):
    palabra_base = palabra_base.replace(" ", "")
    simbolos = "!@#$%&*+?"
    numeros = string.digits
    letras = string.ascii_letters
    opciones = []

    # Opción 1: Frase Secreta
    palabras_random = ["Zorro", "Luna", "Nova", "Roca", "Cima", "Eco"]
    op1 = f"{palabra_base.capitalize()}{secrets.choice(palabras_random)}{secrets.choice(numeros)}{secrets.choice(numeros)}{secrets.choice(simbolos)}"
    while len(op1) < 12:
        op1 += secrets.choice(simbolos + numeros)
    opciones.append(op1)

    # Opción 2: Sustitución (Leetspeak)
    leet = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
    op2_base = "".join(leet.get(c.lower(), c) for c in palabra_base)
    op2 = f"{op2_base.capitalize()}{secrets.choice(simbolos)}{secrets.choice(simbolos)}"
    while len(op2) < 12:
        op2 += secrets.choice(letras + numeros)
    opciones.append(op2)

    # Opción 3: Base encapsulada
    relleno_izq = "".join(secrets.choice(letras + numeros + simbolos) for _ in range(4))
    relleno_der = "".join(secrets.choice(letras + numeros + simbolos) for _ in range(4))
    op3 = f"{relleno_izq}{palabra_base}{relleno_der}"
    while len(op3) < 12:
        op3 += secrets.choice(simbolos)
    opciones.append(op3)

    return opciones

def evaluar_criterios(pwd):
    simbolos_validos = set(string.punctuation)
    
    # Si el campo está vacío, devolvemos todo en falso para no evaluar nada aún
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

st.set_page_config(page_title="Gestor de Contraseñas Seguras", page_icon="🔐")

st.title("🔐 Gestor de Contraseñas Seguras")
st.write("Genera contraseñas fuertes o evalúa las tuyas siguiendo los mejores estándares de ciberseguridad.")

st.divider()

# SECCIÓN 1: Generador
st.header("1. Generador de Contraseñas")
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
st.write("Escribe tu contraseña. Los criterios se actualizarán al instante.")

# Usamos st_keyup para que se actualice tecla por tecla. 
# Nota: Si omites type="password", la contraseña será visible mientras se escribe.
pwd_prueba = st_keyup("Ingresa la contraseña a probar:", type="password", key="evaluador")

# Evaluar en tiempo real
criterios = evaluar_criterios(pwd_prueba)

st.markdown("### Progreso de seguridad:")
for criterio, cumplido in criterios.items():
    icono = "✅" if cumplido else "❌"
    color = "green" if cumplido else "red"
    st.markdown(f":{color}[{icono} {criterio}]")

# Lógica condicional: Mostrar el bloque de copiar SÓLO cuando todo es correcto
if pwd_prueba:
    if all(criterios.values()):
        st.success("¡Excelente! Tu contraseña es 100% segura.")
        st.balloons()
        
        st.markdown("**Copia tu nueva contraseña aquí (ícono a la derecha):**")
        st.code(pwd_prueba, language="text")
    else:
        st.info("💡 Sigue escribiendo hasta que todos los criterios estén en verde.")
