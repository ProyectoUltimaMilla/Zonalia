# ADR-001: Fragmentación y shard key

- **Fecha:** 2026-11-23
- **Estado:** Propuesta (tomada de la propuesta aprobada en la primera entrega; se completa con datos en el issue #12)
- **Responsable:** Arturo
- **Aprobada por:** (los 4 integrantes en el PR del #12)

## Contexto

La operación del centro ya trabaja por zonas: cada cuadrilla atiende una zona y la mayoría de las consultas del día filtran por ella (paquetes por asignar, rutas, entregas pendientes). Los datos del destinatario son personales y deben poder cifrarse y restringirse.

## Alternativas consideradas

_El equipo completa esta tabla en el #12._

| Alternativa | A favor | En contra |
| --- | --- | --- |
| Zona |  |  |
| Colonia |  |  |
| Fecha de recepción |  |  |

## Decisión

Propuesta del equipo en la primera entrega: fragmentación horizontal de `paquete` por **zona** y fragmentación vertical que separa los datos del **destinatario** del paquete. Un directorio de fragmentos registra a qué zona pertenece cada colonia y en qué nodo vive cada zona.

## Justificación con datos del sistema

_Se completa en el #12 con el conteo de paquetes por zona del generador (#15) y las consultas frecuentes del documento de requerimientos (#5)._

## Consecuencias

_Se completa en el #12._
