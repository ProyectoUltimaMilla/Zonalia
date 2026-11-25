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

## 4. La IA como factor de riesgo

## 5. Resumen por pilar

### Confidencialidad

### Integridad

### Disponibilidad

## 6. Riesgos aceptados