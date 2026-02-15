# Docker Setup Guide for LegalContractAI

## Overview

Your project now supports Docker deployment for Railway and local development. This guide explains how to use Docker with your LegalContractAI backend.

## Prerequisites

- Docker Desktop installed ([download](https://www.docker.com/products/docker-desktop))
- Docker Compose installed (included with Docker Desktop)

## Local Development with Docker

### Build and Run Locally

```bash
# Build the Docker image
docker build -t legalcontractai-backend ./backend

# Run the container
docker run -p 8000:8000 legalcontractai-backend
```

### Using Docker Compose (Recommended for Development)

```bash
# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### With Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
SUPABASE_URL=your_url_here
SUPABASE_KEY=your_key_here
```

Then run:

```bash
docker-compose up --build
```

## Deployment to Railway

### Option 1: Automatic Docker Detection (Recommended)

Railway will automatically detect your `Dockerfile` in the backend directory. Simply:

1. Push your code to GitHub
2. Connect your GitHub repo to Railway
3. Railway will detect the Dockerfile and build/deploy automatically

### Option 2: Using `railway.json`

The `railway.json` file has been updated to explicitly use Docker:

```json
{
  "build": {
    "builder": "DOCKER",
    "dockerfile": "Dockerfile"
  },
  "deploy": {
    "startCommand": "gunicorn app.main:app...",
    "healthcheckPath": "/api/health"
  }
}
```

### Steps to Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Docker support"
   git push origin master
   ```

2. **On Railway Dashboard**
   - Create a new project
   - Connect your GitHub repository
   - Select the backend directory as the root
   - Railway will automatically detect Dockerfile and build it
   - Add environment variables (OPENAI_API_KEY, GEMINI_API_KEY, etc.) in Railway dashboard
   - Deploy!

3. **Build & Deploy Status**
   - Railway will log the Docker build process
   - Your app will be available at a Railway URL
   - Monitor deployments in the Railway dashboard

## Docker Image Details

### Dockerfile Features

- **Multi-stage build**: Reduces final image size by ~50%
- **Python 3.11-slim**: Lightweight base image (~150MB)
- **Non-root user**: Runs as `appuser` (uid 1000) for security
- **Health checks**: Automatic health monitoring
- **Optimized dependencies**: Only runtime dependencies in final image

### Build Process

1. Install Python dependencies in builder stage
2. Copy only compiled artifacts to runtime stage
3. Create non-root user
4. Start gunicorn with uvicorn workers

## File Structure

```
backend/
├── Dockerfile           # Docker build configuration
├── .dockerignore        # Excludes unnecessary files from Docker build
├── railway.json         # Railway deployment configuration
├── requirements.txt     # Python dependencies
├── app/
│   ├── main.py         # FastAPI app entry point
│   ├── config.py       # Configuration
│   ├── api/            # API routes
│   ├── agents/         # LLM agents
│   ├── services/       # Business logic
│   └── ...
```

## Common Commands

```bash
# Build image
docker build -t legalcontractai-backend ./backend

# Run container
docker run -p 8000:8000 legalcontractai-backend

# View running containers
docker ps

# View logs
docker logs <container_id>

# Stop container
docker stop <container_id>

# Test with docker-compose
docker-compose up --build
docker-compose down

# Clean up
docker system prune -a
```

## Troubleshooting

### Image Build Fails
- Check that all files in `.dockerignore` are correct
- Ensure `requirements.txt` has all dependencies
- Check for missing or corrupted files

### Container Won't Start
- Check logs: `docker logs <container_id>`
- Verify environment variables are set
- Ensure port 8000 is available

### High Memory Usage
- Reduce worker count in gunicorn command
- Check for memory leaks in your code
- Monitor with `docker stats`

### Slow Build Times
- Docker layer caching will speed up subsequent builds
- Avoid frequent changes to `requirements.txt`
- Clean old images: `docker image prune`

## Environment Variables for Railway

In your Railway dashboard, add these variables:

```
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
PINECONE_API_KEY=your_pinecone_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
DATABASE_URL=your_database_url (if needed)
```

## API Endpoints

After deployment, your API will be available at:
- **Main API**: `https://your-railway-url:8000`
- **Docs**: `https://your-railway-url:8000/docs` (Swagger UI)
- **ReDoc**: `https://your-railway-url:8000/redoc`
- **Health**: `https://your-railway-url:8000/api/health`

## Next Steps

1. Test locally with `docker-compose up`
2. Push changes to GitHub
3. Deploy to Railway
4. Monitor logs and health checks
5. Scale workers as needed based on traffic

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Railway Documentation](https://docs.railway.app/)
- [FastAPI + Docker Guide](https://fastapi.tiangolo.com/deployment/docker/)
- [Gunicorn Workers Guide](https://docs.gunicorn.org/)
