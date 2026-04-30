# 🔬 Baker Street Laboratory

Autonomous AI research platform with 8 specialized models, multi-agent orchestration, and production-grade infrastructure.

Part of the [Baker Street Labs](https://github.com/Bakery-street-project) ecosystem.

## 🚀 Live Deployment

| Service | URL |
|---------|-----|
| **Flutter Web App** | https://baker-street-flutter-dev-r54rq6v49pj2pxqw-8080.app.github.dev |
| **Baker Street API** | https://baker-street-flutter-dev-r54rq6v49pj2pxqw-5000.app.github.dev/api/v1 |
| **Repository** | https://github.com/BoozeLee/Baker-Street-Laboratory-1 |

## 📱 Flutter Research Platform

Located in `research_app/` - a full-featured research dashboard:

### Features
- **Dashboard Tab**: System health, quick stats (reports, agents, storage)
- **Research Tab**: Submit research queries to the API
- **Reports Tab**: View research reports with **5-star rating system**
- **Agents Tab**: Monitor all 8 AI agents (vision, embed, scientific, creative, coder, legal, audio, longcontext)

### 5-Star Rating System
Rate research reports directly in the Flutter app:
- Tap stars to rate (1-5 stars)
- Ratings persist during session
- Visual feedback with amber/grey stars

### API Integration
The Flutter app connects to the Baker Street Laboratory API:
- `POST /api/v1/research/conduct` - Submit research queries
- `GET /api/v1/system/health` - Check API status
- `GET /api/v1/reports/list` - List research reports
- `GET /api/v1/reports/{id}` - Get report content

### Security
API requires `X-API-Key` header: `bsl-local-dev-key`

## 🤖 Running Locally

### Prerequisites
- Flutter SDK (stable channel)
- Python 3.8+
- GitHub Codespace (recommended)

### Start API Server
```bash
cd Bker-Street-Laboratory-1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 api/app.py
```

### Run Flutter App
```bash
cd research_app
flutter pub get
flutter run -d chrome
```

## 📊 Research Examples

### Homelessness Research
```
Query: "homelessness causes solutions policy interventions"
Session: 78965a56
Status: Completed
Summary: Research report generated successfully
```

## 🏗️ Architecture

```
baker-street-laboratory/
├── api/                    # FastAPI/Flask API server
├── research_app/           # Flutter research platform
│   ├── lib/
│   │   ├── main.dart
│   │   ├── screens/      # Dashboard, Reports, etc.
│   │   ├── widgets/      # StarRating, AgentCard
│   │   ├── services/     # API service
│   │   └── models/       # ResearchReport model
│   ├── build/web/        # Web build output
│   └── pubspec.yaml
├── research/              # Research outputs
├── config/                # Agent configurations
└── implementation/        # Core framework
```

## 💰 License

Proprietary - [Enterprise Licensing Available](mailto:iamthatiamresearch@gmail.com)

---
**Baker Street Laboratory - Where AI Agents Never Sleep** 🔬
