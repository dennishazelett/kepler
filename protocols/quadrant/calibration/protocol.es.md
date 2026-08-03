# Protocolo de Calibración del Cuadrante

**ID del Protocolo:** `quadrant-calibration`
**Versión del Protocolo:** `0.1.0`
**Estado:** Borrador

---

# Propósito

Este protocolo describe un procedimiento estandarizado para caracterizar el desempeño del sistema de medición observador–instrumento de un cuadrante bajo condiciones controladas.

El observador mide la geometría del objetivo de calibración y registra las lecturas del cuadrante. Posteriormente, durante el análisis, los ángulos de referencia se infieren a partir de la altura del objetivo, la distancia horizontal del observador y la altura del objetivo con respecto al nivel de los ojos. Estos ángulos inferidos se comparan con las lecturas registradas por el cuadrante.

La calibración documenta el desempeño de las mediciones; no modifica ni corrige observaciones posteriores.

---

# Alcance

Este protocolo se aplica a encuestas de calibración realizadas utilizando el cuadrante Kepler.

Está destinado a la caracterización inicial del instrumento, la verificación posterior a reparaciones, ejercicios educativos y evaluaciones periódicas del desempeño.

Este protocolo no está destinado a observaciones astronómicas de campo.

---

# Pregunta Científica

> ¿Cómo se comparan las lecturas obtenidas por este sistema observador–instrumento con los ángulos inferidos a partir de una geometría de calibración medida de manera independiente?

---

# Equipo Requerido

* Cuadrante Kepler
* Cinco objetivos de calibración separados por intervalos de 1 pie (o 0.3 m), comenzando al nivel de los ojos
* Instrumento de medición adecuado para determinar la distancia horizontal del observador
* Instrumento de medición adecuado para determinar las alturas del objetivo y del nivel de los ojos
* Material para registrar observaciones o un dispositivo electrónico de captura de datos
* Especificación de observación aplicable para la calibración del cuadrante

---

# Requisitos Previos

Antes de comenzar la encuesta de calibración:

* el cuadrante debe estar completamente construido y ser mecánicamente funcional;
* la plomada debe oscilar libremente, sin obstrucciones;
* el observador debe estar familiarizado con el funcionamiento normal del cuadrante;
* la posición del observador y del objetivo de calibración deben permanecer fijas mientras se recopilan las observaciones correspondientes a esa geometría; y
* las distancias y alturas requeridas deben poder medirse independientemente del cuadrante.

---

# Procedimiento de Observación

Para cada punto de referencia marcado en el objetivo de calibración:

1. Establezca la posición del observador y el objetivo de calibración.
2. Mida y registre la geometría de calibración según lo requerido por la especificación de observación correspondiente.
3. Apunte al punto de referencia marcado utilizando el cuadrante.
4. Permita que la plomada se estabilice.
5. Registre la lectura del cuadrante exactamente como se observa.
6. Baje el cuadrante alejándolo del objetivo antes de comenzar la siguiente observación.
7. Repita los pasos 3–6 hasta haber registrado **cinco observaciones independientes** para el mismo punto de referencia.
8. Repita el procedimiento para cada uno de los puntos de referencia restantes.
9. Repita las mediciones de la geometría siempre que cambien la posición del observador, la posición del objetivo, la altura de los ojos u otros elementos relevantes de la configuración.

Los ángulos de referencia no deben registrarse en la tabla canónica de observaciones, salvo que hayan sido proporcionados directamente como mediciones originales. Los ángulos calculados a partir de la geometría registrada constituyen cantidades derivadas y pertenecen al análisis posterior.

---

# Requisitos de los Datos

Las observaciones producidas mediante este protocolo deberán ajustarse a la especificación de observación aplicable para la calibración del cuadrante.

La especificación de observación define:

* los campos obligatorios;
* la semántica de cada campo;
* las representaciones canónicas;
* los tipos de datos permitidos; y
* los metadatos requeridos.

Este protocolo no redefine dichos requisitos.

---

# Control de Calidad

Los observadores deben:

* verificar que el instrumento permanezca mecánicamente estable durante toda la encuesta;
* evitar perturbar la plomada antes de registrar las lecturas;
* asegurar que cada observación represente una única medición intencional;
* registrar las observaciones directamente, sin reconstrucciones retrospectivas; y
* documentar cualquier condición inusual que pueda afectar la calidad de las mediciones.

> Las observaciones consecutivas deben representar intentos de medición independientes. Los observadores no deben registrar múltiples lecturas obtenidas a partir de una única alineación del instrumento. Siempre que sea práctico, las observaciones correspondientes a un mismo punto de referencia deben intercalarse con observaciones de otros puntos de referencia. Cuando sea necesario realizar observaciones consecutivas del mismo punto de referencia, el cuadrante debe bajarse completamente y volver a alinearse antes de cada medición.

Si una observación no puede considerarse razonablemente confiable, deberá conservarse únicamente cuando las circunstancias queden completamente documentadas. En caso contrario, la medición deberá repetirse y registrarse la observación de reemplazo.

---

# Desviaciones del Protocolo

Las desviaciones de este protocolo no invalidan automáticamente una encuesta.

Toda desviación que pueda influir en la interpretación deberá documentarse en las notas de la encuesta, proporcionando información suficiente para su revisión posterior.

Algunos ejemplos incluyen:

* fallas del equipo;
* perturbaciones ambientales;
* cambios en la geometría de calibración;
* secuencias de observación interrumpidas; y
* errores del observador detectados durante la recopilación de datos.

---

# Resultados Esperados

Una encuesta producida mediante este protocolo debe incluir:

* `survey.json`;
* una o más tablas de observaciones de calibración del cuadrante conformes con la especificación de observación correspondiente;
* `notes.csv`, cuando sea aplicable;
* archivos adjuntos de apoyo, cuando sea aplicable; y
* toda la información de procedencia requerida.

---

# Referencias

* Especificación de Encuestas de Kepler
* Especificación de Observación para la Calibración del Cuadrante
* Documentación del Cuadrante Kepler
