# Cuadrante

El cuadrante es el segundo instrumento de referencia del proyecto Kepler.

A diferencia de la ballestilla, que estima la separación angular mediante mediciones lineales y reconstrucción geométrica, el cuadrante mide directamente ángulos de elevación utilizando un arco graduado y una plomada. En conjunto, ambos instrumentos ilustran enfoques complementarios para la medición astronómica y ofrecen la oportunidad de comparar su precisión, exactitud, requisitos de calibración y características de error.

El cuadrante está diseñado para apoyar tanto investigaciones históricas como la práctica científica moderna. Aunque se inspira en instrumentos históricos, el objetivo no es reconstruirlos por sí mismos. En cambio, el instrumento sirve como un medio para estudiar cómo la observación cuidadosa, la calibración, el análisis de la incertidumbre y la inferencia estadística se combinan para producir conocimiento científico.

## Objetivos de Aprendizaje

Construir y utilizar el cuadrante introduce a los participantes en:

- medición angular directa;
- la gravedad como referencia de medición;
- calibración de instrumentos graduados;
- incertidumbre observacional;
- comparación entre instrumentos;
- recopilación reproducible de datos.

Estos conceptos complementan los introducidos por la ballestilla y amplían el conjunto de técnicas de observación disponibles dentro de Kepler.

## Contenido del Repositorio

| Archivo | Propósito |
|----|----|
| `design.md` | Principios de medición, contexto histórico y decisiones de ingeniería |
| [build-guide.es.md](build-guide.es.md) | Instrucciones de construcción y materiales requeridos |
| `calibration.md` | Principios, fundamentos e interpretación de la calibración |
| `bill-of-materials.md` | Componentes necesarios para construir el instrumento |

Los procedimientos operativos de calibración se mantienen por separado en `protocols/quadrant/calibration/protocol.md`.

## Relación con el Modelo de Datos de Kepler

El cuadrante constituye la primera prueba de la arquitectura independiente del instrumento desarrollada para Kepler.

Se espera que los metadatos de la encuesta, el flujo de validación y la organización del repositorio permanezcan sin cambios. Únicamente el esquema de observación específico del instrumento debe diferir del utilizado por la ballestilla.

Esto ofrece la oportunidad de evaluar si el modelo de datos de Kepler logra separar correctamente los conceptos observacionales comunes de los detalles de medición específicos de cada instrumento.

## Estado Actual

El cuadrante de referencia de Kepler ha sido diseñado, construido y evaluado mediante una campaña inicial de calibración.

El trabajo actual se centra en perfeccionar el protocolo de calibración, documentar el rendimiento del instrumento y extender su uso desde mediciones de calibración controladas hacia observaciones astronómicas de campo.
