import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/api/cliente_api.dart';
import '../../core/api/servicio_auth.dart';
import '../../estado/sesion.dart';

/// Pantalla de inicio de sesión (#23). Valida, muestra la carga y los errores,
/// y al entrar guarda el token y el rol en la Sesion; app.dart decide qué abrir.
class PantallaLogin extends StatefulWidget {
  const PantallaLogin({super.key, this.servicio});

  /// Las pruebas pasan un servicio con un cliente falso.
  final ServicioAuth? servicio;

  @override
  State<PantallaLogin> createState() => _PantallaLoginState();
}

class _PantallaLoginState extends State<PantallaLogin> {
  final _formulario = GlobalKey<FormState>();
  final _usuario = TextEditingController();
  final _contrasena = TextEditingController();
  late final ServicioAuth _servicio = widget.servicio ?? ServicioAuth();
  bool _cargando = false;
  bool _ocultar = true;
  String? _error;

  @override
  void dispose() {
    _usuario.dispose();
    _contrasena.dispose();
    super.dispose();
  }

  Future<void> _entrar() async {
    if (!_formulario.currentState!.validate()) return;
    setState(() {
      _cargando = true;
      _error = null;
    });
    try {
      final credenciales = await _servicio.iniciarSesion(
        _usuario.text.trim(),
        _contrasena.text,
      );
      if (!mounted) return;
      context.read<Sesion>().iniciar(credenciales.token, credenciales.rol);
    } on ErrorApi catch (error) {
      _error = error.codigo == 401
          ? 'Usuario o contraseña incorrectos.'
          : error.mensaje;
    } finally {
      if (mounted) setState(() => _cargando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final tema = Theme.of(context);
    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 400),
            child: Form(
              key: _formulario,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Icon(
                    Icons.local_shipping_outlined,
                    size: 64,
                    color: tema.colorScheme.primary,
                  ),
                  const SizedBox(height: 12),
                  Text(
                    'Zonalia',
                    textAlign: TextAlign.center,
                    style: tema.textTheme.headlineMedium,
                  ),
                  const SizedBox(height: 32),
                  TextFormField(
                    key: const Key('campo_usuario'),
                    controller: _usuario,
                    enabled: !_cargando,
                    textInputAction: TextInputAction.next,
                    autofillHints: const [AutofillHints.username],
                    decoration: const InputDecoration(
                      labelText: 'Usuario',
                      prefixIcon: Icon(Icons.person_outline),
                      border: OutlineInputBorder(),
                    ),
                    validator: validarUsuario,
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    key: const Key('campo_contrasena'),
                    controller: _contrasena,
                    enabled: !_cargando,
                    obscureText: _ocultar,
                    autofillHints: const [AutofillHints.password],
                    onFieldSubmitted: (_) => _entrar(),
                    decoration: InputDecoration(
                      labelText: 'Contraseña',
                      prefixIcon: const Icon(Icons.lock_outline),
                      border: const OutlineInputBorder(),
                      suffixIcon: IconButton(
                        tooltip: _ocultar ? 'Mostrar' : 'Ocultar',
                        icon: Icon(
                          _ocultar ? Icons.visibility : Icons.visibility_off,
                        ),
                        onPressed: () => setState(() => _ocultar = !_ocultar),
                      ),
                    ),
                    validator: validarContrasena,
                  ),
                  if (_error != null) ...[
                    const SizedBox(height: 16),
                    Text(
                      _error!,
                      key: const Key('mensaje_error'),
                      style: TextStyle(color: tema.colorScheme.error),
                      textAlign: TextAlign.center,
                    ),
                  ],
                  const SizedBox(height: 24),
                  FilledButton(
                    key: const Key('boton_entrar'),
                    onPressed: _cargando ? null : _entrar,
                    child: _cargando
                        ? const SizedBox(
                            height: 20,
                            width: 20,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Text('Entrar'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

/// El usuario es el nombre de usuario de la API (#13), por ejemplo supervisor1 o rep01.
String? validarUsuario(String? valor) {
  final texto = valor?.trim() ?? '';
  if (texto.isEmpty) return 'Escribe tu usuario';
  if (texto.contains(' ')) return 'El usuario no lleva espacios';
  return null;
}

String? validarContrasena(String? valor) {
  if (valor == null || valor.isEmpty) return 'Escribe tu contraseña';
  if (valor.length < 6) return 'La contraseña tiene al menos 6 caracteres';
  return null;
}
