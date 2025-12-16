import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:qr_flutter/qr_flutter.dart';

import '../../api/client.dart';

final qrProvider = FutureProvider<Map<String, dynamic>>((ref) async {
  final dio = ref.watch(dioProvider);
  final resp = await dio.get<Map<String, dynamic>>('/attendance/id/qr');
  return resp.data ?? <String, dynamic>{};
});

class IdTab extends ConsumerWidget {
  const IdTab({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final qr = ref.watch(qrProvider);
    return CustomScrollView(
      slivers: [
        const SliverAppBar(pinned: true, title: Text('Digital ID')),
        SliverPadding(
          padding: const EdgeInsets.all(16),
          sliver: qr.when(
            data: (data) {
              final token = data['token'] as String?;
              if (token == null || token.isEmpty) {
                return const SliverToBoxAdapter(child: Text('No token'));
              }
              return SliverToBoxAdapter(
                child: Card(
                  child: Padding(
                    padding: const EdgeInsets.all(18),
                    child: Column(
                      children: [
                        QrImageView(data: token, size: 240),
                        const SizedBox(height: 10),
                        const Text('Show this QR for attendance scanning (expires quickly).'),
                        const SizedBox(height: 10),
                        FilledButton(onPressed: () => ref.invalidate(qrProvider), child: const Text('Refresh')),
                      ],
                    ),
                  ),
                ),
              );
            },
            loading: () => const SliverToBoxAdapter(child: LinearProgressIndicator()),
            error: (e, _) => SliverToBoxAdapter(child: Text('ID error: $e')),
          ),
        ),
      ],
    );
  }
}

