# Marco legal de Zonalia

## 1. Qué datos personales trata Zonalia

Zonalia trata datos del destinatario, del personal que opera el sistema y de las evidencias de entrega. El hash de contraseña es información de autenticación que requiere protección, aunque no es un dato personal sensible en sentido jurídico. La bitácora de accesos (#16) ya está implementada y probada; su integración con el resto de la API está pendiente de confirmar.

Los datos del destinatario se guardan en una tabla aparte porque pertenecen a una persona externa a la operación, que no usa el sistema y no puede controlar cómo se manejan.

| Titular | Datos tratados | Tipo de dato | Tabla o fuente | Finalidad del tratamiento |
| --- | --- | --- | --- | --- |
| Destinatario | Nombre, teléfono, calle y número, referencias | Identificación y domicilio | `destinatario` | Identificar a quién se entrega y ubicar el domicilio |
| Destinatario (indirecto) | Número de guía | Identificable si se vincula al destinatario | `paquete` | Localizar el paquete durante el reparto |
| Administrador, supervisor y repartidor | Nombre, usuario, rol, estado activo | Identificación | `usuario` | Asignar permisos y controlar el acceso |
| Administrador, supervisor y repartidor | Hash de contraseña | Autenticación | `usuario` | Verificar la identidad al iniciar sesión |
| Repartidor | Zona y capacidad diaria | Dato laboral | `repartidor` | Asignar paquetes por zona y respetar su capacidad |
| Repartidor | Rutas, fechas y orden de entrega | Actividad laboral | `ruta`, `asignacion` | Organizar la jornada y medir la carga |
| Repartidor y destinatario | Coordenadas, foto y firma | Ubicación, imagen | `entrega` | Comprobar la entrega y atender reclamaciones |
| Usuarios de la API | Usuario, IP y actividad | Identificador en línea | Bitácora (#16) | Registrar accesos y cambios |

Los catálogos de colonias, códigos postales y zonas no son datos personales.

## 2. Ley que aplica y quién es el responsable

La ley aplicable es la Ley Federal de Protección de Datos Personales en Posesión de los Particulares, publicada el 20 de marzo de 2025 y en vigor desde el 21 de marzo de 2025. La reforma del 14 de noviembre de 2025 sólo modificó el artículo 4.

El responsable es quien decide para qué se usan los datos (artículo 2, fracción XIV). En la operación real sería la empresa de reparto que opera el centro. Si un proveedor, como una nube, procesa los datos por su cuenta, es persona encargada (fracción XII). La vigilancia corresponde a la Secretaría Anticorrupción y Buen Gobierno (fracción XV).

## 3. Principios y cómo los cumple Zonalia

La ley exige ocho principios: licitud, finalidad, lealtad, consentimiento, calidad, proporcionalidad, información y responsabilidad (artículo 5). En Zonalia, la finalidad se cumple porque los datos sólo sirven para entregar paquetes (artículo 11). La proporcionalidad se cumple con la separación del destinatario, porque la asignación no necesita nombre ni dirección (artículo 12). La calidad se atiende validando direcciones contra el catálogo de SEPOMEX (artículo 10).

El consentimiento sigue pendiente: por regla general es tácito si el aviso está disponible (artículo 7). Los datos actuales no son sensibles, así que no requieren consentimiento expreso por escrito (artículo 8).

## 4. Aviso de privacidad

El aviso de privacidad informa al titular qué datos se tratan, para qué y cómo ejercer sus derechos (artículos 14 y 15). En Zonalia aún no existe. Debe estar disponible antes de cualquier prueba con datos reales y presentarse a los repartidores al crear su cuenta. Para el destinatario, el aviso debe llegar por la vía en que la empresa recibe sus datos (artículo 17).

## 5. Minimización y conservación

Sólo deben tratarse los datos necesarios para la finalidad (artículo 12). Cuando ya no hacen falta, se bloquean y después se suprimen (artículos 10 y 24). La ley no fija un plazo único; Zonalia aún no define los suyos. Una propuesta es suprimir los datos del destinatario una vez entregado el paquete y vencido el plazo de reclamaciones, y definir un plazo propio para la bitácora. La empresa debe aprobar esos plazos.

## 6. Derechos ARCO

El titular puede acceder a sus datos (artículo 22), rectificarlos (artículo 23), cancelarlos (artículo 24) y oponerse a su tratamiento (artículo 26). El ejercicio es gratuito (artículo 34). El responsable tiene 20 días para responder y 15 más para hacerlo efectivo (artículo 31). Zonalia debe permitir localizar los datos de una persona por nombre, teléfono o guía, y corregir o suprimir un registro sin afectar a otros.

## 7. La ubicación del repartidor como dato personal

Las coordenadas de entrega y el registro de ubicación previsto en MongoDB permiten saber dónde está una persona identificable (artículo 2, fracción V). Un rastreo continuo puede revelar hábitos o el domicilio del repartidor, lo que podría generar un riesgo grave (artículo 2, fracción VI).

Por proporcionalidad (artículo 12), la ubicación debería capturarse sólo al confirmar cada entrega. El repartidor debe saber que se registra (artículo 6). La base laboral del artículo 9, fracción IV, cubre el registro de la entrega, pero no es claro que cubra un rastreo continuo; ese punto debe discutirse con la empresa.

## 8. Seguridad de los datos y vulneraciones

El responsable debe mantener medidas de seguridad administrativas, técnicas y físicas (artículo 18). En Zonalia, las administrativas son los roles y las políticas; las técnicas son el cifrado, el hash de contraseñas, los tokens con vencimiento y la validación de entradas; las físicas son el control de acceso a los servidores. Algunas siguen planeadas y deben marcarse así en el documento final.

Si una vulneración afecta de forma significativa los derechos de los titulares, debe informarse de inmediato (artículo 19). Vulnerar la seguridad por causa imputable al responsable es una infracción (artículo 58, fracción XI). Quien, con ánimo de lucro, provoque una vulneración puede enfrentar de tres meses a tres años de prisión (artículo 62).

## 9. Datos sintéticos en este proyecto

La ley aplica sólo a datos de personas identificadas o identificables (artículo 2, fracción V). Los registros sintéticos sin relación con personas reales quedan fuera. Hay que evitar que un nombre o teléfono generado coincida con una persona real, y no mezclar datos reales en las pruebas. Las colonias pueden ser reales porque provienen del catálogo público de SEPOMEX. El proyecto no debe compartir datos reales con herramientas de IA.