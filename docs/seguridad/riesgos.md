# Análisis de riesgos de Zonalia

Análisis de confidencialidad (C), integridad (I) y disponibilidad (D) del sistema. Parte de la tabla de riesgos de la propuesta de la primera entrega y la amplía. Lo elaboró Hugo Vázquez Hernandez y lo revisó el equipo.

Fecha: 2026-11-25

## 1. Activos

Lo que hay que proteger y por qué importa.

| ID | Activo | Dónde vive | Por qué importa |
| --- | --- | --- | --- |
| A01 | Datos de destinatarios (nombre, teléfono, dirección) | N2, N3 | Son una necesidad para identificar y localizar a los destinatarios. Su exposicion podria provocar suplantación de identidad, fraude o vulneración para la información de los clientes |
| A02 | Contraseñas y tokens de sesión | N2, app |Permiten autenticar a los usuarios del sistema. Si alguien obtiene acceso indebido a ellos, podria acceder a cuentas ajenas, realizar operaciones no autorizadas.  |
| A03 | Base de datos primaria | N2 | Almacena la información necesaria para la operación del reparto. Su perdida o alteración ocasionaria la interrupcion del servicio, errores en las entregas y perdida de información critica |
| A04 | Réplica de la base de datos | N3 |  Tendremos una copia de la información del nodo primario. Su falla afectaria la disponibilidad del sistema y la capacidad de recuperacion ante desastres|
| A05 | API REST | N1 | Permite la comunicación entre la aplicación y los servicios del sistema si deja de funcionar, los usuarios no podrian realizar pedidos, consultar el estado de sus entregas ni comunicarse con los repartidaroes |
| A06 | Base analítica | N4 |Almacena informacion para generar reportes y monitorear el sistema. La alteracion de sus datos podria ocasionar, decisiones erroneas, reportes inexactos y perdida de confianza en la operación.|
| A07 | Evidencias de entrega (foto y ubicación) | N2, app | Permiten comporbar que los paquetes fueron entregados. Su perdida o modificacion podria generar disputas con los clientes, fraudes en las entregas y dificultades para resolver reclamos |
| A08 | Manifiestos de paquetes (CSV o JSON) | N1 |Contienen informacion de los paquetes que deben procesarse. Los errores en estos archivos podrian provocar entregas a destinos incorrectos  |
| A09 | Llaves y certificados (TLS, firma, SSH) | Todos los nodos | Permiten establecer comunicaciones, seguras, autenticar componentes y realizar firmas digitales. si se coompormeten, podria ocurrir intercepcion de comunicaciones, suplantacion de nodos y falsificacion de documentos o transacciones. |
| A10 | VPN entre nodos | Todos los nodos | Permite la comunicación segura entre los nodos del sistema distribuido. Su interrupcion afectaria la sincronizacion entre nodos por lo tanto la disponibilidad del servicio y la seguridad de las comunicaciones |
| A11 | Laptops que funcionan como nodos | Físicas | El daño al equipo provocaria la caida parcial del sistema, perdidad de datos tanto locales y retrassos en la operación del reparto |
| A12 | Repositorio en GitHub | GitHub | Almacena el codigo fuente, la documentación y el historial del proyecto. Una modificacion no autorizada podria ocasionar la introduccion de codigo malicioso |
| A13 | Ubicación en tiempo real del repartidor | App, N2 | La ubicacion y el seguimiento de los repartidores es importante de no tener una exposicion o alteracio ya que afecta la privacidad y segurdidad de los repartidores, asi como la precision de la asignación de entregas.|

## 2. Escala

Probabilidad e impacto de 1 a 3. **Nivel = probabilidad × impacto.**

| Valor | Probabilidad | Impacto |
| --- | --- | --- |
| 1 |Requiere conocimientos avanzados y acceso considerable.  | Afectación menor que puede solucionarse rápidamente. |
| 2 | Puede ocurrir por conocimientos intermedios o errores comunes.| Afecta la operación de un día o a varios clientes. |
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

| R16 |   A12   | Integridad | Incorporación de código generado por IA sin revisión humana. | Introducción de código con vulnerabilidades de seguridad. | Por determinar. | Por determinar | --- | 	Revisión obligatoria mediante PR y análisis estático con Bandit. | 8 |

## 4. La IA como factor de riesgo
El uso de herramientas de inteligencia artificial durante el desarrollo de Zonalia puede representar riesgos para la seguridad, la calidad y la confidencialidad del sistema y de su código fuente.

Los principales escenarios identificados son la generación de código inseguro o con licencias incompatibles, y la exposición de información sensible o propietaria en las consultas realizadas a herramientas de IA, correspondientes a los riesgos R14 y R15 de la tabla de riesgos.

Para reducir estos riesgos, el equipo contempla el uso de herramientas de IA aprobadas, la revisión obligatoria del código generado, la anonimización de datos antes de enviarlos a servicios externos y la documentación del origen de las sugerencias utilizadas.

El código y las sugerencias proporcionadas por IA deberán ser revisados, validados y probados por un miembro del equipo antes de integrarse al repositorio, respetando las reglas establecidas en CONTRIBUTING.md.

## 5. Resumen por pilar

### Confidencialidad
El riesgo de mayor nivel en este pilar es R02, con una puntuación de 9 (alto). Si un atacante roba credenciales, [consecuencia concreta: qué datos o sistemas quedan expuestos]. La probabilidad asignada es [valor] porque [razón], y el impacto es [valor] porque [razón]. Los controles del Issue #13 reducen esta exposición al [cómo lo reducen].

### Integridad
El riesgo de mayor nivel en este pilar es R04, con una puntuación de 9 (alto). Una inyección SQL o NoSQL permitiría [consecuencia concreta: qué datos se leerían o alterarían]. La probabilidad asignada es [valor] porque [razón], y el impacto es [valor] porque [razón]. Los controles del Issue #37 mitigan el riesgo al [cómo lo mitigan].

### Disponibilidad
El riesgo R03 es uno de los de mayor nivel en este pilar, con una puntuación de 6 (alto). Si el servidor primario falla, [consecuencia concreta: tiempo fuera de servicio y efecto en usuarios]. La probabilidad asignada es [valor] porque [razón], y el impacto es [valor] porque [razón]. La defensa del Issue #25 reduce el efecto de una caída al [cómo lo reduce].

## 6. Riesgos aceptados
El análisis no identificó riesgos de nivel bajo que el equipo pueda aceptar sin aplicar medidas de seguridad. De los 15 riesgos identificados, 11 son altos y 4 son medios.

Los riesgos altos tienen prioridad de tratamiento por su impacto potencial sobre la confidencialidad, la integridad y la disponibilidad de Zonalia. Los riesgos medios se atenderán según el calendario de desarrollo del proyecto.

Una vez implementadas y verificadas las defensas, el equipo hará una nueva evaluación para determinar si los riesgos residuales pueden aceptarse.