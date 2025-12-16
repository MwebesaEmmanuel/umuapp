import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../state/auth.dart';

class MoreTab extends ConsumerWidget {
  const MoreTab({super.key, this.visitorMode = false});

  final bool visitorMode;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final auth = ref.watch(authControllerProvider);
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Text(
          visitorMode ? 'Explore UMU' : 'More',
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w800),
        ),
        const SizedBox(height: 12),
        Card(
          child: ListTile(
            leading: const Icon(Icons.public),
            title: const Text('University website'),
            subtitle: const Text('www.umu.ac.ug'),
            onTap: () => _open('https://www.umu.ac.ug/'),
          ),
        ),
        Card(
          child: ListTile(
            leading: const Icon(Icons.assignment),
            title: const Text('Online applications'),
            subtitle: const Text('applications.umu.ac.ug'),
            onTap: () => _open('https://applications.umu.ac.ug/'),
          ),
        ),
        Card(
          child: ListTile(
            leading: const Icon(Icons.directions_bus),
            title: const Text('Bus booking & tracking'),
            subtitle: const Text('Coming next (API ready)'),
          ),
        ),
        Card(
          child: ListTile(
            leading: const Icon(Icons.groups),
            title: const Text('Clubs'),
            subtitle: const Text('Join clubs and chat (API ready)'),
          ),
        ),
        const SizedBox(height: 8),
        if (!visitorMode)
          Card(
            child: ListTile(
              leading: const Icon(Icons.logout),
              title: const Text('Sign out'),
              subtitle: Text('${auth.email ?? ''} ${auth.role ?? ''}'.trim()),
              onTap: () => ref.read(authControllerProvider.notifier).signOut(),
            ),
          ),
      ],
    );
  }

  Future<void> _open(String url) async {
    await launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication);
  }
}

