# Análisis de riesgos de Zonalia

Análisis de confidencialidad (C), integridad (I) y disponibilidad (D) del sistema. Parte de la tabla de riesgos de la propuesta de la primera entrega y la amplía. Lo elaboró Hugo Vázquez Hernández y lo revisó el equipo.

Fecha: 2026-11-25

## 1. Activos

Lo que hay que proteger y por qué importa.

| ID | Activo | Dónde vive | Por qué importa |
| --- | --- | --- | --- |
| A01 | Datos de destinatarios (nombre, teléfono, dirección) | N2, N3 | Son necesarios para identificar y localizar a los destinatarios. Su exposición podría provocar suplantación de identidad, fraude o vulneración de la información de los clientes. |
| A02 | Contraseñas y tokens de sesión | N2, app | Permiten autenticar a los usuarios. Si alguien los obtiene, podría acceder a cuentas ajenas y realizar operaciones no autorizadas. |
| A03 | Base de datos primaria | N2 | Almacena la información necesaria para la operación del reparto. Su pérdida o alteración interrumpiría el servicio, causaría errores en las entregas y provocaría pérdida de información crítica. |
| A04 | Réplica de la base de datos | N3 | Es una copia de la información del nodo primario. Su falla afectaría la disponibilidad del sistema y la capacidad de recuperación ante desastres. |
| A05 | API REST | N1 | Permite la comunicación entre la aplicación y los servicios del sistema. Si deja de funcionar, el supervisor no puede asignar paquetes y el repartidor no puede consultar su ruta ni confirmar entregas. |
| A06 | Base analítica | N4 | Almacena información para generar reportes y monitorear el sistema. Su alteración podría causar decisiones erróneas, reportes inexactos y pérdida de confianza en la operación. |
| A07 | Evidencias de entrega (foto y ubicación) | N2, app | Permiten comprobar que los paquetes fueron entregados. Su pérdida o modificación podría generar disputas con clientes, fraudes y dificultades para resolver reclamos. |
| A08 | Manifiestos de paquetes (CSV o JSON) | N1 | Contienen la información de los paquetes que deben procesarse. Los errores en estos archivos podrían provocar entregas a destinos incorrectos. |
| A09 | Llaves y certificados (TLS, firma, SSH) | Todos los nodos | Permiten establecer comunicaciones seguras, autenticar componentes y realizar firmas digitales. Si se comprometen, podría haber intercepción de comunicaciones, suplantación de nodos y falsificación de documentos. |
| A10 | VPN entre nodos | Todos los nodos | Permite la comunicación segura entre los nodos del sistema distribuido. Su interrupción afectaría la sincronización entre nodos, la disponibilidad del servicio y la seguridad de las comunicaciones. |
| A11 | Laptops que funcionan como nodos | Físicas | Un daño al equipo provocaría la caída parcial del sistema, pérdida de datos locales y retrasos en la operación del reparto. |
| A12 | Repositorio en GitHub | GitHub | Almacena el código fuente, la documentación y el historial del proyecto. Una modificación no autorizada podría introducir código malicioso. |
| A13 | Ubicación en tiempo real del repartidor | App, N2 | Su exposición o alteración afecta la privacidad y la seguridad de los repartidores, así como la precisión de la asignación de entregas. |

## 2. Escala

Probabilidad e impacto de 1 a 3. **Nivel = probabilidad × impacto.**

| Valor | Probabilidad | Impacto |
| --- | --- | --- |
| 1 | Requiere conocimientos avanzados y acceso considerable. | Afectación menor que puede solucionarse rápidamente. |
| 2 | Puede ocurrir por conocimientos intermedios o errores comunes. | Afecta la operación de un día o a varios clientes. |
| 3 | Puede ocurrir fácilmente o existen antecedentes en sistemas similares. | Expone datos personales o detiene la operación de reparto. |

| Nivel | Rango | Qué hacemos |
| --- | --- | --- |
| Bajo | 1 a 2 | Aceptar y documentar el riesgo. |
| Medio | 3 a 4 | Implementar una defensa si el calendario lo permite. |
| Alto | 6 a 9 | Implementar una defensa obligatoriamente en esta versión. |

## 3. Tabla de riesgos

