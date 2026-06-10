# language: es

Característica: Gestor de Contraseñas Seguras
  Como usuario del sistema
  Quiero generar contraseñas fuertes y evaluar las mías
  Para proteger mis cuentas siguiendo estándares de ciberseguridad

  # -- Pruebas para la Función 1: Generador --

  Escenario: Generar opciones de contraseña válidas
    Dado que el usuario tiene la palabra base "mariposa"
    Cuando el sistema genera las contraseñas
    Entonces el sistema debe devolver exactamente 3 opciones
    Y cada opción generada debe tener una longitud mínima de 12 caracteres
    Y cada opción debe incluir símbolos y números

  Escenario: Intentar generar contraseñas con una palabra muy corta
    Dado que el usuario ingresa la palabra base "yo"
    Cuando intenta generar las opciones en la interfaz
    Entonces el sistema debe mostrar una advertencia pidiendo al menos 3 letras

  # -- Pruebas para la Función 2: Evaluador --

  Escenario: Evaluar una contraseña débil y corta
    Dado que el usuario ingresa la contraseña "hola123" para evaluar
    Cuando el sistema evalúa la seguridad
    Entonces el sistema debe mostrar un error de longitud ("Debe tener 12 caracteres o más")
    Y el sistema debe mostrar un error por falta de símbolos
    Y el sistema debe mostrar un error por falta de mayúsculas

  Escenario: Evaluar una contraseña completamente segura
    Dado que el usuario ingresa la contraseña "M@r1p0s$a_2026!"
    Cuando el sistema evalúa la seguridad
    Entonces la lista de errores debe estar vacía
    Y el sistema debe mostrar un mensaje de éxito indicando que es segura
