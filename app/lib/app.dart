import 'package:flutter/material.dart';

import 'ui/marco_adaptable.dart';

/// Color base de Zonalia. Material 3 arma el resto de la paleta a partir de él.
const Color colorZonalia = Color(0xFF00695C);

class ZonaliaApp extends StatelessWidget {
  const ZonaliaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Zonalia',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: colorZonalia),
        useMaterial3: true,
      ),
      darkTheme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: colorZonalia,
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      home: const MarcoAdaptable(),
    );
  }
}