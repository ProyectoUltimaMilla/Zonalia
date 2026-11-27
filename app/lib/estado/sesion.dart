import 'package:flutter/foundation.dart';

/// Sesión del usuario: token y rol. Todas las pantallas la leen con provider.
/// Guardarla en el dispositivo llega en el #41 (ver ADR-006).
class Sesion extends ChangeNotifier {
  String? _token;
  String? _rol;

  String? get token => _token;
  String? get rol => _rol;
  bool get iniciada => _token != null;

  void iniciar(String token, String rol) {
    _token = token;
    _rol = rol;
    notifyListeners();
  }

  void cerrar() {
    _token = null;
    _rol = null;
    notifyListeners();
  }
}