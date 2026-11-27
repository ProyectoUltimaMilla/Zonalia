# ADR-003: Distribución de nodos

- **Fecha:** 2026-11-26
- **Estado:** Pendiente (se decide en persona el 30 nov)
- **Responsable:** Arturo
- **Aprobada por:** (revisores del PR del #18)

## Contexto

Zonalia tiene 4 nodos: N1 (API, Nginx y Suricata), N2 (PostgreSQL primario), N3 (PostgreSQL réplica) y N4 (MongoDB y monitoreo). En esta etapa cada nodo es la laptop de un integrante; la arquitectura ubica N1 y N2 en el centro de distribución (locales) y N3 y N4 fuera de él (remotos). Las laptops se conectan por WireGuard (#18).

## Alternativas consideradas

| Alternativa | A favor | En contra |
| --- | --- | --- |
| A: cada quien hospeda lo suyo (N1 Hugo, N2 Arturo, N3 Jesús, N4 Tadeo) | Cada responsable prueba su componente en su laptop; 4 nodos reales | Si una laptop se apaga, ese nodo se cae |
| B: Arturo concentra lo local (N1 y N2 Arturo, N3 Jesús, N4 Tadeo) | Menos laptops necesarias para que funcione la API | Una sola laptop carga API, base y Suricata; solo hay 3 nodos de verdad |
| C: la réplica en la laptop más estable | La réplica es lo más crítico en la prueba de falla (#25) | Hay que medir antes cuál laptop es más estable |
| Suricata en N1 o en N4 | En N1 ve el tráfico que llega a la API, que es lo único expuesto | En N4 no vería el tráfico de la API |

## Decisión

_Pendiente: los nodos se asignan más adelante._

## Justificación con datos del sistema

_Pendiente._

## Consecuencias

_Pendiente._
