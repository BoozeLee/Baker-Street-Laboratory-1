import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/report.dart';

class ApiService {
  static const String baseUrl = 'https://baker-street-flutter-dev-r54rq6v49pj2pxqw-5000.app.github.dev/api/v1';
  static const String apiKey = 'bsl-local-dev-key';

  static Map<String, String> get _headers => {
    'Content-Type': 'application/json',
    'X-API-Key': apiKey,
  };

  static Future<Map<String, dynamic>> conductResearch(String query) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/research/conduct'),
        headers: _headers,
        body: jsonEncode({'query': query, 'output_dir': 'research/api_output'}),
      );
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<Map<String, dynamic>> getSystemHealth() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/system/health'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<List<ResearchReport>> listReports() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/reports/list'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final reports = data['reports'] as List? ?? [];
        return reports.map((r) => ResearchReport(
          id: r['filename'] ?? '',
          title: 'Report: ${r['filename'] ?? 'Unknown'}',
          summary: r['summary'] ?? '',
          content: '',
          query: r['query'] ?? '',
          createdAt: DateTime.tryParse(r['created'] ?? '') ?? DateTime.now(),
        )).toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }

  static Future<String> getReportContent(String reportId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/reports/$reportId'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['content'] ?? '';
      } else {
        throw Exception('Failed to get report');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }
}
