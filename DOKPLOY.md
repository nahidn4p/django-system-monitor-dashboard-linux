# Dokploy Deployment Guide

## Quick Deployment Steps

### 1. Prepare Your Repository
- Push your code to GitHub/GitLab/Bitbucket
- Make sure `Dockerfile` is in the root directory
- Ensure `requirements.txt` exists

### 2. Deploy in Dokploy

1. **Login to Dokploy** → Go to **Applications**

2. **Click "New Application"**

3. **Configure Application:**
   - **Name**: `system-monitor` (or your preferred name)
   - **Type**: Select **Dockerfile**
   - **Repository URL**: Your Git repository URL
   - **Branch**: `main` (or your default branch)
   - **Build Context**: `.` (root directory)

4. **Port Configuration:**
   - **Port**: `8000` (This is the internal port Django listens on)
   - **HTTP**: Enable this to get automatic HTTPS/domain via Traefik (optional - can skip if no domain)
   - **Note**: 
     - If you enable HTTP: Traefik will route traffic from port 80 (HTTP) and 443 (HTTPS) to Django on port 8000
     - If you don't enable HTTP: Access Django directly via Dokploy's port mapping or IP:8000

5. **Environment Variables** (Optional):
   ```
   # For IP-based access (no domain), you can skip DJANGO_ALLOWED_HOSTS
   # Django will allow all hosts in DEBUG mode
   
   # If you have a domain:
   DJANGO_ALLOWED_HOSTS=your-domain.com,localhost,127.0.0.1
   
   # For production (recommended):
   DJANGO_SECRET_KEY=your-secret-key-here
   DEBUG=False
   ```
   
   **Note**: 
   - Without a domain: Django allows all hosts when `DEBUG=True` (default), so you can access via IP
   - With a domain: Set `DJANGO_ALLOWED_HOSTS` to your domain name
   - The application is configured to work with Traefik proxy headers when behind a proxy

6. **Click "Deploy"**

### 3. Access Your Application

**Without a domain (IP-based access):**
- Access via: `http://your-server-ip:8000` (if HTTP is disabled)
- Or via Dokploy's port mapping if configured

**With a domain (HTTP enabled):**
- Dokploy will provide a URL (or use your custom domain)
- Access the dashboard at: `http://your-domain/` or `https://your-domain/`

## Important Notes

### Port Configuration with Traefik

**How it works:**
- **Django** listens on port **8000** inside the container (configured in Dockerfile)
- **Traefik** (Dokploy's reverse proxy) listens on port **80** (HTTP) and **443** (HTTPS)
- Traefik automatically routes external traffic (port 80/443) to your Django container (port 8000)
- When you enable "HTTP" in Dokploy, Traefik handles SSL termination and routing

**You don't need to configure port 80** - just set the container port to **8000** and enable HTTP in Dokploy. Traefik handles the rest!

### Database Storage
- The SQLite database is stored in `/app/data/db.sqlite3` inside the container
- **Data persistence**: If you need to persist data across deployments, consider:
  - Using Dokploy's volume mounts feature
  - Or switching to PostgreSQL (recommended for production)

### Host System Monitoring
**By default, Dokploy deployments show CONTAINER metrics**, not host system metrics.

To monitor the **host system**, you need to configure the container with host access:

1. **In Dokploy, look for "Advanced Settings" or "Docker Options"**
2. **Add these Docker flags:**
   ```
   --privileged
   --pid=host
   --network=host
   ```

   Or if Dokploy supports docker-compose override, use:
   ```yaml
   pid: host
   network_mode: host
   privileged: true
   ```

**⚠️ Security Warning**: Using `--privileged` and `--pid=host` gives the container access to the host system. Only use in trusted environments.

### Alternative: Use Dokploy's Built-in Monitoring
Dokploy itself provides host system monitoring. You might not need host access if you just want to monitor the server.

## Troubleshooting

### Database Permission Error
If you see `unable to open database file`:
- The Dockerfile creates `/app/data` with proper permissions
- Make sure the container has write access
- Check Dokploy logs for permission issues

### Container Shows Limited Resources
- This is normal - containers are isolated by default
- To see host metrics, use the advanced Docker options mentioned above

### Static Files Not Loading
- Run `python manage.py collectstatic` manually if needed
- Or ensure `STATIC_ROOT` is properly configured

## Production Recommendations

1. **Use PostgreSQL instead of SQLite:**
   - SQLite doesn't work well in multi-container setups
   - Use Dokploy's database service or external PostgreSQL

2. **Set `DEBUG=False`** in production

3. **Use proper `SECRET_KEY`** (not the default one)

4. **Configure proper `ALLOWED_HOSTS`**

5. **Set up SSL/HTTPS** (Dokploy handles this automatically if HTTP is enabled)

6. **Use environment variables** for sensitive configuration

## Example Environment Variables for Production

```
DJANGO_SECRET_KEY=your-super-secret-key-here-min-50-chars
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:5432/dbname  # If using PostgreSQL
```

