# db

Código SQL de PostgreSQL y catálogos (lineamientos IV-a). Responsable principal: Arturo.

| Carpeta | Contenido | Issue | Responsable |
| --- | --- | --- | --- |
| `esquema/` | Tablas, llaves e índices (`01_tablas.sql`, …), luego procedimientos, funciones y triggers | #5, #11 | Arturo |
| `catalogos/` | Catálogo de colonias de Aguascalientes, zonas y sus scripts de preparación y asignación | #9 | Tadeo |
| Replicación, roles y respaldos | Se agregan en sus issues | #19, #33, #39 | Arturo |

- La explicación de cada parte va en `docs/bd/`.
- Nunca se suben contraseñas: los scripts las leen de variables de entorno (`.env`).


## Quién decidió y cuándo. 
Arturo decidió el criterio el 25 de noviembre. Tú lo aplicaste y lo revisaste en el mapa.
## Opciones evaluadas: 
A sector geográfico, 
B rangos de código postal, 
C volumen esperado.
## Criterio elegido. 
5 zonas por sector geográfico, con el Centro dentro del primer anillo (Av. Convención de 1914), asignadas por código postal.
## Por qué
Era mas facil para saber como distribuir y organizar de manera efiziente a los repartidores.
## Resultado. 
Colonias por zona:
  1 Centro: 48
  2 Norte: 128
  3 Oriente: 137
  4 Sur: 117
  5 Poniente: 101
El Centro es más chico porque solo es el primer anillo. El Campestre se pasó al Poniente para balancear el Norte.

### Correcciones de códigos postales dudosos

CP 20286 (Barlovento): se cambió de zona 5 (Poniente) a zona 4 (Sur), debido a que su ubicación geográfica corresponde al sector sur de la ciudad.
