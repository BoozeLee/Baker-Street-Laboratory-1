class ResearchReport {
  final String id;
  final String title;
  final String summary;
  final String content;
  final String query;
  final DateTime createdAt;
  double rating;
  final String status;

  ResearchReport({
    required this.id,
    required this.title,
    required this.summary,
    required this.content,
    required this.query,
    required this.createdAt,
    this.rating = 0.0,
    this.status = 'completed',
  });

  factory ResearchReport.fromJson(Map<String, dynamic> json) {
    return ResearchReport(
      id: json['session_id'] ?? json['report_id'] ?? '',
      title: 'Research: ${json['query'] ?? 'Unknown'}',
      summary: json['summary'] ?? '',
      content: json['content'] ?? '',
      query: json['query'] ?? '',
      createdAt: DateTime.now(),
      rating: (json['rating'] ?? 0).toDouble(),
    );
  }
}
