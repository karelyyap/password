# language: es

Característica: Gestor de Contraseñas Seguras
  Como usuario del sistema
  Quiero generar contraseñas fuertes y evaluar el progreso de las mías
  Para proteger mis cuentas siguiendo los mejores estándares de ciberseguridad

  # --- Pruebas para la Sección 1: Generador de Contraseñas ---

  Escenario: Generar opciones de contraseña válidas a partir de una palabra simple
    Dado que el usuario ingresa la palabra base "mariposa"
    Cuando hace clic en el botón de "Generar Opciones"
    Entonces el sistema debe devolver exactamente 3 opciones de seguridad
    Y la Opción 1 debe seguir el formato de "Frase Secreta"
    Y la Opción 2 debe aplicar sustitución de caracteres (Leetspeak)
    Y la Opción 3 debe aplicar encapsulamiento aleatorio
    Y todas las opciones generadas deben tener una longitud mínima de 12 caracteres

  Escenario: Limpieza de espacios en palabras compuestas
    Dado que el usuario ingresa la palabra base "la niña"
    Cuando el sistema valida la entrada antes de generar
    Entonces el sistema debe ignorar los espacios en blanco
    Y debe tratar la palabra como "laniña" para validar que tiene más de 3 letras
    Y debe generar las contraseñas exitosamente

  Escenario: Intentar generar contraseñas con una palabra muy corta (incluyendo espacios)
    Dado que el usuario ingresa la palabra base "y o"
    Cuando el sistema limpia los espacios en blanco
    Y valida que la longitud real es menor a 3 letras
    Entonces el sistema debe mostrar una advertencia pidiendo al menos 3 letras
    Y no se deben generar ni mostrar las opciones de contraseña

  # --- Pruebas para la Sección 2: Evaluador en Tiempo Real ---

  Escenario: Mostrar estado inicial del evaluador con campo vacío
    Dado que el usuario está en la sección del evaluador
    Y el campo de texto está vacío
    Entonces la lista de progreso debe mostrar 5 criterios
    Y todos los criterios deben aparecer como incumplidos (❌ en rojo)
    Y el bloque para copiar la contraseña debe mantenerse oculto

  Escenario: Evaluar una contraseña que cumple longitud pero carece de variedad
    Dado que el usuario ingresa la contraseña "contraseñalarga"
    Cuando el sistema evalúa la seguridad de los criterios
    Entonces el criterio "Longitud de 12 caracteres o más" debe marcarse como cumplido (✅ en verde)
    Pero el criterio "Al menos una letra mayúscula" debe mostrarse incumplido (❌)
    Y el criterio "Al menos un número" debe mostrarse incumplido (❌)
    Y el bloque de copiar contraseña debe seguir oculto

  Escenario: Evaluar una contraseña completamente segura y habilitar el copiado
    Dado que el usuario ingresa la contraseña "L@_n1ñA_2026!"
    Cuando el sistema evalúa la seguridad de todos los criterios
    Entonces todos los elementos de la lista deben marcarse como cumplidos (✅ en verde)
    Y el sistema debe mostrar un mensaje de éxito ("Tu contraseña es 100% segura")
    Y se debe habilitar y mostrar el bloque de texto con el ícono para copiar al portapapeles
