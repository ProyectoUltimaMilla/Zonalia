import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../estado/sesion.dart';

/// Botón de la barra superior que cierra la sesión y regresa al login.
class BotonCerrarSesion extends StatelessWidget {
  const BotonCerrarSesion({super.key});

  @override
  Widget build(BuildContext context) {
    return IconButton(
      tooltip: 'Cerrar sesión',
      icon: const Icon(Icons.logout),
      onPressed: () => context.read<Sesion>().cerrar(),
    );
  }
}
