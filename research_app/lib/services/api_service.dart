import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/report.dart';

class ApiService {
  static const String baseUrl = 'https://baker-street-flutter-dev-r54rq6v49pj2pxqw-5000.app.github.dev/api/v1';

  static Future<Map<String, dynamic>> conductResearch(String query) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/research/conduct'),
        headers: {'Content-Type': 'application/json'},
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
      final response = await http.get(Uri.parse('$baseUrl/system/health'));
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
      final response = await http.get(Uri.parse('$baseUrl/reports/list'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final reports = data['reports'] as List? ?? [];
        return reports.map((r) => ResearchReport(
          id: r['filename'] ?? '',
          title: 'Report: ${r['filename'] ?? 'Unknown'}',
          summary: '',
          content: '',
          query: '',
          createdAt: DateTime.tryParse(r['created'] ?? '') ?? DateTime.now(),
        )).toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }
}
