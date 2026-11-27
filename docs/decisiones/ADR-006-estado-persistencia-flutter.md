# ADR-006: Estado y persistencia local en Flutter

- **Fecha:** 2026-11-25
- **Estado:** Propuesta
- **Responsable:** Jesús
- **Aprobada por:** (revisor del PR del #14)

## Contexto

La app es una sola base de código para tres plataformas: Android (repartidor), web (supervisor y administrador) y Linux de escritorio. Varias pantallas necesitan los mismos datos: el token y el rol de la sesión, la ruta del día y los paquetes por asignar. Además, el repartidor trabaja con datos móviles y la señal se puede cortar unos minutos. Las confirmaciones de entrega no se deben perder mientras tanto (#41).

Datos del sistema:

- Un repartidor lleva como máximo `capacidad_diaria` paquetes al día, que por omisión son 60 (`repartidor.capacidad_diaria` en `db/esquema/001_tablas.sql`).
- El centro recibe unos 700 paquetes al día, así que un supervisor ve a lo mucho unos cientos de paquetes de su zona.
- Lo que se guarda en el dispositivo es poco: una sesión y, como máximo, unas decenas de confirmaciones pendientes con foto.

## Alternativas consideradas

**Manejo de estado**

| Alternativa | A favor | En contra |
| --- | --- | --- |
| Solo `setState` | Sin dependencias | Hay que pasar la sesión de pantalla en pantalla; no escala a varias pantallas |
| `provider` con `ChangeNotifier` | Es la opción de la documentación oficial de Flutter, poco código y fácil de explicar | Con muchas dependencias entre estados se vuelve desordenado |
| Riverpod | Más seguro en tiempo de compilación y fácil de probar | Más conceptos nuevos para un equipo que empieza con Flutter |
| BLoC | Separa muy bien eventos y estados | Mucho código repetido para pantallas sencillas |

**Persistencia local**

| Alternativa | A favor | En contra |
| --- | --- | --- |
| `shared_preferences` | Simple, funciona en Android, web y Linux | Solo pares clave y valor; no sirve para una cola con fotos |
| `sqflite` (con `sqflite_common_ffi` en Linux) | SQL real: la cola de confirmaciones es una tabla y se consulta en orden | No funciona en web |
| Hive | Rápido y funciona en las tres plataformas | Sin SQL y con menos mantenimiento reciente |
| Drift | SQL con tipos y migraciones | Generación de código: más pasos para el equipo |

## Decisión

Usamos `provider` con `ChangeNotifier` para el estado. Para guardar datos en el dispositivo usamos `sqflite` en Android y Linux (cola de confirmaciones) y `shared_preferences` en web (solo la sesión, porque en web no se confirman entregas).

## Justificación con datos del sistema

El volumen local es pequeño: a lo mucho 60 paquetes en la ruta de un repartidor y unas decenas de confirmaciones pendientes. No hace falta una solución pesada. `provider` alcanza para compartir la sesión y la ruta entre pantallas y lo podemos explicar los 4. La cola de confirmaciones necesita guardarse en orden y sobrevivir a que se cierre la app, y eso se resuelve con una tabla de `sqflite`. En web no hay confirmaciones de entrega, así que basta con `shared_preferences` para la sesión.

## Consecuencias

- La capa de persistencia necesita dos implementaciones, una con `sqflite` y otra con `shared_preferences`, detrás de la misma interfaz (#41).
- Si el estado crece mucho, habrá que reconsiderar Riverpod en un ADR nuevo.
- Las pruebas de widgets envuelven la app en `ChangeNotifierProvider`, como hace ya `test/marco_adaptable_test.dart`.