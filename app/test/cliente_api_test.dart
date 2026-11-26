import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:zonalia/core/api/cliente_api.dart';

void main() {
  test('Manda el token y devuelve el JSON', () async {
    late http.Request recibida;
    final api = ClienteApi(
      cliente: MockClient((peticion) async {
        recibida = peticion;
        return http.Response(jsonEncode({'estado': 'ok'}), 200);
      }),
      base: 'http://api',
    )..token = 'abc';

    final datos = await api.get('/health');

    expect(datos['estado'], 'ok');
    expect(recibida.headers['Authorization'], 'Bearer abc');
  });

  test('Un 401 se convierte en un mensaje de sesión', () async {
    final api = ClienteApi(
      cliente: MockClient((_) async => http.Response('{"detail":"x"}', 401)),
      base: 'http://api',
    );

    await expectLater(
      api.get('/auth/yo'),
      throwsA(isA<ErrorApi>().having((e) => e.codigo, 'codigo', 401)),
    );
  });

  test('Sin conexión da un mensaje claro', () async {
    final api = ClienteApi(
      cliente: MockClient((_) async => throw http.ClientException('sin red')),
      base: 'http://api',
    );

    await expectLater(
      api.get('/health'),
      throwsA(isA<ErrorApi>().having((e) => e.codigo, 'codigo', 0)),
    );
  });
}
