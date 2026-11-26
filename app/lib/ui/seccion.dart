import 'package:flutter/material.dart';

/// Una sección de la navegación principal.
class Seccion {
  const Seccion(this.titulo, this.icono, this.descripcion);

  final String titulo;
  final IconData icono;
  final String descripcion;
}

/// Secciones de la app. Cada una tendrá su pantalla en su issue
/// (#40 asignación, #35 ruta del repartidor, #42 reportes, #43 monitoreo).
const List<Seccion> secciones = [
  Seccion('Inicio', Icons.home_outlined, 'Resumen del día'),
  Seccion(
    'Paquetes',
    Icons.inventory_2_outlined,
    'Paquetes recibidos y por asignar',
  ),
  Seccion('Rutas', Icons.route_outlined, 'Rutas de los repartidores'),
  Seccion('Reportes', Icons.bar_chart_outlined, 'Entregas y fallas por zona'),
];
