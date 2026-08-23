# IntelliDeploy

AI/ML-integrated CI/CD pipeline for a full-stack application, built with Jenkins.

- **Backend**: FastAPI + scikit-learn (insurance risk classifier, synthetic data)
- **Frontend**: React (Vite), dark dashboard UI
- **CI/CD**: Jenkins declarative pipeline → Docker images → `docker compose` deploy
- **Deploy target**: Docker containers (local machine or a VM with Docker installed)

## Project layout

```
intellideploy/
├── backend/
│   ├── app/            FastAPI app (main.py, model.py, schemas.py)
│   ├── ml/              train_model.py — trains and saves model.pkl
│   ├── tests/            pytest suite
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/              React app (RiskPredictor, PolicyBoard)
│   ├── nginx.conf         proxies /api to the backend container
│   └── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
└── README.md
```

## Run it locally (no Jenkins, no Docker)

**Backend**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python ml/train_model.py       # generates app/model.pkl
uvicorn app.main:app --reload  # http://localhost:8000
```

**Frontend** (separate terminal)
```bash
cd frontend
npm install
npm run dev                    # http://localhost:5173
```

## Run it with Docker Compose

```bash
docker compose up --build
```
- Frontend: http://localhost:8080
- Backend:  http://localhost:8000/health

## Setting up the Jenkins pipeline

1. **Prerequisites on the Jenkins agent**: Docker, Docker Compose plugin, Python 3.11, Node 20. (Or run the pipeline on an agent with those pre-baked, or swap the `sh` steps for `docker run`-based tool containers if you'd rather not install them on the host.)
2. In Jenkins: **New Item → Pipeline**.
3. Under **Pipeline → Definition**, choose **Pipeline script from SCM**, point it at this repo, and set the script path to `Jenkinsfile`.
4. Make sure the Jenkins user can run `docker` (add it to the `docker` group) and has ports 8000/8080 free on the agent.
5. Run the build. Stages: **Checkout → Backend Test → Train Model → Frontend Build → Build Docker Images → Deploy → Smoke Test**.
6. Optional next steps once this works end-to-end:
   - Add a **webhook trigger** (GitHub/GitLab → Jenkins) so pushes to `main` build automatically.
   - Push images to a registry (Docker Hub / ACR / ECR) in the **Build Docker Images** stage instead of only tagging locally.
   - Split `Deploy` into a manual-approval **input** step for a "staging → prod" promotion flow.

## API reference

| Method | Path              | Description                          |
|--------|-------------------|---------------------------------------|
| GET    | `/health`          | Liveness check                        |
| POST   | `/api/predict`     | Risk prediction from the ML model     |
| GET    | `/api/policies`    | List policies                         |
| POST   | `/api/policies`    | Create a policy                       |
| DELETE | `/api/policies/{id}` | Delete a policy                    |

## Notes

- The risk model is trained on **synthetic** data purely to give the pipeline a real ML artifact to build, test, and ship — it is not a real underwriting model.
- The policy board uses an in-memory list (resets on backend restart) to keep the demo dependency-free. Swap in Postgres/SQLite behind `app/main.py` if you want persistence.
