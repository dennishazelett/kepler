# Modelo de Medición

## Propósito

El proyecto Kepler se construye alrededor de una idea central:

> El conocimiento científico se obtiene realizando mediciones imperfectas del mundo físico y razonando cuidadosamente sobre la incertidumbre presente en esas mediciones.

El proyecto utiliza la astronomía a simple vista como un contexto concreto e históricamente auténtico en el que los participantes construyen instrumentos sencillos, recopilan observaciones y emplean métodos estadísticos y de aprendizaje automático para inferir los procesos físicos subyacentes. El énfasis no está en reproducir la astronomía profesional, sino en comprender cómo se genera, evalúa y acumula la evidencia.

Kepler considera las observaciones individuales no como mediciones directas del **estado latente** del mundo físico, sino como restricciones sobre ese estado. Una altitud, un acimut o una separación angular medidos no determinan directamente la posición de un objeto celeste. En cambio, cada observación aporta evidencia que reduce el conjunto de explicaciones posibles. La comprensión científica surge al combinar muchas de estas restricciones mediante inferencia.

Este documento define el modelo conceptual de medición que sustenta todos los componentes del proyecto. El diseño de instrumentos, los protocolos de observación, los esquemas de datos, la simulación, la inferencia estadística, el aprendizaje automático y los materiales educativos deben mantenerse coherentes con este modelo.

---

# El Proceso de Medición

El proyecto considera cada observación como una realización del siguiente proceso causal:

```text
Sistema Solar
      ↓
Cielo observable
      ↓
Instrumento
      ↓
Observador
      ↓
Medición
      ↓
Conjunto de datos
      ↓
Inferencia
      ↓
Comprensión científica
      ↓
Comunicación científica
```

Cada etapa introduce información y, al mismo tiempo, puede introducir incertidumbre, sesgo o error.

El propósito del proyecto no es eliminar estas imperfecciones, sino caracterizarlas y razonar rigurosamente sobre ellas.

---

# Etapa 1 — Sistema Solar

El estado físico del Sistema Solar existe independientemente del observador.

Algunos ejemplos incluyen:

* posiciones planetarias;
* velocidades planetarias;
* rotación de la Tierra;
* posición orbital de la Tierra;
* posición de la Luna;
* marco de referencia estelar.

En conjunto, estas cantidades definen el **estado latente** del mundo físico. Los participantes nunca observan ese estado de manera directa.

---

# Etapa 2 — Cielo observable

El estado físico produce un cielo aparente visto desde una ubicación y un momento específicos.

Esta etapa incluye efectos como:

* latitud y longitud del observador;
* fecha y hora;
* rotación de la Tierra;
* refracción atmosférica;
* obstrucciones del horizonte;
* condiciones de visibilidad.

El cielo observable constituye la interfaz entre la mecánica celeste y la medición.

---

# Etapa 3 — Instrumento

El instrumento transforma el cielo observable en cantidades medibles.

Inicialmente, el proyecto se centra en instrumentos sencillos construidos por los propios participantes, tales como:

* ballestillas (*cross-staffs*);
* cuadrantes.

Cada instrumento posee propiedades medibles, entre ellas:

* revisión del diseño;
* materiales de construcción;
* dimensiones;
* historial de calibración;
* precisión estimada.

El instrumento se considera parte integral del proceso de medición y no simplemente una herramienta pasiva.

---

# Etapa 4 — Observador

Los observadores utilizan instrumentos para producir mediciones.

Cada observador aporta sus propias características, entre ellas:

* experiencia;
* habilidad de calibración;
* consistencia;
* precisión en el registro de datos;
* toma de decisiones.

Es de esperar que distintos observadores produzcan mediciones sistemáticamente diferentes bajo condiciones idénticas.

Esta variabilidad constituye una característica del proyecto, y no un defecto.

---

# Etapa 5 — Medición

Las mediciones constituyen las observaciones primarias registradas por el proyecto.

Cada medición registra una propiedad del cielo observable bajo un conjunto particular de condiciones de observación.

Algunos ejemplos incluyen:

* separaciones angulares;

* altitudes;

* acimuts;

* marcas temporales;

* mediciones de calibración.

Aunque con frecuencia estas mediciones se tratan como si determinaran directamente las coordenadas celestes, Kepler adopta una perspectiva diferente.

**Cada medición constituye una restricción sobre el estado desconocido del mundo físico.**

Por ejemplo:

* una medición de altitud restringe la posible ubicación de un objeto sobre la esfera celeste;

* una medición de acimut aporta una restricción direccional independiente;

* una separación angular restringe las posiciones relativas de dos objetos.

Ninguna observación individual determina completamente el estado latente.

