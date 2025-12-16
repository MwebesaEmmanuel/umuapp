import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'tabs/dash.dart';
import 'tabs/more.dart';
import 'tabs/offices.dart';

class VisitorPage extends StatefulWidget {
  const VisitorPage({super.key});

  @override
  State<VisitorPage> createState() => _VisitorPageState();
}

class _VisitorPageState extends State<VisitorPage> {
  int _index = 0;

  @override
  Widget build(BuildContext context) {
    final pages = const [DashTab(visitorMode: true), OfficesTab(visitorMode: true), MoreTab(visitorMode: true)];
    return Scaffold(
      appBar: AppBar(
        title: const Text('Visitor mode'),
        actions: [TextButton(onPressed: () => context.go('/login'), child: const Text('Sign in'))],
      ),
      body: SafeArea(child: pages[_index]),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (i) => setState(() => _index = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.dashboard_outlined), selectedIcon: Icon(Icons.dashboard), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.map_outlined), selectedIcon: Icon(Icons.map), label: 'Campus'),
          NavigationDestination(icon: Icon(Icons.more_horiz), label: 'More'),
        ],
      ),
    );
  }
}

