# ADR-001: Fragmentación y shard key

- **Fecha:** 2026-11-23
- **Estado:** Propuesta (Arturo, 26 nov); se ratifica con la aprobación de los 4 en el PR del #12 y en persona el 30 nov
- **Responsable:** Arturo
- **Aprobada por:** Pendiente: los 4 integrantes

## Contexto

La operación del centro ya trabaja por zonas: cada cuadrilla atiende una zona y la mayoría de las consultas del día filtran por ella (paquetes por asignar, rutas, entregas pendientes). Los datos del destinatario son personales y deben poder cifrarse y restringirse.

## Alternativas consideradas

| Alternativa | A favor | En contra |
| --- | --- | --- |
| Zona (5 valores) | Es como trabaja la operación: una cuadrilla por zona; las consultas del día filtran por zona; los cuatro sectores quedan de tamaño parecido | El Centro queda más chico; una zona nueva necesita su partición |
| Colonia (531 valores) | Más fina | 531 particiones para unos 700 paquetes al día; muchas colonias casi vacías; ninguna consulta del día filtra por una sola colonia |
| Fecha de recepción | Sirve para archivar o borrar lo viejo | Las consultas del día no filtran por rango de fechas; la partición de hoy se llevaría toda la carga |

## Decisión

Decisión de Arturo (26 nov): la shard key de `paquete` es la **zona**. Cada paquete cae en su zona por su colonia: la colonia pertenece a un código postal y cada código postal está asignado a una de las 5 zonas. La colonia no es la shard key: es el dato que la determina. Se mantiene la fragmentación vertical que separa los datos del destinatario.

## Justificación con datos del sistema

- Con los 100 000 paquetes sintéticos (semilla 2026), las particiones quedan en 9 199 (Centro), 24 063 (Norte), 25 689 (Oriente), 21 881 (Sur) y 19 168 (Poniente). Entre los cuatro sectores, el más grande es 1.34 veces el más chico; el Centro es menor a propósito porque solo es el primer anillo.
- Las consultas frecuentes de `docs/bd/requerimientos.md` (paquetes por asignar, rutas y entregas pendientes) filtran por zona. El `EXPLAIN` del #12 muestra que PostgreSQL solo lee la partición de esa zona (poda de particiones).
- Partir por colonia daría 531 particiones con unos 700 paquetes diarios repartidos entre ellas: casi todas quedarían vacías y ninguna consulta se beneficiaría.

## Consecuencias

- Cada zona puede vivir en un nodo distinto; el directorio de fragmentos registra en qué nodo está cada una.
- Una zona nueva cae en `paquete_sin_zona` hasta que se cree su partición y se registre en el directorio.
- Una consulta de varias zonas (por ejemplo, el reporte general del supervisor) lee varias particiones; es aceptable porque es poco frecuente.
