import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
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

final newsProvider = FutureProvider<List<Map<String, dynamic>>>((ref) async {
  final dio = ref.watch(dioProvider);
  final resp = await dio.get<List<dynamic>>('/public/news', queryParameters: {'limit': 20});
  return (resp.data ?? []).cast<Map<String, dynamic>>();
});

final motivationProvider = FutureProvider<List<Map<String, dynamic>>>((ref) async {
  final dio = ref.watch(dioProvider);
  final resp = await dio.get<List<dynamic>>('/public/motivation');
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
    final news = ref.watch(newsProvider);
    final motivation = ref.watch(motivationProvider);

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
                ref.invalidate(newsProvider);
                ref.invalidate(motivationProvider);
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
                const SizedBox(height: 18),
                Text('Trending news', style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800)),
                const SizedBox(height: 10),
                news.when(
                  data: (items) => _News(items: items),
                  loading: () => const LinearProgressIndicator(),
                  error: (e, _) => Text('News error: $e'),
                ),
                const SizedBox(height: 18),
                Text('Motivation', style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800)),
                const SizedBox(height: 10),
                motivation.when(
                  data: (items) => _Motivation(items: items),
                  loading: () => const LinearProgressIndicator(),
                  error: (e, _) => Text('Motivation error: $e'),
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

class _News extends StatelessWidget {
  const _News({required this.items});

  final List<Map<String, dynamic>> items;

  @override
  Widget build(BuildContext context) {
    if (items.isEmpty) return const Text('No news right now');
    return Column(
      children: items.take(8).map((it) {
        final title = (it['title'] as String?) ?? '';
        final source = (it['source'] as String?) ?? '';
        final url = (it['url'] as String?) ?? '';
        final imageUrl = (it['image_url'] as String?) ?? '';
        return Card(
          child: ListTile(
            leading: _Thumb(imageUrl: imageUrl, fallbackIcon: Icons.trending_up),
            title: Text(title, maxLines: 2, overflow: TextOverflow.ellipsis),
            subtitle: Text(source),
            onTap: url.isEmpty
                ? null
                : () {
                    if (context.mounted) {
                      context.push('/browser?title=${Uri.encodeComponent(source)}&url=${Uri.encodeComponent(url)}');
                    }
                  },
          ),
        );
      }).toList(),
    );
  }
}

class _Motivation extends StatelessWidget {
  const _Motivation({required this.items});

  final List<Map<String, dynamic>> items;

  @override
  Widget build(BuildContext context) {
    if (items.isEmpty) return const Text('No videos yet');
    return Column(
      children: items.take(6).map((it) {
        final title = (it['title'] as String?) ?? 'Video';
        final url = (it['url'] as String?) ?? '';
        final thumb = _youtubeThumb(url);
        return Card(
          child: ListTile(
            leading: _Thumb(imageUrl: thumb, fallbackIcon: Icons.play_circle),
            title: Text(title, maxLines: 2, overflow: TextOverflow.ellipsis),
            subtitle: const Text('Watch inside the app'),
            onTap: url.isEmpty
                ? null
                : () {
                    if (context.mounted) {
                      context.push('/browser?title=${Uri.encodeComponent('Motivation')}&url=${Uri.encodeComponent(url)}');
                    }
                  },
          ),
        );
      }).toList(),
    );
  }
}

class _Thumb extends StatelessWidget {
  const _Thumb({required this.imageUrl, required this.fallbackIcon});

  final String imageUrl;
  final IconData fallbackIcon;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final placeholder = Container(
      width: 56,
      height: 56,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
        color: theme.colorScheme.surfaceContainerHighest,
      ),
      child: Icon(fallbackIcon),
    );

    if (imageUrl.isEmpty) return placeholder;
    return ClipRRect(
      borderRadius: BorderRadius.circular(12),
      child: Image.network(
        imageUrl,
        width: 56,
        height: 56,
        fit: BoxFit.cover,
        errorBuilder: (_, __, ___) => placeholder,
      ),
    );
  }
}

String _youtubeThumb(String url) {
  final id = _youtubeId(url);
  if (id == null) return '';
  return 'https://img.youtube.com/vi/$id/hqdefault.jpg';
}

String? _youtubeId(String url) {
  try {
    final uri = Uri.parse(url);
    if (uri.host.contains('youtu.be')) return uri.pathSegments.isEmpty ? null : uri.pathSegments.first;
    if (uri.host.contains('youtube.com')) {
      final v = uri.queryParameters['v'];
      if (v != null && v.isNotEmpty) return v;
      final idx = uri.pathSegments.indexOf('embed');
      if (idx != -1 && uri.pathSegments.length > idx + 1) return uri.pathSegments[idx + 1];
    }
  } catch (_) {}
  return null;
}
