# Ballestilla Kepler

## Propósito

La Ballestilla Kepler es el principal instrumento de medición angular utilizado en todo el proyecto Kepler.

Su propósito no es recrear un artefacto histórico, sino proporcionar un instrumento económico, comprensible y científicamente útil que permita a los participantes medir separaciones angulares entre objetos del cielo.

Estas mediciones constituyen las observaciones originales sobre las que se construyen todas las investigaciones científicas posteriores.

La ballestilla es, por tanto, uno de los instrumentos fundamentales del Observatorio Kepler.

La implementación de referencia actual (Prototipo 0.2) utiliza una funda deslizante de cartón, una traviesa fija de madera y fiduciales montados permanentemente que proporcionan múltiples rangos de medición. Revisiones futuras podrán perfeccionar este diseño manteniendo la compatibilidad con el modelo general de medición.

------------------------------------------------------------------------

# ¿Por qué una Ballestilla?

La ballestilla ocupa un lugar singular en la historia de la astronomía.

Mucho antes de la invención del telescopio, los astrónomos medían el cielo comparando ángulos entre objetos celestes.

Esas mediciones permitieron a astrónomos como Regiomontanus, Gemma Frisius y Tycho Brahe construir mapas cada vez más precisos del cielo y, en última instancia, proporcionaron la base observacional para que Johannes Kepler descubriera las leyes del movimiento planetario.

Una breve descripción de la ballestilla histórica y de la filosofía de diseño de la implementación Kepler se encuentra en la [Especificación de Diseño](design.md).

El proyecto Kepler comienza con la misma actividad fundamental:

**medir cuidadosamente ángulos.**

------------------------------------------------------------------------

# Función Científica

La ballestilla **no** mide:

- distancias;
- órbitas planetarias;
- brillo;
- velocidad;
- tamaño físico.

En cambio, mide una sola cosa de manera excepcionalmente eficaz:

> **La separación angular entre dos objetos sobre la esfera celeste.**

Esta sencilla medición se vuelve sorprendentemente poderosa cuando se combina con:

- observaciones repetidas;
- marcas temporales precisas;
- estrellas de referencia conocidas;
- observaciones aportadas por muchos participantes.

Cada observación realizada con la ballestilla contribuye a una representación compartida del cielo, a partir de la cual pueden desarrollarse modelos científicos cada vez más sofisticados.

------------------------------------------------------------------------

# Filosofía de Diseño

La Ballestilla Kepler está diseñada de acuerdo con cuatro principios.

## Accesibilidad

Cualquier participante, en cualquier parte del mundo, debe poder construir u obtener un instrumento compatible utilizando materiales económicos.

La participación científica no debe depender de los recursos económicos.

------------------------------------------------------------------------

## Transparencia

Toda medición debe surgir de una geometría que el participante pueda comprender.

El instrumento debe hacer visible el proceso de medición, en lugar de ocultarlo detrás de sistemas electrónicos o automatizados.

------------------------------------------------------------------------

## Reproducibilidad

Distintos participantes que utilicen instrumentos construidos de manera independiente deben ser capaces de producir mediciones comparables después de la calibración.

El objetivo no es disponer de instrumentos idénticos, sino de observaciones reproducibles.

------------------------------------------------------------------------

## Evolución

La Ballestilla Kepler es un instrumento en evolución.

Su diseño puede mejorar con el tiempo a medida que los participantes descubran nuevas mejoras.

Cada revisión del diseño debe permanecer científicamente documentada y ser reproducible.

Los instrumentos de revisiones anteriores continúan siendo contribuciones valiosas para el proyecto.

------------------------------------------------------------------------

# Requisitos Funcionales

Toda ballestilla compatible con Kepler debe ser capaz de:

- medir la separación angular entre dos objetos celestes visibles;
- producir mediciones repetidas con incertidumbre documentada;
- permitir la calibración utilizando separaciones angulares conocidas;
- identificarse mediante un identificador único de instrumento;
- registrar la revisión del instrumento utilizada para obtener las observaciones.

------------------------------------------------------------------------

# Rendimiento Esperado

El objetivo de la Ballestilla Kepler **no** es alcanzar la máxima precisión.

En cambio, el instrumento debe producir mediciones cuya incertidumbre sea comprendida y documentada.

Los objetivos iniciales del proyecto son aproximadamente:

- costo de construcción inferior a USD \$10;
- tiempo de construcción inferior a una hora;
- repetibilidad típica del orden de un grado o mejor después de la calibración;
- funcionamiento sin electricidad ni equipo especializado.

Estos valores podrán evolucionar a medida que el proyecto avance.

------------------------------------------------------------------------

# Relación con Otros Instrumentos

La ballestilla es uno de los componentes del Sistema de Medición Kepler.

Junto con el cuadrante y el gnomon proporciona información complementaria.

| Instrumento | Medición principal                             |
|-------------|------------------------------------------------|
| Ballestilla | Separación angular entre objetos celestes      |
| Cuadrante   | Altitud sobre el horizonte local               |
| Gnomon      | Posición solar y geometría local de referencia |

Cada instrumento mide un aspecto diferente del cielo observable.

En conjunto, permiten a los participantes ubicar objetos celestes dentro de un marco observacional común.

------------------------------------------------------------------------

# Medición Antes que Teoría

La ballestilla encarna una de las ideas centrales del proyecto Kepler.

Antes de que los científicos puedan explicar el cielo, primero deben describirlo.

Por ello, el instrumento precede a toda investigación científica.

Los participantes utilizan la ballestilla para producir observaciones.

Esas observaciones se convierten en evidencia.

Solo entonces las investigaciones preguntan qué conclusiones están justificadas.

------------------------------------------------------------------------

# Estructura del Repositorio

Este directorio contiene la especificación completa de la Ballestilla Kepler.

- **`design.md`** — diseño de ingeniería y geometría de medición
- [**`build-guide.md`**](build-guide.es.md) — instrucciones de construcción paso a paso
- **`calibration/`** — procedimientos de calibración, campañas de calibración y análisis de apoyo

El directorio de calibración contiene:

- el protocolo de calibración;
- documentación de campañas de calibración;
- conjuntos de datos originales;
- cuadernos exploratorios;
- tablas de análisis derivadas.

En conjunto, estos recursos definen, validan y documentan la implementación de referencia actual del instrumento.

------------------------------------------------------------------------

# Versionado

La Ballestilla Kepler debe considerarse infraestructura científica.

Se esperan revisiones de diseño.

Cada revisión debe mejorar uno o más aspectos del instrumento, preservando, siempre que sea posible, la compatibilidad con observaciones anteriores.

Las observaciones siempre deben registrar la revisión del instrumento utilizada para obtenerlas.

------------------------------------------------------------------------

# Mirando Hacia el Futuro

La primera tarea realizada con una Ballestilla Kepler es engañosamente sencilla:

Medir el ángulo entre dos objetos del cielo.

Todo lo que viene después —desde mapas celestes, hasta el movimiento planetario, modelos cosmológicos en competencia, inferencia bayesiana y aprendizaje automático— comienza con ese único acto de medición cuidadosa.

La ballestilla no es simplemente un instrumento de medición.

Es la primera contribución del participante a una empresa científica compartida.
