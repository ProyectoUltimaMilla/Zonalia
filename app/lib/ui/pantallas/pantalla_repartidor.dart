import 'package:flutter/material.dart';

import '../boton_cerrar_sesion.dart';

/// Inicio del repartidor. Su ruta del día llega en el #35.
class PantallaRepartidor extends StatelessWidget {
  const PantallaRepartidor({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mi ruta'),
        actions: const [BotonCerrarSesion()],
      ),
      body: const Center(child: Text('Aquí verás tus paquetes del día.')),
    );
  }
}
