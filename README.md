# Zonalia

Plataforma para organizar la última milla de un centro de distribución local en la ciudad de Aguascalientes: clasifica por zona los paquetes que llegan al día, los asigna a los repartidores y permite supervisar cada entrega. Proyecto Integrador de 7° semestre, Ingeniería en Sistemas Computacionales, UAA (agosto–diciembre 2026).

> El sistema trabaja solo con datos sintéticos. Ningún dato real de la empresa ni de sus clientes entra al repositorio.

## Tecnologías

| Componente | Tecnología |
| --- | --- |
| Aplicación (Android, web y escritorio) | Flutter / Dart |
| Servicios y API REST | Python 3.12, FastAPI, pandas, Matplotlib |
| Base relacional distribuida | PostgreSQL 16 (fragmentación por zona y replicación primario-secundario) |
| Base analítica | MongoDB 7 |
| Infraestructura | Docker Compose, WireGuard, Nginx (HTTPS), Suricata |
| Integración continua | GitHub Actions: ruff, bandit, pytest, pip-audit, flutter test |

## Arquitectura general

| Nodo | Ubicación | Función |
| --- | --- | --- |
| N1 Servicios | Local | API REST, servidor web e IDS; único punto expuesto por HTTPS |
| N2 Base primaria | Local | PostgreSQL primario con los fragmentos por zona y el directorio de fragmentos |
| N3 Base secundaria | Remoto | Réplica de PostgreSQL; toma el rol de primario si N2 falla |
| N4 Analítica y monitoreo | Remoto | MongoDB y monitoreo de nodos |

Los nodos se comunican por VPN. Las tres plataformas de la app hablan solo con la API por HTTPS.

## Estructura del repositorio

```text
servicios/   API, dominio, datos, análisis y generador (Python)
app/         aplicación Flutter
db/          esquema, procedimientos, triggers, replicación y respaldos
infra/       nginx, vpn, firewall, hardening e IDS
docs/        bitácora de IA, decisiones, base de datos, seguridad y evidencias
compose.yaml despliegue de contenedores (un perfil por nodo)
```

## Instalación y ejecución

_Se completa en el issue #51. Mientras tanto, cada carpeta explica cómo levantar su parte._

1. Copiar `.env.example` a `.env` y llenar los valores (nunca subir `.env`).
2. Levantar los servicios de un nodo: `docker compose --profile <n1|n2|n3|n4|local> up -d`.

## Integrantes y responsabilidades

Cada integrante es responsable principal de un componente, que defiende de forma individual.

| Integrante | Usuario de GitHub | Componente principal |
| --- | --- | --- |
| José Arturo Picazo Zaragoza | @PicazoArturo | Base de datos distribuida e infraestructura; coordinación del proyecto |
| Hugo Vázquez Hernandez | @Huguiti080 | Auditoría y detección de intrusos |


_Jesús, Hugo y Tadeo agregan su fila en los issues #2, #3 y #4._

## Cómo trabajamos

Todo cambio entra a `main` por pull request revisado por otro integrante. El flujo completo está en [CONTRIBUTING.md](CONTRIBUTING.md). El uso de IA se registra en [docs/bitacora-ia.md](docs/bitacora-ia.md) y las decisiones de diseño en [docs/decisiones/](docs/decisiones/).
