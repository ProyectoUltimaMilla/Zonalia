import 'cliente_api.dart';

/// Resultado de un inicio de sesión correcto.
class Credenciales {
  const Credenciales(this.token, this.rol);

  final String token;
  final String rol;
}

/// Habla con POST /auth/login de la API (#13).
class ServicioAuth {
  ServicioAuth([ClienteApi? api]) : _api = api ?? ClienteApi();

  final ClienteApi _api;

  Future<Credenciales> iniciarSesion(String usuario, String contrasena) async {
    final datos = await _api.post('/auth/login', {
      'nombre_usuario': usuario,
      'contrasena': contrasena,
    });
    return Credenciales(
      datos['access_token'] as String,
      datos['rol'] as String,
    );
  }
}
