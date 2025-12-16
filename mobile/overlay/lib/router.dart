import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'pages/home.dart';
import 'pages/login.dart';
import 'pages/register.dart';
import 'pages/visitor.dart';
import 'state/auth.dart';

final appRouterProvider = Provider<GoRouter>((ref) {
  final auth = ref.watch(authControllerProvider);

  return GoRouter(
    initialLocation: '/home',
    redirect: (context, state) {
      final loc = state.matchedLocation;
      final isAuthRoute = loc == '/login' || loc == '/register';
      final isVisitor = loc.startsWith('/visitor');

      if (!auth.isLoggedIn && !isAuthRoute && !isVisitor) return '/login';
      if (auth.isLoggedIn && isAuthRoute) return '/home';
      return null;
    },
    routes: [
      GoRoute(path: '/login', builder: (_, __) => const LoginPage()),
      GoRoute(path: '/register', builder: (_, __) => const RegisterPage()),
      GoRoute(path: '/visitor', builder: (_, __) => const VisitorPage()),
      GoRoute(path: '/home', builder: (_, __) => const HomePage()),
    ],
  );
});

