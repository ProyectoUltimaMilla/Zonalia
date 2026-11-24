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
