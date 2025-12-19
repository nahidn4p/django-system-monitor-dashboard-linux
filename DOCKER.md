# Docker Deployment Guide

## Important: Container vs Host System Data

When running this application in Docker, **by default it will show the CONTAINER's system data**, not the host system data. This means:

- **Container data (default)**: Limited CPU cores, memory, and processes visible to the container
- **Host data**: Full host system information (CPU, RAM, processes, etc.)

## Option 1: Show Container Data (Default - Isolated)

This is the default behavior. The container runs in isolation and only sees its own resources.

```bash
docker build -t system-monitor .
docker run -p 8000:8000 system-monitor
```

Or with docker-compose:
```bash
docker-compose up
```

**What you'll see:**
- Container's CPU usage (limited cores)
- Container's memory limits
- Only processes running inside the container
- Container's network interfaces

## Option 2: Show Host System Data

To monitor the **host system** instead of the container, you need to give the container access to the host's system directories.

### Method A: Using docker-compose (Recommended)

Use the `docker-compose.host.yml` file:

```bash
docker-compose -f docker-compose.host.yml up
```

This configuration:
- Mounts host's `/proc`, `/sys`, and `/dev` directories
- Uses `privileged: true` mode
- Uses `network_mode: host` to see host network stats

### Method B: Using Docker run command

```bash
docker run -d \
  --name system-monitor \
  --privileged \
  --pid=host \
  --network=host \
  -v $(pwd)/db.sqlite3:/app/db.sqlite3 \
  system-monitor
```

**Key flags:**
- `--privileged`: Gives container access to host devices and capabilities
- `--pid=host`: Uses host's process namespace (see all host processes)
- `--network=host`: Uses host's network stack (see host network stats)
- Note: With `--network=host`, port mapping (`-p`) is not needed

**What you'll see:**
- Host's full CPU usage and cores
- Host's total memory (not container limits)
- All processes running on the host
- Host's network interfaces and statistics
- Host's disk usage

## Security Considerations

⚠️ **Warning**: Running containers with `--privileged` or mounting host system directories gives the container elevated access to your host system. Only use this in trusted environments.

For production:
- Consider using read-only mounts (`:ro`)
- Use specific volume mounts instead of `--privileged` when possible
- Run in isolated networks
- Use proper user permissions

## Verifying What Data You're Seeing

1. **Check the dashboard**: Look at the "System Information" card
   - Container: Will show container hostname, limited resources
   - Host: Will show host system hostname, full resources

2. **Check processes**: 
   - Container: Only shows processes inside container (usually just Python/Django)
   - Host: Shows all system processes

3. **Check CPU cores**:
   - Container: May show limited cores (based on container limits)
   - Host: Shows actual CPU cores available

## Troubleshooting

### Can't see host processes?
- Make sure you're using `--privileged` or mounting `/proc`
- Check that `/host/proc` is accessible inside container

### Network stats not showing?
- Use `network_mode: host` in docker-compose
- Or use `--network=host` flag

### Permission denied errors?
- Container needs `--privileged` mode or proper capabilities
- Check volume mount permissions

## Quick Reference

| Configuration | Shows | Use Case |
|--------------|-------|----------|
| Default Docker | Container data | Testing, development |
| `--privileged` + mounts | Host data | Production monitoring |
| `network_mode: host` | Host network | Network monitoring |

