# Seguridad

Documentación de seguridad del sistema (lineamientos IV-d). Las configuraciones viven en `infra/`; aquí va el análisis y la evidencia.

| Documento (nombre sugerido) | Contenido | Lineamiento | Issue | Responsable |
| --- | --- | --- | --- | --- |
| `riesgos.md` | Tríada CIA: activos, vulnerabilidades, amenazas, defensas, incluida la IA como riesgo | IV-d1 | #10 | Hugo |
| `marco-legal.md` | Leyes aplicables a los datos personales del sistema | Entrega 2 | #17 | Hugo |
| `bitacora-accesos.md` | Cómo se registran los accesos a la API | IV-d4 | #16 | Hugo |
| `trafico.md` | Análisis de tráfico (Wireshark o tcpdump) y bitácora de uso de red | IV-d4, d6 | #31 | Hugo |
| `inyeccion.md` | Pruebas de inyección SQL y NoSQL | IV-e3 | #37 | Hugo |
| `hackeo-etico.md` | nmap / OWASP ZAP: qué se encontró y qué se corrigió | IV-d7 | #47 | Hugo |
| `dependencias.md` | Resultado de pip-audit y verificación de paquetes | IV-f3 | #48 | Tadeo |
| `controles.md` | Resumen de controles: TLS, SSH, VPN, firewall, hardening, IDS, criptografía | IV-d2, d3, d5, d6 | #18, #26, #34, #24 | Arturo y Hugo |

## Cómo se entrega

- **Nivel de IA:** el análisis de riesgos y el marco legal son decisión del equipo; la IA solo puede listar ideas y no redacta conclusiones (5.2).
- **Prohibido subir:** contraseñas, llaves ni certificados reales. En los documentos se usan valores de ejemplo.
- **Capturas:** las que respalden cada documento van en `docs/evidencias/`.
