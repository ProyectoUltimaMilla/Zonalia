# Requerimientos de la base de datos

Qué datos guarda Zonalia, quién los usa y qué consultas se hacen todos los días. De aquí salen las tablas (`db/esquema/001_tablas.sql`) y los índices (`db/esquema/002_indices.sql`).

## Contexto

El centro de distribución recibe de J&T unos 700 paquetes al día para la ciudad de Aguascalientes. Cada cuadrilla de repartidores atiende una zona de la ciudad. La app sirve solo dentro del centro: el centro asigna paquetes y el repartidor confirma la entrega.

## Usuarios y lo que consulta cada uno

| Rol | Qué hace | Qué consulta |
| --- | --- | --- |
| Administrador | Da de alta usuarios y repartidores, importa manifiestos | Usuarios, repartidores, manifiestos importados |
| Supervisor | Asigna paquetes a repartidores por zona y revisa el avance | Paquetes por asignar de su zona, carga de cada repartidor, entregas fallidas |
| Repartidor | Ve su ruta del día y confirma cada entrega | Sus paquetes del día en orden, datos del destinatario |

## Consultas frecuentes

| Id | Consulta | Quién | Cuántas veces | Índice |
| --- | --- | --- | --- | --- |
| C1 | Paquetes por asignar de una zona, del más antiguo al más nuevo | Supervisor | Varias veces cada mañana | `paquete_zona_estado_idx` |
| C2 | Buscar un paquete por su guía | Supervisor y repartidor | Una vez por paquete (unas 700 al día) | `paquete_guia_idx` |
| C3 | Rutas del día de una zona y cuántos paquetes lleva cada repartidor | Supervisor | Al asignar y al revisar avance | `ruta_fecha_zona_idx` |
| C4 | Historial de un paquete: en qué rutas estuvo y qué pasó | Supervisor | Cuando hay una queja o un fallo | `asignacion_paquete_idx` |
| C5 | Entregas fallidas en un periodo, por colonia | Supervisor y reportes | Diario y semanal | `entrega_fallida_fecha_idx` |
| C6 | Paquetes de un manifiesto | Administrador | Al importar | `paquete_manifiesto_idx` |

La ruta del día de un repartidor se resuelve con las llaves únicas que ya existen: `ruta (repartidor_id, fecha)` encuentra la ruta y `asignacion (ruta_id, orden)` da los paquetes en orden. Por eso no lleva índice extra.

## Volumen

| Dato | Cantidad |
| --- | --- |
| Paquetes al día | ~700 |
| Paquetes al mes | ~21 000 (30 días) |
| Registros sintéticos para pruebas | 100 000 paquetes (issue #15) |
| Colonias de la ciudad (SEPOMEX) | 531 (issue #9) |

Con este volumen, una consulta sin índice recorre toda la tabla. Los índices de la tabla de arriba evitan eso en las consultas que más se repiten.

## Datos personales

Nombre, teléfono y dirección del destinatario son datos personales. Por eso van en una tabla aparte (`destinatario`), que se cifra y se restringe por rol en el issue #33. El resto del sistema (asignar, reportar) trabaja sin leerlos.