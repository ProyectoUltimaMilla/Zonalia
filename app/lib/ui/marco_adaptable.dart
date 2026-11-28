import 'package:flutter/material.dart';

import 'boton_cerrar_sesion.dart';

import 'pantallas/pantalla_seccion.dart';
import 'seccion.dart';

/// Ancho a partir del cual se usa el riel lateral (tabletas, escritorio y web).
const double anchoRiel = 600;

/// Marco de la app: navegación inferior en teléfono y riel lateral en pantallas anchas.
class MarcoAdaptable extends StatefulWidget {
  const MarcoAdaptable({super.key});

  @override
  State<MarcoAdaptable> createState() => _MarcoAdaptableState();
}

class _MarcoAdaptableState extends State<MarcoAdaptable> {
  int _indice = 0;

  void _cambiar(int indice) {
    setState(() => _indice = indice);
  }

  @override
  Widget build(BuildContext context) {
    final seccion = secciones[_indice];
    final contenido = PantallaSeccion(seccion: seccion);
    final ancho = MediaQuery.sizeOf(context).width;

    if (ancho < anchoRiel) {
      return Scaffold(
        appBar: AppBar(
          title: Text(seccion.titulo),
          actions: const [BotonCerrarSesion()],
        ),
        body: contenido,
        bottomNavigationBar: NavigationBar(
          selectedIndex: _indice,
          onDestinationSelected: _cambiar,
          destinations: [
            for (final s in secciones)
              NavigationDestination(icon: Icon(s.icono), label: s.titulo),
          ],
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(seccion.titulo),
        actions: const [BotonCerrarSesion()],
      ),
      body: Row(
        children: [
          NavigationRail(
            selectedIndex: _indice,
            onDestinationSelected: _cambiar,
            labelType: NavigationRailLabelType.all,
            destinations: [
              for (final s in secciones)
                NavigationRailDestination(
                  icon: Icon(s.icono),
                  label: Text(s.titulo),
                ),
            ],
          ),
          const VerticalDivider(width: 1),
          Expanded(child: contenido),
        ],
      ),
    );
  }
}
