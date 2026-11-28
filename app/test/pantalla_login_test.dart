import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:provider/provider.dart';
import 'package:zonalia/core/api/cliente_api.dart';
import 'package:zonalia/core/api/servicio_auth.dart';
import 'package:zonalia/estado/sesion.dart';
import 'package:zonalia/ui/pantallas/pantalla_login.dart';

/// Abre el login con una API falsa que responde lo que diga [responder].
Future<Sesion> abrirLogin(
  WidgetTester tester,
  Future<http.Response> Function(http.Request) responder,
) async {
  final sesion = Sesion();
  final servicio = ServicioAuth(
    ClienteApi(cliente: MockClient(responder), base: 'http://api'),
  );
  await tester.pumpWidget(
    ChangeNotifierProvider.value(
      value: sesion,
      child: MaterialApp(home: PantallaLogin(servicio: servicio)),
    ),
  );
  return sesion;
}

Future<void> escribir(WidgetTester tester, String usuario, String clave) async {
  await tester.enterText(find.byKey(const Key('campo_usuario')), usuario);
  await tester.enterText(find.byKey(const Key('campo_contrasena')), clave);
  await tester.tap(find.byKey(const Key('boton_entrar')));
}

void main() {
  testWidgets('Sin datos muestra qué falta y no llama a la API', (
    tester,
  ) async {
    var llamadas = 0;
    await abrirLogin(tester, (_) async {
      llamadas++;
      return http.Response('{}', 200);
    });
    await tester.tap(find.byKey(const Key('boton_entrar')));
    await tester.pump();
    expect(find.text('Escribe tu usuario'), findsOneWidget);
    expect(find.text('Escribe tu contraseña'), findsOneWidget);
    expect(llamadas, 0);
  });

  testWidgets('Muestra la carga y al entrar guarda token y rol', (
    tester,
  ) async {
    final respuesta = Completer<http.Response>();
    late http.Request recibida;
    final sesion = await abrirLogin(tester, (peticion) {
      recibida = peticion;
      return respuesta.future;
    });
    await escribir(tester, 'supervisor1', 'Clave-Demo-1');
    await tester.pump();
    expect(find.byType(CircularProgressIndicator), findsOneWidget);

    respuesta.complete(
      http.Response(
        jsonEncode({
          'access_token': 'abc',
          'token_type': 'bearer',
          'rol': 'supervisor',
        }),
        200,
      ),
    );
    await tester.pumpAndSettle();
    expect(jsonDecode(recibida.body)['nombre_usuario'], 'supervisor1');
    expect(sesion.token, 'abc');
    expect(sesion.rol, 'supervisor');
  });

  testWidgets('Credenciales erróneas dan un mensaje claro', (tester) async {
    final sesion = await abrirLogin(
      tester,
      (_) async =>
          http.Response('{"detail":"Usuario o contraseña incorrectos"}', 401),
    );
    await escribir(tester, 'supervisor1', 'equivocada');
    await tester.pumpAndSettle();
    expect(find.text('Usuario o contraseña incorrectos.'), findsOneWidget);
    expect(sesion.iniciada, isFalse);
  });

  testWidgets('Sin conexión avisa de los datos móviles', (tester) async {
    await abrirLogin(
      tester,
      (_) async => throw http.ClientException('sin red'),
    );
    await escribir(tester, 'rep01', 'Clave-Demo-1');
    await tester.pumpAndSettle();
    expect(find.textContaining('No hay conexión'), findsOneWidget);
  });

  test('Validaciones del formulario', () {
    expect(validarUsuario(' '), 'Escribe tu usuario');
    expect(validarUsuario('rep 01'), 'El usuario no lleva espacios');
    expect(validarUsuario('rep01'), isNull);
    expect(validarContrasena('123'), isNotNull);
    expect(validarContrasena('123456'), isNull);
  });
}
