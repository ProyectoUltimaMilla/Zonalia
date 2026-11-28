import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:zonalia/app.dart';
import 'package:zonalia/estado/sesion.dart';

Future<void> abrirConAncho(WidgetTester tester, double ancho) async {
  tester.view.physicalSize = Size(ancho, 800);
  tester.view.devicePixelRatio = 1;
  addTearDown(tester.view.reset);
  await tester.pumpWidget(
    ChangeNotifierProvider(
      create: (_) => Sesion()..iniciar('token-de-prueba', 'admin'),
      child: const ZonaliaApp(),
    ),
  );
}

void main() {
  testWidgets('En teléfono usa la navegación inferior', (tester) async {
    await abrirConAncho(tester, 400);
    expect(find.byType(NavigationBar), findsOneWidget);
    expect(find.byType(NavigationRail), findsNothing);
  });

  testWidgets('En escritorio y web usa el riel lateral', (tester) async {
    await abrirConAncho(tester, 1000);
    expect(find.byType(NavigationRail), findsOneWidget);
    expect(find.byType(NavigationBar), findsNothing);
  });

  testWidgets('Tocar una sección cambia el contenido', (tester) async {
    await abrirConAncho(tester, 400);
    await tester.tap(find.widgetWithText(NavigationDestination, 'Reportes'));
    await tester.pumpAndSettle();
    expect(find.text('Entregas y fallas por zona'), findsOneWidget);
  });
}
