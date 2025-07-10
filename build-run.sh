podman build -t notes-backend .
podman run -d -p 8000:8000 notes-backend
