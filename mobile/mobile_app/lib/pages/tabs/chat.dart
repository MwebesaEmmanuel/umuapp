import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

import '../../api/client.dart';
import '../../config.dart';
import '../../state/auth.dart';

final roomsProvider = FutureProvider<List<Map<String, dynamic>>>((ref) async {
  final dio = ref.watch(dioProvider);
  final resp = await dio.get<List<dynamic>>('/chat/rooms');
  return (resp.data ?? []).cast<Map<String, dynamic>>();
});

final roomHistoryProvider = FutureProvider.family<List<Map<String, dynamic>>, int>((ref, roomId) async {
  final dio = ref.watch(dioProvider);
  final resp = await dio.get<List<dynamic>>('/chat/rooms/$roomId/messages', queryParameters: {'limit': 50});
  return (resp.data ?? []).cast<Map<String, dynamic>>();
});

class ChatTab extends ConsumerWidget {
  const ChatTab({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final rooms = ref.watch(roomsProvider);
    return CustomScrollView(
      slivers: [
        const SliverAppBar(pinned: true, title: Text('Community chat')),
        SliverPadding(
          padding: const EdgeInsets.all(16),
          sliver: rooms.when(
            data: (items) {
              if (items.isEmpty) return const SliverToBoxAdapter(child: Text('No rooms yet'));
              return SliverList(
                delegate: SliverChildBuilderDelegate(
                  (context, i) {
                    final room = items[i];
                    return Card(
                      child: ListTile(
                        leading: const Icon(Icons.forum),
                        title: Text((room['name'] as String?) ?? 'Room'),
                        subtitle: const Text('Tap to chat'),
                        onTap: () {
                          Navigator.of(context).push(
                            MaterialPageRoute(
                              builder: (_) => ChatRoomPage(
                                roomId: room['id'] as int,
                                roomName: room['name'] as String?,
                              ),
                            ),
                          );
                        },
                      ),
                    );
                  },
                  childCount: items.length,
                ),
              );
            },
            loading: () => const SliverToBoxAdapter(child: LinearProgressIndicator()),
            error: (e, _) => SliverToBoxAdapter(child: Text('Chat error: $e')),
          ),
        ),
      ],
    );
  }
}

class ChatRoomPage extends ConsumerStatefulWidget {
  const ChatRoomPage({super.key, required this.roomId, this.roomName});

  final int roomId;
  final String? roomName;

  @override
  ConsumerState<ChatRoomPage> createState() => _ChatRoomPageState();
}

class _ChatRoomPageState extends ConsumerState<ChatRoomPage> {
  final _text = TextEditingController();
  WebSocketChannel? _channel;
  final List<Map<String, dynamic>> _streamMessages = [];

  @override
  void initState() {
    super.initState();
    _connect();
  }

  @override
  void dispose() {
    _text.dispose();
    _channel?.sink.close();
    super.dispose();
  }

  void _connect() {
    final token = ref.read(authControllerProvider).token;
    if (token == null || token.isEmpty) return;

    final apiUri = Uri.parse(AppConfig.apiBaseUrl);
    final wsScheme = apiUri.scheme == 'https' ? 'wss' : 'ws';
    final wsUri = apiUri.replace(
      scheme: wsScheme,
      path: '${apiUri.path}/chat/ws/rooms/${widget.roomId}',
      queryParameters: {'token': token},
    );

    _channel = WebSocketChannel.connect(wsUri);
    _channel!.stream.listen((event) {
      final decoded = jsonDecode(event as String) as Map<String, dynamic>;
      if (!mounted) return;
      setState(() => _streamMessages.add(decoded));
    });
  }

  @override
  Widget build(BuildContext context) {
    final auth = ref.watch(authControllerProvider);
    final history = ref.watch(roomHistoryProvider(widget.roomId));

    if (!auth.isLoggedIn) {
      return Scaffold(
        appBar: AppBar(title: Text(widget.roomName ?? 'Room')),
        body: const Center(child: Text('Please sign in to chat')),
      );
    }

    return Scaffold(
      appBar: AppBar(title: Text(widget.roomName ?? 'Room')),
      body: Column(
        children: [
          Expanded(
            child: history.when(
              data: (items) {
                final merged = [
                  ...items.map((e) => {...e, 'type': 'history'}),
                  ..._streamMessages,
                ];
                return ListView.builder(
                  padding: const EdgeInsets.all(12),
                  itemCount: merged.length,
                  itemBuilder: (context, i) {
                    final m = merged[i];
                    final type = (m['type'] as String?) ?? 'message';
                    final body = (m['body'] as String?) ?? (m['message'] as String?) ?? '';
                    return Padding(
                      padding: const EdgeInsets.symmetric(vertical: 6),
                      child: Text('$type: $body'),
                    );
                  },
                );
              },
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (e, _) => Center(child: Text('History error: $e')),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _text,
                    decoration: const InputDecoration(border: OutlineInputBorder(), hintText: 'Message'),
                    onSubmitted: (_) => _send(),
                  ),
                ),
                const SizedBox(width: 10),
                IconButton(onPressed: _send, icon: const Icon(Icons.send)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  void _send() {
    final text = _text.text.trim();
    if (text.isEmpty) return;
    _channel?.sink.add(text);
    _text.clear();
  }
}

