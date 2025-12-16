import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../api/auth_api.dart';
import '../api/client.dart';
import '../config.dart';
import '../state/auth.dart';

final _authApiProvider = Provider<AuthApi>((ref) => AuthApi(ref.watch(dioProvider)));

class RegisterPage extends ConsumerStatefulWidget {
  const RegisterPage({super.key});

  @override
  ConsumerState<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends ConsumerState<RegisterPage> {
  final _email = TextEditingController();
  final _password = TextEditingController();
  bool _loading = false;
  String? _error;

  @override
  void dispose() {
    _email.dispose();
    _password.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final api = ref.read(_authApiProvider);
      final token = await api.register(email: _email.text.trim(), password: _password.text);
      final me = await api.me();
      await ref.read(authControllerProvider.notifier).setSession(
            token: token,
            email: (me['email'] as String?) ?? _email.text.trim(),
            role: (me['role'] as String?) ?? 'student',
          );
      if (mounted) context.go('/home');
    } on DioException catch (e) {
      final msg = e.response?.data.toString() ?? e.message ?? e.toString();
      setState(
        () => _error =
            '$msg\n\nIf you are on Web: ensure backend is running on http://localhost:8000 and restart Flutter.',
      );
    } catch (e) {
      setState(() => _error = e.toString());
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Create account')),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            if (kDebugMode)
              Padding(
                padding: const EdgeInsets.only(bottom: 10),
                child: Text('API: ${AppConfig.apiBaseUrl}', style: theme.textTheme.bodySmall),
              ),
            TextField(
              controller: _email,
              keyboardType: TextInputType.emailAddress,
              decoration: const InputDecoration(
                labelText: 'University email',
                hintText: 'emwebesa@umu.ac.ug',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _password,
              obscureText: true,
              decoration: const InputDecoration(
                labelText: 'Password (min 8 chars)',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            if (_error != null) ...[
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: theme.colorScheme.errorContainer,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(_error!, style: TextStyle(color: theme.colorScheme.onErrorContainer)),
              ),
              const SizedBox(height: 12),
            ],
            FilledButton(
              onPressed: _loading ? null : _submit,
              child: _loading
                  ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator())
                  : const Text('Create account'),
            ),
          ],
        ),
      ),
    );
  }
}

