import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../api/client.dart';

final linksProvider = FutureProvider<List<Map<String, dynamic>>>((ref) async {
  final dio = ref.watch(dioProvider);
  final resp = await dio.get<List<dynamic>>('/public/links');
  return (resp.data ?? []).cast<Map<String, dynamic>>();
});

final announcementsProvider = FutureProvider<List<Map<String, dynamic>>>((ref) async {
  final dio = ref.watch(dioProvider);
  final resp = await dio.get<List<dynamic>>('/content/announcements');
  return (resp.data ?? []).cast<Map<String, dynamic>>();
});

class DashTab extends ConsumerWidget {
  const DashTab({super.key, this.visitorMode = false});

  final bool visitorMode;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = Theme.of(context);
    final links = ref.watch(linksProvider);
    final announcements = ref.watch(announcementsProvider);

    return CustomScrollView(
      slivers: [
        SliverAppBar(
          pinned: true,
          title: Text(visitorMode ? 'UMU (Visitor)' : 'UMU'),
          actions: [
            IconButton(
              onPressed: () {
                ref.invalidate(linksProvider);
                ref.invalidate(announcementsProvider);
              },
              icon: const Icon(Icons.refresh),
            ),
          ],
        ),
        SliverPadding(
          padding: const EdgeInsets.all(16),
          sliver: SliverList(
            delegate: SliverChildListDelegate.fixed(
              [
                Text('Quick links', style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800)),
                const SizedBox(height: 10),
                links.when(
                  data: (items) => _Links(items: items),
                  loading: () => const LinearProgressIndicator(),
                  error: (e, _) => Text('Links error: $e'),
                ),
                const SizedBox(height: 18),
                Text('Announcements', style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800)),
                const SizedBox(height: 10),
                announcements.when(
                  data: (items) => _Announcements(items: items),
                  loading: () => const LinearProgressIndicator(),
                  error: (e, _) => Text('Announcements error: $e'),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class _Links extends StatelessWidget {
  const _Links({required this.items});

  final List<Map<String, dynamic>> items;

  @override
  Widget build(BuildContext context) {
    if (items.isEmpty) return const Text('No links yet');
    return Wrap(
      spacing: 10,
      runSpacing: 10,
      children: items.take(6).map((it) {
        final title = (it['title'] as String?) ?? 'Link';
        final url = (it['url'] as String?) ?? '';
        return FilledButton.tonalIcon(
          onPressed: url.isEmpty ? null : () => launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication),
          icon: const Icon(Icons.link),
          label: Text(title, overflow: TextOverflow.ellipsis),
        );
      }).toList(),
    );
  }
}

class _Announcements extends StatelessWidget {
  const _Announcements({required this.items});

  final List<Map<String, dynamic>> items;

  @override
  Widget build(BuildContext context) {
    if (items.isEmpty) return const Text('No announcements yet');
    return Column(
      children: items.take(8).map((it) {
        return Card(
          child: ListTile(
            title: Text((it['title'] as String?) ?? ''),
            subtitle: Text(
              (it['body'] as String?) ?? '',
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        );
      }).toList(),
    );
  }
}

