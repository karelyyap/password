# language: es
@gestor_contrasenas @seguridad
Característica: Sistema Integral de Generación y Evaluación de Contraseñas Seguras
  Para proteger la integridad de las cuentas y prevenir ataques de fuerza bruta
  Como usuario final sin conocimientos técnicos avanzados
  Quiero una herramienta que genere contraseñas de alta entropía y evalúe mis contraseñas actuales

  Antecedentes:
    Dado que el sistema del "Gestor de Contraseñas Seguras" está iniciado
    Y la interfaz gráfica construida con Streamlit ha cargado correctamente

  # ========================================================================
  # MÓDULO 1: GENERADOR DE CONTRASEÑAS
  # ========================================================================

  @generador @validaciones_entrada
  Esquema del escenario: Bloqueo de generación por entradas inválidas o cortas
    Dado que el usuario se encuentra en la sección del Generador
    Cuando ingresa la cadena "<entrada_usuario>" en el campo de palabra base
    Y hace clic en el botón "Generar Opciones"
    Entonces el sistema debe detectar que la longitud útil es menor a 3 caracteres
    Y debe mostrar una advertencia pidiendo suficientes letras
    Y no debe generar ninguna contraseña

    Ejemplos: Entradas no válidas
      | entrada_usuario | motivo_rechazo                          |
      | a               | Un solo carácter                        |
      | yo              | Dos caracteres                          |
      |                 | Campo vacío                             |
      | "  "            | Solo espacios (se eliminan al procesar) |
      | " a "           | Solo un carácter útil tras limpieza     |

  @generador @logica_procesamiento
  Escenario: Procesamiento de una sola palabra eliminando espacios
    Dado que el usuario ingresa la palabra "   m a r i p o s a   "
    Cuando el sistema procesa la entrada para la generación
    Entonces debe eliminar todos los espacios en blanco
    Y debe utilizar un máximo de 5 caracteres ("marip") como núcleo de la contraseña

  @generador @logica_procesamiento
  Escenario: Procesamiento de múltiples palabras extrayendo fragmentos
    Dado que el usuario ingresa la frase "Mi perro azul"
    Cuando el sistema procesa la entrada para la generación
    Entonces debe separar la frase por palabras
    Y debe tomar las primeras 2 letras de cada palabra ("Mi", "pe", "az")
    Y debe unir los fragmentos limitando el núcleo a 5 caracteres ("Mipea")

  @generador @salida_exitosa @maxima_seguridad
  Escenario: Generación exitosa de tres variaciones encapsuladas
    Dado que el usuario ingresó la palabra base válida "seguridad"
    Cuando el sistema finaliza el proceso de generación
    Entonces el sistema debe renderizar exactamente 3 cuadros de código
    Y cada una de las 3 opciones debe tener una longitud exacta de 12 caracteres
    Y cada opción debe comenzar con una cadena aleatoria de letras, números y símbolos
    Y cada opción debe terminar con una cadena aleatoria garantizando la encapsulación

  # ========================================================================
  # MÓDULO 2: EVALUADOR DE CONTRASEÑAS (REACTIVO)
  # ========================================================================

  @evaluador @reactividad
  Escenario: Evaluación en tiempo real (st_keyup)
    Dado que el usuario está en la sección del Evaluador
    Cuando teclea un nuevo carácter en el campo de prueba
    Entonces el sistema no debe requerir que se presione el botón "Enter"
    Y debe actualizar los 5 criterios de seguridad instantáneamente en la pantalla

  @evaluador @limite_caracteres
  Escenario: Respeto del límite máximo de caracteres en el evaluador
    Dado que el usuario intenta pegar una contraseña extremadamente larga
    Cuando la cadena supera los 50 caracteres
    Entonces el campo de texto debe truncar la entrada al límite configurado de 50

  @evaluador @criterios_individuales
  Esquema del escenario: Validación estricta de la variedad de caracteres
    Dado que el usuario ingresa la contraseña "<contrasena_prueba>"
    Cuando el evaluador procesa la cadena
    Entonces el indicador de mayúscula debe ser "<req_mayus>"
    Y el indicador de minúscula debe ser "<req_minus>"
    Y el indicador de número debe ser "<req_num>"
    Y el indicador de símbolo especial debe ser "<req_simbolo>"

    Ejemplos: Pruebas de variedad atómica
      | contrasena_prueba | req_mayus | req_minus | req_num | req_simbolo |
      | sololetras        | Falso     | Verdadero | Falso   | Falso       |
      | MAYUSCULAS        | Verdadero | Falso     | Falso   | Falso       |
      | 1234567890        | Falso     | Falso     | Verdadero| Falso      |
      | !@#$%&*()_+       | Falso     | Falso     | Falso   | Verdadero   |
      | Letras123         | Verdadero | Verdadero | Verdadero| Falso      |

  @evaluador @casos_limite_longitud
  Esquema del escenario: Pruebas de frontera para la longitud de la contraseña
    Dado que la contraseña ingresada tiene exactamente "<longitud>" caracteres
    Cuando se evalúa el criterio de longitud
    Entonces el sistema debe marcar el criterio de longitud como "<resultado>"

    Ejemplos: Valores de frontera (Boundary Value Analysis)
      | longitud | resultado |
      | 0        | Falso     |
      | 11       | Falso     |
      | 12       | Verdadero |
      | 13       | Verdadero |
      | 50       | Verdadero |

  @evaluador @flujo_completo
  Escenario: Aprobación total de una contraseña 100% segura
    Dado que el usuario tecleó la contraseña "K@r3ly_2026!"
    Cuando todos los 5 criterios de seguridad cambian a estado "Verdadero"
    Entonces el sistema debe mostrar un mensaje de éxito ("¡Excelente!")
    Y debe disparar la animación de globos (balloons) en la interfaz
    Y debe mostrar un bloque de código para que el usuario pueda copiar su contraseña validada
