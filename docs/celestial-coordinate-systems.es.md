# Sistemas de Coordenadas Celestes

## Propósito

Para realizar observaciones científicas, debemos ser capaces de describir dónde aparece un objeto en el cielo.

Los sistemas de coordenadas celestes proporcionan un lenguaje común para registrar esas posiciones.

Comprender estos sistemas es fundamental porque los instrumentos astronómicos no miden "coordenadas". Miden cantidades observables que pueden utilizarse para inferir coordenadas.

---

# El Problema

Supongamos que alguien señala una estrella brillante y dice:

> "Está por allá."

La descripción solo tiene significado para alguien que se encuentre en el mismo lugar y al mismo tiempo.

Las observaciones científicas requieren una descripción que pueda comunicarse, reproducirse y compararse entre distintos observadores.

Un sistema de coordenadas resuelve este problema.

---

# La Esfera Celeste

La esfera celeste es una esfera imaginaria de radio arbitrariamente grande centrada en el observador.

Todos los objetos celestes visibles se proyectan sobre esta esfera.

Aunque las estrellas se encuentran a distancias enormemente diferentes, al describir sus direcciones aparecen como puntos sobre la esfera celeste.

Por lo tanto, la esfera celeste es un modelo geométrico y no un objeto físico.

---

# El Sistema de Coordenadas Horizontales

El sistema de coordenadas más intuitivo está basado en el observador.

Dos coordenadas describen cada objeto visible.

## Altitud

La altitud es el ángulo medido sobre el horizonte local.

* Horizonte = 0°
* Cenit (directamente sobre la cabeza) = 90°

La altitud responde a la pregunta:

> ¿Qué tan alto sobre el horizonte se encuentra el objeto?

---

## Acimut

El acimut mide la dirección alrededor del horizonte.

Responde a la pregunta:

> ¿Hacia qué dirección debo mirar?

La convención exacta varía, pero Kepler adoptará una única convención publicada para todas las observaciones.

---

## Ventajas

* Es fácil de comprender.
* Está directamente relacionado con la observación.
* Es natural para muchos instrumentos sencillos.

---

## Limitaciones

El sistema de coordenadas horizontales depende de:

* la ubicación del observador;
* el momento de la observación.

A medida que la Tierra rota, las coordenadas de cada objeto celeste cambian continuamente.

Por ello, una misma estrella tiene coordenadas horizontales diferentes a lo largo de la noche.

---

# El Sistema de Coordenadas Ecuatoriales

Con frecuencia, los astrónomos necesitan un sistema de coordenadas que no dependa del horizonte local del observador.

Para ello, proyectan el eje de rotación y el ecuador de la Tierra sobre la esfera celeste.

Esto da origen al sistema de coordenadas ecuatoriales.

---

## Declinación

La declinación es análoga a la latitud geográfica.

Mide qué tan al norte o al sur del ecuador celeste se encuentra un objeto.

La declinación se expresa en grados.

---

## Ascensión Recta

La ascensión recta es análoga a la longitud geográfica.

Tradicionalmente, se expresa en horas, minutos y segundos, en lugar de grados.

Veinticuatro horas de ascensión recta corresponden a una vuelta completa alrededor del ecuador celeste.

---

## Ventajas

A diferencia de las coordenadas horizontales, las coordenadas ecuatoriales permanecen esencialmente fijas para los objetos celestes durante escalas normales de observación.

Proporcionan un sistema de referencia común para catálogos y mapas astronómicos.

---

# Instrumentos y Coordenadas

Distintos instrumentos astronómicos miden diferentes cantidades físicas.

Por ejemplo:

| Instrumento                 | Medición directa                                    |
| --------------------------- | --------------------------------------------------- |
| Ballestilla (*Cross-staff*) | Separación angular                                  |
| Cuadrante                   | Altitud                                             |
| Gnomon                      | Altitud solar a partir de la geometría de la sombra |
| Telescopio                  | Dirección de apuntado                               |

Estas mediciones no constituyen, por sí mismas, coordenadas celestes.

En cambio, proporcionan información a partir de la cual pueden inferirse coordenadas celestes.

---

# Kepler

Kepler se interesa por el proceso científico completo.

En lugar de comenzar con coordenadas celestes, el proyecto comienza con observaciones.

```text
Cielo
   ↓
Instrumento
   ↓
Medición
   ↓
Inferencia de coordenadas
   ↓
Inferencia científica
```

Comprender cómo las mediciones se transforman en coordenadas constituye uno de los temas centrales del proyecto.

Documentos futuros describen la geometría, los procedimientos de calibración y los métodos de inferencia que conectan las observaciones originales con el sistema de coordenadas celestes.
