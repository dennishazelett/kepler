# Kepler


## Idiomas

- 🇺🇸 [English](README.md)
- 🇪🇸 Español (este documento)

> **Nota:** Este documento es una traducción del README canónico en inglés. Los nombres de archivos, directorios y otros identificadores del repositorio permanecen en inglés para preservar enlaces estables y una estructura uniforme.

# **Aprender ciencia haciendo ciencia.**

Kepler es un proyecto abierto de educación e investigación que utiliza la astronomía a simple vista para enseñar medición científica y ciencias computacionales —desde la inferencia estadística hasta el aprendizaje automático moderno y la inteligencia artificial— mediante investigación observacional reproducible.

Los participantes construyen instrumentos astronómicos sencillos con materiales económicos, realizan observaciones del cielo nocturno y contribuyen con esas observaciones a un conjunto de datos compartido en constante crecimiento. Esas mediciones constituyen la base para explorar una amplia variedad de métodos inferenciales mientras desarrollan las prácticas de la investigación científica reproducible.

El proyecto culmina no simplemente en modelos o predicciones, sino en la explicación científica. Los participantes evalúan hipótesis en competencia, comunican evidencia y elaboran escritos científicos que justifican sus conclusiones. Muchas investigaciones invitan a reexaminar afirmaciones astronómicas históricas utilizando estándares modernos de evidencia, llegando a sus propias conclusiones a partir de las observaciones en lugar de reproducir narrativas establecidas.

> **¿Cómo podemos inferir la estructura oculta del mundo a partir de observaciones imperfectas?**

------------------------------------------------------------------------

# ¿Qué es Kepler?

Kepler apoya dos formas complementarias de investigación científica.

Las investigaciones fundacionales desarrollan habilidades de observación mediante estudios guiados del cielo.

Las investigaciones de afirmaciones invitan a los participantes a evaluar afirmaciones científicas de importancia histórica mediante investigaciones diseñadas por ellos mismos.

------------------------------------------------------------------------

# ¿Por qué Kepler?

La educación científica moderna suele presentar el conocimiento científico como una colección de hechos establecidos. Kepler aborda la ciencia de una manera diferente.

Los participantes experimentan la ciencia como un proceso:

- construir instrumentos;
- realizar mediciones;
- caracterizar la incertidumbre;
- combinar evidencia;
- comparar modelos en competencia;
- perfeccionar explicaciones.

El proyecto enfatiza que la incertidumbre no es un defecto de la ciencia: es la materia prima a partir de la cual se construye el conocimiento científico.

------------------------------------------------------------------------

# Filosofía del proyecto

Toda observación comienza en el mundo real y termina en una inferencia.

