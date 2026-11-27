import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'app.dart';
import 'estado/sesion.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (_) => Sesion(),
      child: const ZonaliaApp(),
    ),
  );
}