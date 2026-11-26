import 'dart:convert';

import 'package:http/http.dart' as http;

/// Dirección de la API. Se cambia al compilar, por ejemplo:
/// flutter run --dart-define=API_URL=https://zonalia.local
const String urlApi = String.fromEnvironment(
  'API_URL',
  defaultValue: 'http://localhost:8080',
);

/// Error que la app le muestra al usuario con un mensaje claro.
/// codigo es el estado HTTP; 0 significa que no hubo conexión.
class ErrorApi implements Exception {
  const ErrorApi(this.codigo, this.mensaje);

  final int codigo;
  final String mensaje;

  @override
  String toString() => 'ErrorApi($codigo): $mensaje';
}

/// Cliente HTTP de la app: agrega el token y convierte los errores en ErrorApi.
class ClienteApi {
  ClienteApi({http.Client? cliente, this.base = urlApi})
    : _http = cliente ?? http.Client();

  final http.Client _http;
  final String base;
  String? token;

  Map<String, String> get _encabezados => {
    'Content-Type': 'application/json',
    if (token != null) 'Authorization': 'Bearer $token',
  };

  Future<Map<String, dynamic>> get(String ruta) {
    return _enviar(
      () => _http.get(Uri.parse('$base$ruta'), headers: _encabezados),
    );
  }

  Future<Map<String, dynamic>> post(String ruta, Map<String, dynamic> cuerpo) {
    return _enviar(
      () => _http.post(
        Uri.parse('$base$ruta'),
        headers: _encabezados,
        body: jsonEncode(cuerpo),
      ),
    );
  }

  Future<Map<String, dynamic>> _enviar(
    Future<http.Response> Function() peticion,
  ) async {
    final http.Response respuesta;
    try {
      respuesta = await peticion();
    } on Exception {
      throw const ErrorApi(
        0,
        'No hay conexión con el servidor. Revisa tus datos móviles.',
      );
    }
    final codigo = respuesta.statusCode;
    if (codigo >= 200 && codigo < 300) {
      return jsonDecode(utf8.decode(respuesta.bodyBytes))
          as Map<String, dynamic>;
    }
    throw ErrorApi(codigo, _mensajePara(respuesta));
  }

  String _mensajePara(http.Response respuesta) {
    final codigo = respuesta.statusCode;
    if (codigo == 401) {
      return 'Tu sesión expiró o los datos no son correctos. '
          'Inicia sesión otra vez.';
    }
    if (codigo == 403) {
      return 'Tu rol no tiene permiso para esta acción.';
    }
    if (codigo >= 500) {
      return 'El servidor tuvo un problema. Intenta en un momento.';
    }
    try {
      final datos =
          jsonDecode(utf8.decode(respuesta.bodyBytes)) as Map<String, dynamic>;
      return datos['detail']?.toString() ?? 'La petición no se pudo completar.';
    } on FormatException {
      return 'La petición no se pudo completar.';
    }
  }
}
