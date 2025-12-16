import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../api/auth_api.dart';
import '../api/client.dart';
import '../state/auth.dart';

final _authApiProvider = Provider<AuthApi>((ref) => AuthApi(ref.watch(dioProvider)));

class LoginPage extends ConsumerStatefulWidget {
  const LoginPage({super.key});

  @override
  ConsumerState<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends ConsumerState<LoginPage> {
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
      final token = await api.login(email: _email.text.trim(), password: _password.text);
      final me = await api.me();
      await ref.read(authControllerProvider.notifier).setSession(
            token: token,
            email: (me['email'] as String?) ?? _email.text.trim(),
            role: (me['role'] as String?) ?? 'student',
          );
      if (mounted) context.go('/home');
    } on DioException catch (e) {
      setState(() => _error = e.response?.data.toString() ?? e.message);
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
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            const SizedBox(height: 18),
            Text('UMU App', style: theme.textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.w800)),
            const SizedBox(height: 6),
            Text('Students • Staff • Admins • Visitors', style: theme.textTheme.bodyMedium),
            const SizedBox(height: 26),
            TextField(
              controller: _email,
              keyboardType: TextInputType.emailAddress,
              decoration: const InputDecoration(
                labelText: 'University email',
                hintText: 'jane.sam@stud.umu.ac.ug',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _password,
              obscureText: true,
              decoration: const InputDecoration(labelText: 'Password', border: OutlineInputBorder()),
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
                  : const Text('Sign in'),
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                TextButton(onPressed: () => context.go('/register'), child: const Text('Create account')),
                const Spacer(),
                TextButton(onPressed: () => context.go('/visitor'), child: const Text('Continue as visitor')),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