``` text
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

La comprensión científica no está completa hasta que puede ser comunicada, examinada críticamente y reproducida por otras personas.

Cada componente de este repositorio existe para apoyar una o más etapas de ese proceso.

Para una discusión completa del marco conceptual, consulte:

- [`docs/measurement-model.es.md`](docs/measurement-model.es.md)

------------------------------------------------------------------------

# ¿Qué hace diferente a Kepler?

Muchos proyectos de astronomía enseñan astronomía.

Muchos cursos de estadística analizan conjuntos de datos ya existentes.

Muchos cursos de aprendizaje automático comienzan con datos que ya han sido limpiados y organizados.

Kepler comienza mucho antes.

Los participantes crean los datos por sí mismos.

El proyecto trata todo el proceso de medición como un objeto de estudio. Los instrumentos difieren. Los observadores difieren. Las condiciones difieren. Esas diferencias no son problemas que deban eliminarse: son información que debe modelarse.

Esto convierte al proyecto en un entorno natural para estudiar:

- error de medición;
- cuantificación de la incertidumbre;
- modelos jerárquicos;
- simulación;
- razonamiento causal;
- comparación de modelos;
- flujos de trabajo científicos reproducibles.

------------------------------------------------------------------------

# Objetivos del proyecto

Kepler tiene cuatro objetivos complementarios.

## 1. Enseñar medición científica

Los participantes aprenden cómo se producen, calibran y evalúan las observaciones.

## 2. Construir un conjunto de datos astronómicos abierto

Las observaciones recopiladas a lo largo de múltiples ediciones del curso contribuyen a un conjunto de datos longitudinal en crecimiento, adecuado para investigación y educación.

## 3. Comparar métodos inferenciales

El repositorio está diseñado para apoyar múltiples enfoques de inferencia, incluidos:

- estadística descriptiva;
- regresión;
- modelos de efectos mixtos;
- inferencia bayesiana;
- modelos de espacio de estados;
- procesos gaussianos;
- aprendizaje supervisado;
- aprendizaje no supervisado;
- aprendizaje profundo.

Ningún marco se considera el enfoque "correcto".

## 4. Promover la investigación reproducible

Todos los aspectos del proyecto —incluyendo diseños de instrumentos, protocolos de observación, esquemas de datos, simulaciones, métodos de inferencia, investigaciones, flujos de trabajo y software— están bajo control de versiones y documentados de manera abierta.

------------------------------------------------------------------------

# Organización del repositorio

El repositorio está organizado alrededor del proceso de medición, y no alrededor de un lenguaje de programación o un marco estadístico en particular.

| Directorio | Propósito |
|-------------------|-----------------------------------------------------|
| [`docs/`](docs/) | Visión del proyecto y documentación conceptual |
| [`instruments/`](instruments/) | Diseños de instrumentos, guías de construcción y procedimientos de calibración |
| [`protocols/`](protocols/) | Procedimientos estandarizados de observación y control de calidad |
| [`data/`](data/) | Contrato de datos, esquemas, encuestas de ejemplo y herramientas de validación |
| [`simulation/`](simulation/) | Generación de datos sintéticos y simulación del proceso de medición |
| [`src/`](src/) | Utilidades principales de software |
| [`inference/`](inference/) | Métodos estadísticos y de aprendizaje automático |
| [`course/`](course/) | Materiales educativos |
| [`tests/`](tests/) | Pruebas de validación y reproducibilidad |
| [`experiments/`](experiments/) | Benchmarks, estudios de ablación, recuperación de modelos y experimentos computacionales controlados |
| [`investigations/`](investigations/) | Investigaciones fundacionales y de afirmaciones, incluyendo orientación y análisis específicos de cada proyecto |
| [`workflows/`](workflows/) | Flujos de trabajo de referencia para combinar datos, software y componentes inferenciales de Kepler |

------------------------------------------------------------------------

# Estado actual

Kepler se encuentra en una etapa temprana de desarrollo activo.

El repositorio ya incluye:

- un diseño completo del instrumento cross-staff y su guía de construcción;
- una encuesta de calibración validada;
- una especificación inicial de datos y esquemas JSON;
- herramientas para validar encuestas;
- documentación para colaboradores.

El proyecto continuará evolucionando a medida que se desarrollen nuevos instrumentos, protocolos de observación, conjuntos de datos, simulaciones y materiales educativos.

El repositorio ya contiene una implementación de referencia completa del contrato inicial de datos, incluyendo una encuesta de calibración validada del cross-staff.

Las prioridades de desarrollo y los objetivos de largo plazo continúan definiéndose.

------------------------------------------------------------------------

# Primeros pasos

Si es la primera vez que visita el proyecto, el orden recomendado de lectura es:

1.  [`docs/project-charter.es.md`](docs/project-charter.es.md)
2.  [`docs/measurement-model.es.md`](docs/measurement-model.es.md)
3.  [`docs/celestial-coordinate-systems.es.md`](docs/celestial-coordinate-systems.es.md)
4.  [`instruments/quadrant/README.es.md`](instruments/quadrant/README.es.md)

Estos documentos describen la motivación, el marco conceptual y la dirección a largo plazo del proyecto.

------------------------------------------------------------------------

# Cómo contribuir

Las contribuciones son bienvenidas.

El proyecto se beneficia de la experiencia en astronomía, estadística, aprendizaje automático, ingeniería de software, educación, historia de la ciencia, diseño de instrumentos y visualización científica.

Lea primero:

- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)

antes de enviar cambios.

------------------------------------------------------------------------

# Citación

Si utiliza Kepler en investigación o docencia, cite el repositorio de Git.

Se añadirá un archivo formal `CITATION.cff` y una guía de citación versionada antes del primer lanzamiento público.

------------------------------------------------------------------------

# Licencia

Kepler se distribuye bajo los términos de la licencia MIT.

Consulte [`LICENSE`](LICENSE) para conocer el texto completo de la licencia.

------------------------------------------------------------------------

# Agradecimientos

Kepler se inspira en siglos de astronomía observacional, especialmente en el trabajo de Tycho Brahe y Johannes Kepler, cuyo compromiso con la medición cuidadosa transformó nuestra comprensión del Sistema Solar.

Su trabajo nos recuerda que las revoluciones científicas no comienzan con la certeza, sino con observaciones apenas lo suficientemente precisas como para revelar que nuestras explicaciones actuales son incompletas.
