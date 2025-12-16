import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../api/client.dart';

class AssistantPage extends ConsumerStatefulWidget {
  const AssistantPage({super.key});

  @override
  ConsumerState<AssistantPage> createState() => _AssistantPageState();
}

class _AssistantPageState extends ConsumerState<AssistantPage> {
  final _controller = TextEditingController();
  bool _loading = false;
  String? _answer;
  String? _error;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _ask() async {
    final prompt = _controller.text.trim();
    if (prompt.isEmpty) return;

    setState(() {
      _loading = true;
      _error = null;
      _answer = null;
    });

    try {
      final dio = ref.read(dioProvider);
      final resp = await dio.post<Map<String, dynamic>>('/ai/chat', data: {'prompt': prompt});
      setState(() => _answer = (resp.data?['answer'] as String?) ?? '');
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
      appBar: AppBar(title: const Text('UMU Assistant (beta)')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Text(
              'Ask about UMU services, offices, and general guidance. '
              'In V1 this is a basic assistant; we will improve it with UMU knowledge documents.',
              style: theme.textTheme.bodySmall,
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _controller,
              minLines: 1,
              maxLines: 3,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Type your question…',
              ),
            ),
            const SizedBox(height: 10),
            FilledButton(
              onPressed: _loading ? null : _ask,
              child: _loading ? const SizedBox(height: 18, width: 18, child: CircularProgressIndicator()) : const Text('Ask'),
            ),
            const SizedBox(height: 16),
            if (_error != null)
              Text(_error!, style: TextStyle(color: theme.colorScheme.error)),
            if (_answer != null)
              Expanded(
                child: SingleChildScrollView(
                  child: Text(_answer!),
                ),
              )
            else
              const Spacer(),
          ],
        ),
      ),
    );
  }
}

