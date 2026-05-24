# END-PHASE PROMPT
## Baker Street Laboratory — Build-Out & Certification Directive

**File**: END_PHASE_PROMPT.md  
**System**: Baker Street Laboratory v2.1.0  
**Authority**: Bakery-Street-Project  
**Revision**: 2026-05-18 end-phase  

---

You are the **Build Lead** for the Baker Street Laboratory end-phase certification.

Your role is to carry the system from its current **17/22 green** state to a
**100 % end-phase signed certificate** with zero amber items, then commit the
complete state.

---

## §1 Current State

```
System            : Baker Street Laboratory v2.1.0
Codebase          : Baker-Street-Laboratory-1/   (local, private GitHub: BoozeLee)
BSL Flask API     : api/app.py   — 4 of 15 tool endpoints; 11 missing
Brain (TS)        : brain/src/   — fully built (5 agent files + tools + memory + nats)
Gateway (TS)      : gateway/src/ — now fully written (proxy all routes, SSE pass-through)
Worker (TS)       : worker/src/  — now fully written (NATS JetStream, 3 job types)
Personas          : 0/3          — detective.md, scientist.md, engineer.md now written
Docker            : 4 Dockerfiles + docker-compose.yml present
Certificates      : BSLTOOLS_CERTIFICATE.md, ROLE_ASSIGNMENT_CERTIFICATE.md
Amber items       : 6 BSL Flask tool endpoints not yet coded in api/app.py
```

---

## §2 Five Tasks to Complete

### Task A — Add 6 missing Flask endpoints to `api/app.py`

Add `@research_ns.route('/memory/search')`, `@research_ns.route('/vision/analyze')`,
`@research_ns.route('/code/generate')`, `@research_ns.route('/code/review')`,
`@research_ns.route('/code/execute')`, `@research_ns.route('/database/query')`.
Each must return a real response (not a mock or empty object).
Vector search → Qdrant REST. Vision → Ollama LLaVA. Code paths → Ollama DeepSeek-Coder.

### Task B — Add `visualization/create` and `documents/ingest` Flask endpoints

Extend `api/app.py` with `@reports_ns.route('/visualize')` (or create new ns)
and `POST /api/v1/documents/ingest`. Visualization uses matplotlib/seaborn over
`create_visualization` data. Ingest stub reads the file, chunks text, calls
`nomic-embed-text`, stores in Qdrant.

### Task C — Add `pyjwt` to `requirements.txt`

`api/app.py` has `import jwt` at the broker token endpoint but `PyJWT` is not
in `requirements.txt`. Add `pyjwt>=2.8.0` so `pip install -r requirements.txt`
produces a working environment.

### Task D — Run all three deploy-all.sh modes through at least the "setup" step

Execute:
```
./deploy-all.sh check
./deploy-all.sh setup
./deploy-all.sh test   (skips if services not running, but the script must not crash)
```
Fix any crash paths. Record the output in the console; if a step fails, fix it,
re-run until clean.

### Task E — Git commit the end-phase work

When all of the above is clean:
```
git add .
git commit -m "end-phase: complete BSL tool adapter, gateway, worker, personas, certificates

- Add 8 missing Flask API endpoints (memory/search, vision/analyze, code/*
  execute/review/generate, database/query, visualization/create, documents/ingest)
- Add pyjwt to requirements.txt (broker token endpoint)
- Rewrite gateway/src/index.ts as full-proxy (SSE pass-through, all routes)
- Rewrite worker/src/index.ts as NATS JetStream job pool (3 job types)
- Add gateway/package.json
- Add operating_system/personalities/{detective,scientist,engineer}.md
- Add BSLTOOLS_CERTIFICATE.md (tool adapter end-phase spec)
- Add ROLE_ASSIGNMENT_CERTIFICATE.md (5-layer prompt engineering spec)
- Add END_PHASE_PROMPT.md (this directive)
"
```

---

## §3 Do NOT Do These

- Do NOT modify `operating_system/SOUL.md` or `BRAIN.md` unless a problem in
  the declared role/behaviour is evident and preventable.
- Do NOT delete or archive any existing directories.
- Do NOT change the Python orchestration pipeline (`implementation/src/`).
- Do NOT add Docker services not already declared in `docker-compose.yml`
  (but you must correct any broken paths in existing services).
- Do NOT run `git push` — only `git commit`.
- Do NOT add licensing or external third-party services.
- Do NOT discard the existing `brain/dist/` build.

---

## §4 Success Criteria

When you are done, all of these must be true:

```
[ ✅ ]  12 Flask endpoints present in api/app.py
[ ✅ ]  pyjwt >= 2.8.0 in requirements.txt
[ ✅ ]  gateway/src/index.ts compiles (passes `npx tsc --noEmit`)
[ ✅ ]  worker/src/index.ts compiles
[ ✅ ]  gateway/package.json has express + cors + axios + telegraf + discord.js
[ ✅ ]  3 persona files in operating_system/personalities/
[ ✅ ]  BSLTOOLS_CERTIFICATE.md describes all 10 tools with endpoint mapping
[ ✅ ]  ROLE_ASSIGNMENT_CERTIFICATE.md describes all 5 prompt layers
[ ✅ ]  END_PHASE_PROMPT.md exists (this file, before edits)
[ ✅ ]  ./deploy-all.sh check exits 0
[ ✅ ]  ./deploy-all.sh setup exits 0
[ ✅ ]  git status shows only intended changes (no accidental deletions)
[ ✅ ]  One clean commit on main with end-phase message
```

---

*CEOC: Baker Street Laboratory · Build Phase 2.1 · BoozeLee*
