# Cómo trabajamos

Todo cambio sigue el mismo ciclo: issue → rama → commits → pull request revisado → integración a `main`.

## 1. Issue

- Cada tarea es un issue con título, descripción, responsable, criterios de terminado y etiquetas.
- Al empezar, muévelo a **En progreso** en el Project y ponle la etiqueta `en-progreso`.
- Si algo te detiene, ponle `bloqueado` y avisa al coordinador.

## 2. Rama

Crea tu rama desde `main` actualizado, con el número del issue:

```bash
git switch main && git pull
git switch -c feature/13-autenticacion
```

Prefijos permitidos: `feature/` (código nuevo, incluida infraestructura), `fix/` (correcciones), `docs/` (documentación) y `test/` (pruebas).

## 3. Commits

Pequeños y descriptivos, a lo largo del día:

```text
feat(api): agrega inicio de sesión con JWT (#13)

Valida usuario y contraseña contra el hash argon2 y devuelve un token
que expira en 8 horas.

IA: asistido
```

- La última línea solo va si se usó IA: `IA: asistido` o `IA: generado y revisado`.
- Nunca subas contraseñas, llaves, certificados, tokens ni datos reales.

## 4. Pull request

- Usa la plantilla y escribe `Closes #<número>` para ligar el issue.
- Pide revisión a la persona indicada en el issue y cambia la etiqueta a `en-revision`.
- Si usaste IA, agrega tu entrada en `docs/bitacora-ia.md` en el mismo PR.
- Ningún PR debe esperar más de 12 horas su revisión.

## 5. Revisión

- La aprobación es de una persona distinta al autor, nunca de una IA.
- El revisor prueba el cambio. Si el autor no puede explicar su PR en dos minutos, no se integra.

## 6. Integración

- Con CI en verde y una aprobación, el autor integra con **Create a merge commit** (no squash ni rebase, para conservar los hashes que anota la bitácora).
- El issue se cierra solo al integrar y pasa a **Hecho**.

## Niveles de uso de IA (apartado V de los lineamientos)

| Etiqueta | Qué incluye | Condición |
| --- | --- | --- |
| `ia-libre` | Plantillas, widgets, configuración inicial, datos sintéticos, documentación, casos de prueba | Entrada breve en la bitácora |
| `ia-verificacion` | Lógica de negocio, SQL y MongoDB, procedimientos y triggers, replicación, firewall, TLS, SSH, VPN, criptografía | Bitácora, pruebas que lo respalden y revisión de otro integrante |
| `ia-decision-equipo` | Fragmentación, shard key, postura CAP, distribución de nodos, análisis de riesgos, marco legal | Lo decide y escribe el equipo; la IA solo puede listar alternativas |

Está prohibido compartir con una IA datos personales reales, contraseñas, llaves o certificados del proyecto.

## Dónde va cada cosa

| Qué entregas | Dónde va | Cómo se llena |
| --- | --- | --- |
| Código Python | `servicios/` | [servicios/README.md](servicios/README.md) |
| App Flutter | `app/` | [app/README.md](app/README.md) |
| SQL de PostgreSQL | `db/` | [db/README.md](db/README.md) |
| Nginx, VPN, firewall, IDS | `infra/` | [infra/README.md](infra/README.md) |
| Uso de IA | `docs/bitacora-ia.md` | Instrucciones al inicio del archivo |
| Decisiones de diseño | `docs/decisiones/` | [docs/decisiones/README.md](docs/decisiones/README.md) |
| Documentos de base de datos | `docs/bd/` | [docs/bd/README.md](docs/bd/README.md) |
| Documentos de seguridad | `docs/seguridad/` | [docs/seguridad/README.md](docs/seguridad/README.md) |
| Capturas y videos | `docs/evidencias/` | [docs/evidencias/README.md](docs/evidencias/README.md) |
| Variables y contraseñas | `.env` (local, nunca se sube) | Copia `.env.example` y llénalo |

Cada carpeta dice qué documento va, quién lo hace y en qué issue. Si algo no encaja en ninguna, pregunta al coordinador antes de crear carpetas nuevas.

## Si trabajas con un asistente de IA

Pídele a tu asistente que lea este archivo, el README de la carpeta donde vas a trabajar y tu issue antes de empezar. Reglas para ti y para él:

- Trabaja solo en la rama de tu issue (`tipo/N-tema`, viene en el issue). Nunca en `main`.
- No crees carpetas ni archivos fuera de lo que pide el issue y el README de la carpeta.
- No agregues coautores de IA ni firmas automáticas al commit o al PR (`Co-Authored-By`, "Generated with…"). El uso de IA se declara solo con la línea `IA: asistido` o `IA: generado y revisado` y con tu fila en la bitácora.
- Nunca pegues en la IA contraseñas, llaves, certificados, el contenido de `.env` ni datos reales (5.2).
- Las decisiones de diseño y las conclusiones las escribes tú (5.2). La IA solo puede proponer alternativas.
- Antes de pedir revisión, tienes que poder explicar tu cambio sin la IA: el profesor elige commits al azar (5.4).
