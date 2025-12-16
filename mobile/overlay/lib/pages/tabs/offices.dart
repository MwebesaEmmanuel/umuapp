import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../api/client.dart';

final officesProvider = FutureProvider.family<List<Map<String, dynamic>>, String?>((ref, q) async {
  final dio = ref.watch(dioProvider);
  final resp = await dio.get<List<dynamic>>('/campus/offices', queryParameters: {'q': q});
  return (resp.data ?? []).cast<Map<String, dynamic>>();
});

class OfficesTab extends ConsumerStatefulWidget {
  const OfficesTab({super.key, this.visitorMode = false});

  final bool visitorMode;

  @override
  ConsumerState<OfficesTab> createState() => _OfficesTabState();
}

class _OfficesTabState extends ConsumerState<OfficesTab> {
  String? _q;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final offices = ref.watch(officesProvider(_q));

    return CustomScrollView(
      slivers: [
        const SliverAppBar(pinned: true, title: Text('Campus offices')),
        SliverPadding(
          padding: const EdgeInsets.all(16),
          sliver: SliverList(
            delegate: SliverChildListDelegate.fixed(
              [
                TextField(
                  decoration: const InputDecoration(
                    prefixIcon: Icon(Icons.search),
                    hintText: 'Search office (e.g. Registry)',
                    border: OutlineInputBorder(),
                  ),
                  onChanged: (v) => setState(() => _q = v.trim().isEmpty ? null : v.trim()),
                ),
                const SizedBox(height: 12),
                offices.when(
                  data: (items) {
                    if (items.isEmpty) return const Text('No offices yet (staff will add them)');
                    return Column(
                      children: items.map((it) {
                        final name = (it['name'] as String?) ?? '';
                        final building = (it['building'] as String?) ?? '';
                        final category = (it['category'] as String?) ?? '';
                        return Card(
                          child: ListTile(
                            title: Text(name),
                            subtitle: Text([category, building].where((x) => x.isNotEmpty).join(' • ')),
                            trailing: const Icon(Icons.chevron_right),
                            onTap: () {
                              final lat = it['latitude'];
                              final lon = it['longitude'];
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(content: Text('Map: $lat,$lon (Google Maps embed next)')),
                              );
                            },
                          ),
                        );
                      }).toList(),
                    );
                  },
                  loading: () => const LinearProgressIndicator(),
                  error: (e, _) => Text('Offices error: $e', style: TextStyle(color: theme.colorScheme.error)),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

