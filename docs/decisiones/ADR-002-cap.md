# ADR-002: Postura CAP y tipo de consistencia

- **Fecha:** 2026-11-26
- **Estado:** Propuesta (Arturo, 26 nov); se ratifica con la aprobación de los 4 en el PR del #12 y en persona el 30 nov
- **Responsable:** Arturo
- **Aprobada por:** Pendiente: los 4 integrantes

## Contexto

La base relacional tiene un primario (N2) y una réplica (N3) conectados por la VPN (#18, #19). Si la red entre ellos se corta (partición de red), el sistema tiene que elegir entre seguir aceptando cambios (disponibilidad) o detenerse para no perder ninguno (consistencia). El centro asigna unos 700 paquetes al día y los repartidores confirman entregas desde la calle con datos móviles.

## Alternativas consideradas

| Alternativa | A favor | En contra |
| --- | --- | --- |
| CP con réplica síncrona: N2 no confirma un cambio hasta que N3 lo tiene | Nunca se pierde una asignación ni una entrega confirmada | Si N3 o la VPN fallan, N2 se detiene y nadie puede asignar ni confirmar entregas |
| AP con réplica asíncrona: N2 confirma enseguida y N3 se pone al día después | Si N3 cae, el centro sigue trabajando | Si N2 cae, se pueden perder los cambios que N3 no alcanzó a recibir |
| Asíncrona con promoción manual: como la anterior, pero N3 solo se vuelve primario cuando una persona lo decide (#25) | Evita dos primarios al mismo tiempo | La recuperación no es automática |

## Decisión

Decisión de Arturo (26 nov): **CP con réplica síncrona** entre el primario (N2) y la réplica (N3). N2 no confirma un cambio hasta que N3 lo tiene escrito.

## Justificación con datos del sistema

Ensayo del 26 nov en una sola laptop (evidencia en `docs/evidencias/issue-19/`):

| Medición | Asíncrona | Síncrona |
| --- | --- | --- |
| Tiempo por cambio confirmado (promedio de 5) | 0.59 ms | 1.42 ms (0.79 ms sin el primero) |
| Mayor retraso de la réplica al cargar 100 000 paquetes | 0.36 s y 9.8 MB pendientes | No aplica: N2 espera a N3 |
| Si N3 se detiene | N2 sigue y N3 se pone al día después | El cambio queda esperando (191 s en la prueba) y se completa solo al volver N3 |

Con unos 700 paquetes al día, el centro hace pocos cambios por minuto, así que el costo extra por cambio no se nota. Lo que no se puede permitir es perder una asignación o una entrega ya confirmada: con réplica asíncrona, si N2 cae, lo que N3 no alcanzó a recibir (hasta 9.8 MB en la carga masiva) se pierde.

## Consecuencias

- Si N3 o la VPN fallan, N2 deja de confirmar cambios: nadie puede asignar ni confirmar entregas hasta que N3 vuelva o se quite la espera a mano (`synchronous_standby_names = ''`). Este procedimiento se documenta en el #25.
- En la prueba de falla del #25: si se apaga N3, el sistema se congela pero no pierde nada; si se apaga N2, N3 tiene todo lo confirmado y se promueve como nuevo primario.
- Por la VPN entre laptops el costo por cambio será mayor que en una sola laptop; se mide el lunes 30 nov y se anota aquí.