La comprensión científica surge al combinar numerosas restricciones independientes recopiladas en distintos momentos, desde diferentes lugares, utilizando distintos instrumentos y por diferentes observadores.

Cada medición va acompañada de metadatos que describen las circunstancias bajo las cuales fue obtenida.

Las mediciones constituyen registros inmutables.

Las correcciones, calibraciones o evaluaciones de calidad deben almacenarse por separado y nunca sustituir las observaciones originales.

---

# Etapa 6 — Conjunto de datos

Las mediciones individuales solo adquieren verdadero valor científico cuando se agregan.

El conjunto de datos del proyecto incluye:

* observaciones;
* observadores;
* instrumentos;
* sitios;
* registros de calibración;
* ediciones del curso;
* información ambiental.

Por lo tanto, el conjunto de datos representa tanto las observaciones astronómicas como el proceso completo de medición que las produjo.

---

# Etapa 7 — Inferencia

La inferencia combina las restricciones observacionales para estimar el estado latente del mundo físico.

El proyecto apoya intencionalmente múltiples enfoques de inferencia.

Algunos ejemplos incluyen:

* estadística descriptiva;
* modelos de regresión;
* modelos bayesianos jerárquicos;
* modelos de espacio de estados;
* procesos gaussianos;
* aprendizaje supervisado;
* aprendizaje no supervisado;
* detección de anomalías;
* aprendizaje profundo.

Ningún método de inferencia se considera privilegiado dentro de la arquitectura del proyecto.

Los métodos de inferencia deben entenderse como explicaciones alternativas que compiten por explicar las mismas observaciones.

---

# Etapa 8 — Comprensión científica

La comprensión científica surge al comparar los modelos con las observaciones.

Los participantes deben experimentar la ciencia como un proceso iterativo de:

1. proponer explicaciones;
2. recopilar evidencia;
3. perfeccionar modelos;
4. evaluar la incertidumbre;
5. mejorar las predicciones.

Por ello, el proyecto pone mayor énfasis en el razonamiento científico que en la obtención de respuestas correctas.

---

# Etapa 9 — Comunicación científica

La comprensión científica solo se vuelve duradera cuando puede comunicarse.

Se anima a los participantes a comunicar no solo sus conclusiones, sino también las observaciones, los supuestos, los métodos, las incertidumbres y el razonamiento que condujeron a ellas.

La comunicación permite que las investigaciones sean examinadas, reproducidas, criticadas, perfeccionadas y ampliadas por otras personas.

Por ello, los argumentos científicos pasan a formar parte del proceso de medición y no constituyen simplemente un informe final.

---

# Simulación

La simulación ocupa un lugar único dentro del proyecto.

Un simulador comienza con un estado latente conocido y genera observaciones sintéticas modelando cada etapa del proceso de medición.

Esto permite evaluar métodos de inferencia bajo condiciones controladas en las que la realidad subyacente es conocida.

La simulación respalda:

* desarrollo de software;
* validación de modelos;
* ejercicios educativos;
* estudios comparativos (*benchmarks*);
* estudios de recuperación de modelos.

La arquitectura de simulación debe reflejar el proceso real de medición con la mayor fidelidad posible.

---

# Principios de Diseño

El proyecto sigue varios principios rectores.

## Medir primero

Las observaciones siempre deben preceder a la inferencia.

Los modelos se construyen para explicar las mediciones, no para generarlas.

## Preservar la procedencia

Las observaciones originales nunca deben sobrescribirse.

Las cantidades derivadas deben permanecer reproducibles a partir de las mediciones originales.

Existen estándares comunitarios compartidos para que observaciones recopiladas de forma independiente sean interoperables, preservando al mismo tiempo la procedencia de cada medición.

## Modelar la incertidumbre

La incertidumbre es una propiedad esencial de la medición científica.

El objetivo es comprender la incertidumbre, no eliminarla.

## Apoyar múltiples marcos inferenciales

El repositorio debe fomentar la comparación entre métodos estadísticos y de aprendizaje automático.

Las decisiones arquitectónicas deben evitar privilegiar una única implementación o un único ecosistema de software.

## Construir a partir de componentes simples

El proyecto debe comenzar con instrumentos sencillos, observaciones simples y enfoques inferenciales básicos antes de introducir una mayor complejidad.

---

# Alcance

El proyecto Kepler no pretende reproducir la astrometría profesional ni competir con los estudios astronómicos modernos.

Su propósito es crear un entorno de medición rico y auténtico en el que los participantes puedan aprender:

* ciencia observacional;
* teoría de la medición;
* cuantificación de la incertidumbre;
* inferencia estadística;
* aprendizaje automático;
* investigación reproducible;
* práctica científica colaborativa.

La astronomía proporciona el contexto.

La inferencia es el tema de estudio.

El razonamiento científico es el objetivo.
