import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AuthState {
  const AuthState({required this.token, required this.email, required this.role});

  final String? token;
  final String? email;
  final String? role;

  bool get isLoggedIn => token != null && token!.isNotEmpty;
}

class AuthController extends StateNotifier<AuthState> {
  AuthController() : super(const AuthState(token: null, email: null, role: null)) {
    _load();
  }

  static const _tokenKey = 'umu_token';
  static const _emailKey = 'umu_email';
  static const _roleKey = 'umu_role';

  Future<void> _load() async {
    final prefs = await SharedPreferences.getInstance();
    state = AuthState(
      token: prefs.getString(_tokenKey),
      email: prefs.getString(_emailKey),
      role: prefs.getString(_roleKey),
    );
  }

  Future<void> setSession({required String token, required String email, required String role}) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tokenKey, token);
    await prefs.setString(_emailKey, email);
    await prefs.setString(_roleKey, role);
    state = AuthState(token: token, email: email, role: role);
  }

  Future<void> signOut() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
    await prefs.remove(_emailKey);
    await prefs.remove(_roleKey);
    state = const AuthState(token: null, email: null, role: null);
  }
}

final authControllerProvider = StateNotifierProvider<AuthController, AuthState>((ref) {
  return AuthController();
});

