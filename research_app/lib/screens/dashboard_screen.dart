import 'package:flutter/material.dart';
import 'package:research_app/services/api_service.dart';
import 'package:research_app/widgets/star_rating.dart';
import 'report_detail_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final ApiService _api = ApiService();
  final TextEditingController _queryController = TextEditingController();
  
  Map<String, dynamic>? _systemStatus;
  List<ResearchReport> _reports = [];
  bool _isLoading = false;
  bool _isResearching = false;
  String _selectedTab = 'Dashboard';

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() => _isLoading = true);
    try {
      final status = await _api.getSystemHealth();
      final reportsData = await _api.listReports();
      setState(() {
        _systemStatus = status;
        _reports = reportsData;
      });
    } catch (e) {
      setState(() {
        _systemStatus = {'status': 'error', 'error': e.toString()};
      });
    } finally {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _conductResearch() async {
    if (_queryController.text.isEmpty) return;
    
    setState(() => _isResearching = true);
    try {
      final result = await _api.conductResearch(_queryController.text);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Research completed: ${result['session_id']}')),
        );
        _queryController.clear();
        _loadData();
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e'), backgroundColor: Colors.red),
        );
      }
    } finally {
      setState(() => _isResearching = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Baker Street Laboratory'),
        backgroundColor: const Color(0xFF1A1A2E),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadData,
          ),
        ],
      ),
      body: Column(
        children: [
          _buildTabBar(),
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _buildCurrentTab(),
          ),
        ],
      ),
    );
  }

  Widget _buildTabBar() {
    return Container(
      color: const Color(0xFF1A1A2E),
      child: Row(
        children: ['Dashboard', 'Research', 'Reports', 'Agents'].map((tab) {
          final isSelected = _selectedTab == tab;
          return Expanded(
            child: GestureDetector(
              onTap: () => setState(() => _selectedTab = tab),
              child: Container(
                padding: const EdgeInsets.symmetric(vertical: 12),
                decoration: BoxDecoration(
                  border: Border(
                    bottom: BorderSide(
                      color: isSelected ? Colors.blue : Colors.transparent,
                      width: 2,
                    ),
                  ),
                ),
                child: Text(
                  tab,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: isSelected ? Colors.blue : Colors.grey,
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  ),
                ),
              ),
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildCurrentTab() {
    switch (_selectedTab) {
      case 'Dashboard':
        return _buildDashboardTab();
      case 'Research':
        return _buildResearchTab();
      case 'Reports':
        return _buildReportsTab();
      default:
        return _buildDashboardTab();
    }
  }

  Widget _buildDashboardTab() {
    final status = _systemStatus?['status'] ?? 'unknown';
    final isHealthy = status == 'healthy';
    
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(
                        isHealthy ? Icons.check_circle : Icons.error,
                        color: isHealthy ? Colors.green : Colors.red,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        'System Status: ${isHealthy ? "Healthy" : "Unhealthy"}',
                        style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text('API Version: ${_systemStatus?['version'] ?? "Unknown"}'),
                  Text('Last Check: ${_systemStatus?['timestamp'] ?? "Never"}'),
                ],
            ),
          ),
          const SizedBox(height: 16),
          const Text('Quick Stats', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(child: _buildStatCard('Reports', _reports.length.toString(), Icons.description)),
              const SizedBox(width: 8),
              Expanded(child: _buildStatCard('Agents', '8', Icons.smart_toy)),
              const SizedBox(width: 8),
              Expanded(child: _buildStatCard('Storage', '25GB', Icons.storage)),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          children: [
            Icon(icon, color: Colors.blue),
            const SizedBox(height: 4),
            Text(value, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            Text(title, style: const TextStyle(fontSize: 12, color: Colors.grey)),
          ],
        ),
      ),
    );
  }

  Widget _buildResearchTab() {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('New Research Query', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          TextField(
            controller: _queryController,
            decoration: InputDecoration(
              hintText: 'Enter your research question...',
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
              filled: true,
              fillColor: const Color(0xFF1A1A2E),
            ),
            maxLines: 3,
          ),
          const SizedBox(height: 16),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: _isResearching ? null : _conductResearch,
              icon: _isResearching 
                  ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                  : const Icon(Icons.science),
              label: Text(_isResearching ? 'Researching...' : 'Conduct Research'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                backgroundColor: Colors.blue,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildReportsTab() {
    if (_reports.isEmpty) {
      return const Center(child: Text('No reports yet. Start a research query!'));
    }
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _reports.length,
      itemBuilder: (context, index) {
        final report = _reports[index];
        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          child: ListTile(
            leading: const Icon(Icons.description, color: Colors.blue),
            title: Text(report.id ?? 'Unknown Report'),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(report.createdAt?.toString().split(' ')[0] ?? ''),
                const SizedBox(height: 4),
                StarRating(
                  rating: report.rating,
                  onRatingChanged: (rating) {
                    setState(() {
                      report.rating = rating;
                    });
                  },
                ),
              ],
            ),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ReportDetailScreen(report: report),
                ),
              );
            },
          ),
        );
      },
    );
  }
}
