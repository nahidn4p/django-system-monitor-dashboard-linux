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
   - **Port**: `8000`
   - **HTTP**: Enable this to get automatic HTTPS/domain

5. **Environment Variables** (Optional but recommended):
   ```
   DJANGO_ALLOWED_HOSTS=your-domain.com,localhost,127.0.0.1
   DJANGO_SECRET_KEY=your-secret-key-here
   DEBUG=False
   ```

6. **Click "Deploy"**

### 3. Access Your Application
- Dokploy will provide a URL (or use your custom domain)
- Access the dashboard at: `http://your-domain/`

## Important Notes

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