| ID | Activo | Pilar | Vulnerabilidad | Amenaza | Prob. | Impacto | Nivel | Defensa | Issue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R01 | A01 | C | Almacenamiento de datos personales sin cifrado | Extracción no autorizada de información de destinatarios | 2 | 3 | 6 alto | Cifrado en reposo y enmascaramiento de datos | #33 |
| R02 | A02 | C | Protección insuficiente de contraseñas y tokens de sesión | Robo de credenciales y suplantación de usuarios | 3 | 3 | 9 alto | Hash seguro de contraseñas, JWT con expiración y control de roles | #13 |
| R03 | A03 | D | Dependencia del nodo primario sin conmutación por falla | Caída del servidor PostgreSQL durante la jornada de reparto | 2 | 3 | 6 alto | Prueba de falla y promoción de la réplica como nuevo primario | #25 |
| R04 | A05 | I | Validación insuficiente de las entradas de la API | Inyección SQL o NoSQL para modificar registros | 3 | 3 | 9 alto | Validación de entradas, consultas parametrizadas y pruebas de inyección | #37 |
| R05 | A07 | I | Ausencia de mecanismos de verificación de integridad | Manipulación de fotografías y evidencias de entrega | 2 | 2 | 4 medio | Firma digital de evidencias de entrega | #27 |
| R06 | A09 | C | Almacenamiento de llaves y secretos dentro del código fuente | Obtención de credenciales y llaves privadas por terceros | 2 | 3 | 6 alto | Gestión de secretos fuera del código fuente | #6 |
| R07 | A10 | C | Comunicación entre nodos sin protección suficiente | Interceptación del tráfico de red por terceros | 2 | 3 | 6 alto | Comunicación mediante VPN WireGuard | #18 |
| R08 | A11 | D | Dependencia de equipos físicos sin respaldos recuperables | Daño físico o falla de una laptop que funciona como nodo | 2 | 3 | 6 alto | Respaldos periódicos y pruebas de recuperación | #39 |
| R09 | A05 | C | Comunicación entre cliente y servidor sin cifrado | Interceptación de información y tokens durante su transmisión | 2 | 3 | 6 alto | Implementación de HTTPS con TLS | #26 |
| R10 | A05 | I | Registro insuficiente de accesos y operaciones | Modificación no autorizada de registros sin trazabilidad | 2 | 2 | 4 medio | Bitácora de accesos y revisión de operaciones | #16 |
| R11 | A05 | D | Monitoreo insuficiente del tráfico de red | Saturación de los servicios mediante tráfico malicioso | 2 | 3 | 6 alto | Detección de intrusiones mediante Suricata y respuesta ante alertas | #24 |
| R12 | A11 | C | Exposición innecesaria de servicios y puertos de administración | Acceso no autorizado a información almacenada en los nodos | 2 | 3 | 6 alto | Firewall, autenticación SSH con llaves y hardening | #34 |
| R13 | A05 | I | Vulnerabilidades de autorización no identificadas | Modificación de paquetes por usuarios sin los permisos correspondientes | 2 | 2 | 4 medio | Pruebas de hackeo ético y corrección de vulnerabilidades identificadas | #47 |
| R14 | A12 | I | Incorporación de dependencias sugeridas por IA sin verificar su procedencia | Introducción de paquetes maliciosos al proyecto | 1 | 3 | 3 medio | Verificación de dependencias en PyPI y auditoría mediante pip-audit | #48 |
| R15 | A12 | C | Inclusión de secretos o datos sensibles en consultas a herramientas de IA | Divulgación de credenciales o información confidencial | 2 | 3 | 6 alto | Uso exclusivo de datos sintéticos y prohibición de compartir secretos con IA según CONTRIBUTING.md | #6 |
| R16 | A12 | I | Incorporación de código generado por IA sin revisión humana | Introducción de código con vulnerabilidades de seguridad | 2 | 3 | 6 alto | Revisión obligatoria mediante PR y análisis estático con Bandit | #8 |

## 4. La IA como factor de riesgo

El uso de herramientas de inteligencia artificial durante el desarrollo de Zonalia puede afectar la seguridad, la calidad y la confidencialidad del sistema y de su código fuente.

Los principales escenarios son la generación de código inseguro o con licencias incompatibles, y la exposición de información sensible o propietaria en las consultas a herramientas de IA. Corresponden a los riesgos R16, R14 y R15.

Para reducir estos riesgos, el equipo contempla usar sólo herramientas de IA aprobadas, revisar obligatoriamente el código generado, anonimizar los datos antes de enviarlos a servicios externos y documentar el origen de las sugerencias utilizadas.

El código y las sugerencias generados con IA deben ser revisados, validados y probados por un miembro del equipo antes de integrarse al repositorio, según las reglas de CONTRIBUTING.md.

## 5. Resumen por pilar

Los riesgos de confidencialidad (R02) e integridad (R04) tienen el nivel más alto, 9 cada uno, con probabilidad 3 e impacto 3. El de disponibilidad (R03) queda en 6, con probabilidad 2 e impacto 3.

En confidencialidad, la consecuencia principal es el robo de cuentas y de datos personales. La defensa combina Argon2 para el almacenamiento de contraseñas, JWT y un esquema de roles, y se vincula con el issue #13.

En integridad, el riesgo es la alteración de paquetes, rutas y entregas. Se propone validar las entradas y usar consultas parametrizadas, lo que se rastrea en el issue #37.

En disponibilidad, el riesgo es la interrupción de asignaciones y consultas. La medida es promover la réplica, documentada en el issue #25. Todavía no hay mediciones de tiempo de recuperación, así que no conviene citar ninguna cifra hasta medirla.

Como la matriz asigna el mismo impacto a los tres riesgos, la priorización depende sobre todo de la probabilidad. Por eso R02 y R04 deberían atenderse primero. Antes de cerrar el análisis, el equipo debe confirmar que estas conclusiones coinciden con su criterio.

## 6. Riesgos aceptados

El análisis no identificó riesgos de nivel bajo que el equipo pueda aceptar sin aplicar medidas. De los 16 riesgos identificados, 12 son altos y 4 son medios.

Los riesgos altos tienen prioridad de tratamiento por su impacto potencial sobre la confidencialidad, la integridad y la disponibilidad de Zonalia. Los riesgos medios se atenderán según el calendario del proyecto.

Una vez implementadas y verificadas las defensas, el equipo hará una nueva evaluación para determinar si los riesgos residuales pueden aceptarse.