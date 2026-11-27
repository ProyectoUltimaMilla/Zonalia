# Catálogo de colonias y zonas

Colonias de la ciudad de Aguascalientes con la zona de reparto a la que pertenecen. La zona es la llave de fragmentación de la base de datos (ver `docs/decisiones/ADR-001-shard-key.md`) y la usa el generador de datos sintéticos.

## Fuente

- Catálogo Nacional de Códigos Postales de Correos de México (SEPOMEX), estado de Aguascalientes, formato TXT.
- Descargado el 2026-11-24 del sitio de Correos de México (Consulta de códigos postales → exportar por estado).
- El TXT original no está en el repositorio porque su aviso legal no permite redistribuirlo.

## Cómo regenerar

1. Descarga el TXT, renómbralo a `CPdescarga_ags.txt` y ponlo en esta carpeta.
2. Con el entorno activado y pandas instalado, desde la raíz del repo, corre **los tres** scripts en este orden. Si solo corres el primero, las colonias se quedan sin zona:

```text
python db/catalogos/preparar_catalogo.py
python db/catalogos/asignar_zonas.py
python db/catalogos/revisar_zonas.py
```

## Archivos

| Archivo | Contenido |
| --- | --- |
| `colonias_ags.csv` | Una fila por colonia: id_sepomex, codigo_postal, colonia, tipo_asentamiento, zona_id |
| `zonas_por_cp.csv` | Qué zona le toca a cada código postal; es donde se aplica el criterio |
| `zonas.csv` | Las zonas: zona_id, nombre, descripcion |

## Criterio de zonas (decisión del equipo)

- **Quién y cuándo:** Arturo decidió el criterio el 25 de noviembre de 2026. Tadeo lo aplicó a los 108 códigos postales y revisó en el mapa los 13 que quedaban en la frontera entre dos sectores.
- **Opciones evaluadas:** por sector geográfico (zonas que se recorren de corrido), por rangos de código postal (fácil de calcular, pero los números no siguen el mapa) y por volumen (zonas iguales en paquetes, pero con formas que cruzan la ciudad).
- **Criterio elegido:** 5 sectores geográficos. El Centro es lo que queda dentro del primer anillo (Av. Convención de 1914); Norte, Oriente, Sur y Poniente se reparten por los ejes que salen del centro. Cada colonia toma la zona de su código postal.
- **Por qué:** una cuadrilla reparte en colonias vecinas sin cruzar la ciudad, y el código postal viene en la dirección de cada paquete, así que la zona se calcula sola, sin que nadie la elija a mano. Además, la zona es la llave de fragmentación: cada fragmento queda con colonias que se consultan juntas.
- **Resultado:** 531 colonias. Por zona: Centro 48, Norte 128, Oriente 137, Sur 117 y Poniente 101.
- **Ajustes:** el Centro es más chico porque solo cubre el primer anillo. El Campestre se pasó al Poniente para balancear el Norte. El CP 20286 (Barlovento, 16 colonias) pasó del Poniente al Sur porque en el mapa queda al sur. Con eso, entre los cuatro sectores ninguno tiene más del doble de paquetes que otro.
