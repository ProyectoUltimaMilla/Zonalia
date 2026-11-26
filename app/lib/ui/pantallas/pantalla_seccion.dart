import 'package:flutter/material.dart';

import '../seccion.dart';

/// Pantalla base de una sección: icono y descripción.
class PantallaSeccion extends StatelessWidget {
  const PantallaSeccion({super.key, required this.seccion});

  final Seccion seccion;

  @override
  Widget build(BuildContext context) {
    final tema = Theme.of(context);
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(seccion.icono, size: 48, color: tema.colorScheme.primary),
          const SizedBox(height: 12),
          Text(seccion.descripcion, style: tema.textTheme.titleMedium),
        ],
      ),
    );
  }
}
