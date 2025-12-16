import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:webview_flutter/webview_flutter.dart';

class BrowserPage extends StatefulWidget {
  const BrowserPage({super.key, required this.title, required this.url});

  final String title;
  final String url;

  @override
  State<BrowserPage> createState() => _BrowserPageState();
}

class _BrowserPageState extends State<BrowserPage> {
  WebViewController? _controller;
  int _progress = 0;

  @override
  void initState() {
    super.initState();
    if (kIsWeb) return;

    final controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setNavigationDelegate(
        NavigationDelegate(
          onProgress: (p) => setState(() => _progress = p),
        ),
      )
      ..loadRequest(Uri.parse(widget.url));
    _controller = controller;
  }

  @override
  Widget build(BuildContext context) {
    final uri = Uri.tryParse(widget.url);
    final validUrl = uri != null && (uri.scheme == 'http' || uri.scheme == 'https');

    if (!validUrl) {
      return Scaffold(
        appBar: AppBar(title: const Text('Browser')),
        body: const Center(child: Text('Invalid URL')),
      );
    }

    if (kIsWeb) {
      return Scaffold(
        appBar: AppBar(title: Text(widget.title)),
        body: Center(
          child: FilledButton.icon(
            onPressed: () => launchUrl(uri, mode: LaunchMode.externalApplication),
            icon: const Icon(Icons.open_in_new),
            label: const Text('Open link'),
          ),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
        actions: [
          IconButton(
            tooltip: 'Open externally',
            onPressed: () => launchUrl(uri, mode: LaunchMode.externalApplication),
            icon: const Icon(Icons.open_in_new),
          ),
          IconButton(
            tooltip: 'Refresh',
            onPressed: () => _controller?.reload(),
            icon: const Icon(Icons.refresh),
          ),
        ],
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(3),
          child: _progress >= 100
              ? const SizedBox(height: 3)
              : LinearProgressIndicator(value: _progress / 100.0),
        ),
      ),
      body: WebViewWidget(controller: _controller!),
    );
  }
}

