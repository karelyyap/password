import streamlit as st
import string
import secrets
from st_keyup import st_keyup

# --- FUNCIONES DE LÓGICA ---

def generar_contrasenas(palabra_base):
    # NUEVA LÓGICA: Tomar un poquito de cada palabra
    palabras = palabra_base.split() # Separa la frase por espacios
    
    if len(palabras) > 1:
        # Si hay varias palabras, toma las primeras 2 letras de cada una y las une
        palabra_base = "".join(p[:2] for p in palabras)[:5]
    else:
        # Si es solo una palabra, le quita espacios y toma las primeras 5 letras
        palabra_base = palabra_base.replace(" ", "")[:5] 
    
    simbolos = "!@#$%&*+?"
    numeros = string.digits
    letras = string.ascii_letters
    opciones = []

    # Opción 1: Frase Secreta
    palabras_random = ["Zorro", "Luna", "Nova", "Roca", "Cima", "Eco"]
    op1 = f"{palabra_base.capitalize()}{secrets.choice(palabras_random)}{secrets.choice(numeros)}{secrets.choice(simbolos)}"
    while len(op1) < 12:
        op1 += secrets.choice(simbolos + numeros)
    opciones.append(op1[:12])

    # Opción 2: Sustitución (Leetspeak)
    leet = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
    op2_base = "".join(leet.get(c.lower(), c) for c in palabra_base)
    op2 = f"{op2_base.capitalize()}{secrets.choice(simbolos)}{secrets.choice(numeros)}"
    while len(op2) < 12:
        op2 += secrets.choice(letras + numeros)
    opciones.append(op2[:12])

    # Opción 3: Base encapsulada
    relleno_izq = "".join(secrets.choice(letras + numeros + simbolos) for _ in range(3))
    op3 = f"{relleno_izq}{palabra_base}{secrets.choice(simbolos)}{secrets.choice(numeros)}"
    while len(op3) < 12:
        op3 += secrets.choice(letras + numeros + simbolos)
    opciones.append(op3[:12])

    return opciones

def evaluar_criterios(pwd):
    simbolos_validos = set(string.punctuation)
    
    # Si el campo está vacío, devolvemos todo en falso
    if not pwd:
        return {
            "Longitud exacta de 12 caracteres": False,
            "Al menos una letra mayúscula": False,
            "Al menos una letra minúscula": False,
            "Al menos un número": False,
            "Al menos un símbolo (ej. @, #, $, !)": False
        }
        
    return {
        "Longitud exacta de 12 caracteres": len(pwd) == 12,
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
    # Limpiamos los espacios solo para contar que haya al menos 3 letras útiles
    palabra_limpia = palabra_input.replace(" ", "")
    
    if palabra_limpia:
        if len(palabra_limpia) < 3:
            st.warning("Por favor, ingresa suficientes letras para generar algo seguro.")
        else:
            opciones = generar_contrasenas(palabra_input)
            st.success("¡Opciones generadas con éxito! Todas tienen exactamente 12 caracteres.")
            
            st.code(opciones[0], language="text")
            st.caption("Opción 1: Estilo 'Frase Secreta'. Fácil de memorizar.")
            
            st.code(opciones[1], language="text")
            st.caption("Opción 2: Sustitución de caracteres. Difícil de adivinar.")
            
            st.code(opciones[2], language="text")
            st.caption("Opción 3: Aleatoria. Máxima seguridad para gestores de contraseñas.")
    else:
        st.error("Debes ingresar una palabra o frase base primero.")

st.divider()

# SECCIÓN 2: Evaluador
st.header("2. Evaluador de Contraseñas (En vivo)")
st.write("Escribe tu contraseña y la evaluación se actualizará mientras tecleas.")

# SOLUCIÓN: Agregamos key="eval" y garantizamos que si devuelve None, se convierta en ""
pwd_prueba = st_keyup("Ingresa la contraseña a probar:", max_chars=50, key="eval") or ""

criterios = evaluar_criterios(pwd_prueba)

st.markdown("### Progreso de seguridad:")
for criterio, cumplido in criterios.items():
    icono = "✅" if cumplido else "❌"
    color = "green" if cumplido else "red"
    st.markdown(f":{color}[{icono} {criterio}]")

if pwd_prueba:
    if all(criterios.values()):
        st.success("¡Excelente! Tu contraseña es 100% segura y cumple con los 12 caracteres.")
        st.balloons()
        
        st.markdown("**Copia tu nueva contraseña aquí (ícono a la derecha):**")
        st.code(pwd_prueba, language="text")
    else:
        st.info("💡 Sigue escribiendo hasta que todos los requisitos estén en verde.")
