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

**Check Dokploy UI for Access URL:**
- Dokploy usually provides an access URL in the application dashboard
- Look for "Access URL" or "Endpoint" in your application settings

**Without a domain (IP-based access):**
- If HTTP is disabled: Try `http://your-server-ip:8000`
- If HTTP is enabled: Access via `http://your-server-ip` (port 80, routed by Traefik)
- Note: Port mapping might not show in `docker ps` but the port can still be accessible

**With a domain (HTTP enabled):**
- Dokploy will provide a URL (or use your custom domain)
- Access the dashboard at: `http://your-domain/` or `https://your-domain/`

**Quick Test:**
```bash
# Test if port 8000 is accessible (from server)
curl http://localhost:8000

# Or test from another machine
curl http://your-server-ip:8000
```

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

To monitor the **host system** (including host processes), you need to configure the container with host access:

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

**Note**: Without `--pid=host`, the "Top Processes" will show only container processes. To see host processes, you must enable `--pid=host` in Dokploy's Docker options.

### Alternative: Use Dokploy's Built-in Monitoring
Dokploy itself provides host system monitoring. You might not need host access if you just want to monitor the server.

## Troubleshooting

### Port Mapping Not Showing in `docker ps`
**Problem**: Container is running but `docker ps` shows no port mapping (empty PORTS column).

**Why this happens**: Dokploy uses its own Docker network and manages port exposure differently than standard Docker. The port mapping might not show in `docker ps` even though the container is accessible.

**Solutions**:

1. **Enable HTTP in Dokploy** (Recommended):
   - Go to your application settings in Dokploy
   - Enable "HTTP" option
   - Traefik will route port 80 → container port 8000
   - Access via: `http://your-server-ip` (port 80) or the domain Dokploy provides

2. **Check Dokploy Application Settings**:
   - Make sure "Port" is set to `8000` in Dokploy
   - Dokploy should automatically expose this port
   - Try accessing: `http://your-server-ip:8000`

3. **Use Dokploy's Network Mode**:
   - In Dokploy advanced settings, check if there's a "Network Mode" option
   - Some Dokploy setups require explicit port exposure configuration

4. **Access via Dokploy's Internal Network**:
   - Dokploy containers are accessible via Traefik even without visible port mapping
   - If HTTP is enabled, access via port 80
   - Check Dokploy's application URL/endpoint

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

### Cannot Access Application
1. **Check if container is running**: `docker ps` should show your container
2. **Check Dokploy logs**: Look for any errors in the application logs
3. **Verify port configuration**: Ensure port 8000 is set in Dokploy
4. **Try enabling HTTP**: This routes traffic through Traefik (port 80 → 8000)
5. **Check firewall**: Ensure port 8000 (or 80 if HTTP enabled) is open

### Top Processes Showing Container Processes Instead of Host
**Problem**: The "Top Processes" section shows only Docker/container processes, not host system processes.

**Solution**: Enable host process namespace access in Dokploy:
1. Go to your application settings in Dokploy
2. Find "Advanced Settings" or "Docker Options"
3. Add: `--pid=host` flag
4. Redeploy the application

**Note**: Without `--pid=host`, psutil can only see processes inside the container. With `--pid=host`, the container shares the host's process namespace and can see all host processes.

### CPU Bar Not Loading/Updating
**Problem**: CPU percentage shows correctly but the progress bar doesn't fill.

**Solution**: This has been fixed in the latest code. The progress bar now properly:
- Parses and validates the CPU percentage value
- Clamps values between 0-100%
- Updates the width correctly

If you still see this issue, try:
1. Hard refresh your browser (Ctrl+F5 or Cmd+Shift+R)
2. Check browser console for JavaScript errors
3. Ensure you're using the latest code version

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

