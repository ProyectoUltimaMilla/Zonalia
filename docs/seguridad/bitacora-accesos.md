
# Bitácora de accesos de la API

Cómo registra Zonalia quién usa la API, qué pidió y con qué resultado (lineamientos IV-d4, issue #16). El código está en `servicios/src/zonalia/api/bitacora_accesos.py` y sus pruebas en `servicios/tests/test_bitacora_accesos.py`.

## Qué se registra

Cada petición deja **una línea JSON**, que se puede leer con cualquier herramienta o cargar a MongoDB para analizarla (#29):

```json
{"hora": "2026-11-25T18:04:11+00:00", "evento": "peticion", "usuario_id": 1, "usuario": "super1", "rol": "supervisor", "metodo": "GET", "ruta": "/auth/yo", "ip": "10.10.0.9", "codigo": 200, "duracion_ms": 3.2}
```

| Campo | Qué es |
| --- | --- |
| `hora` | Fecha y hora en UTC |
| `evento` | `peticion`, o `login_fallido` cuando un inicio de sesión no pasa |
| `usuario_id`, `usuario`, `rol` | Quién hizo la petición, según su token. Vacíos si no mandó token |
| `metodo`, `ruta` | Qué pidió. La ruta va sin los parámetros de la URL |
| `ip` | Desde dónde. Detrás de Nginx sale del encabezado `X-Real-IP` |
| `codigo` | El código HTTP de la respuesta |
| `duracion_ms` | Cuánto tardó la API en responder |
| `usuario_intentado` | Solo en `login_fallido`: el nombre de usuario que se intentó |

Las respuestas 401 y 403 se registran con nivel `WARNING`, para encontrarlas rápido. Un error del servidor se registra con nivel `ERROR` y código 500.

## Qué nunca se registra

- Contraseñas, tokens y encabezados completos (`Authorization` incluido).
- El cuerpo de la petición.
- Los parámetros de la URL, porque podrían llevar datos personales.

La prueba `test_nunca_guarda_contrasenas_ni_tokens` verifica que las contraseñas y tokens utilizados durante la prueba no aparezcan en los registros.

## Dónde queda

- Si `BITACORA_ACCESOS_RUTA` tiene una ruta en el `.env`, se escribe en ese archivo.
- Si está vacía, sale por la consola y se ve con `docker compose logs api`.

## Para qué sirve

- Detectar intentos de adivinar contraseñas: muchos `login_fallido` del mismo usuario o de la misma IP en poco tiempo.
- Saber quién hizo un cambio y cuándo, junto con el historial de estados del paquete en la base (#11).
- Dar evidencia al análisis de tráfico (#31) y al hackeo ético (#47).
