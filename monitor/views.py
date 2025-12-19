import json
import os
import psutil
import platform
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

# Check if we're reading from host system (Docker with mounted volumes)
HOST_PROC = os.environ.get('HOST_PROC', '/proc')
IS_CONTAINER = os.path.exists('/.dockerenv') or os.path.exists('/proc/1/cgroup') and 'docker' in open('/proc/1/cgroup').read()


def dashboard(request):
    """Main dashboard view"""
    return render(request, 'monitor/dashboard.html')


@require_http_methods(["GET"])
def system_info(request):
    """API endpoint to get system information"""
    try:
        # CPU Information
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
        
        # Memory Information
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        # Disk Information
        disk = psutil.disk_usage('/')
        disk_io = psutil.disk_io_counters()
        
        # Network Information
        network = psutil.net_io_counters()
        network_if_addrs = psutil.net_if_addrs()
        network_if_stats = psutil.net_if_stats()
        
        # System Information
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        # Process Information
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage and get top 10
        processes = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:10]
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count,
                'frequency': {
                    'current': cpu_freq.current if cpu_freq else None,
                    'min': cpu_freq.min if cpu_freq else None,
                },
                'per_core': cpu_per_core,
            },
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percent': memory.percent,
                'free': memory.free,
            },
            'swap': {
                'total': swap.total,
                'used': swap.used,
                'free': swap.free,
                'percent': swap.percent,
            },
            'disk': {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent,
                'read_bytes': disk_io.read_bytes if disk_io else 0,
                'write_bytes': disk_io.write_bytes if disk_io else 0,
            },
            'network': {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv,
                'interfaces': {
                    name: {
                        'addresses': [str(addr.address) for addr in addrs],
                        'isup': network_if_stats[name].isup if name in network_if_stats else False,
                        'speed': network_if_stats[name].speed if name in network_if_stats else 0,
                    }
                    for name, addrs in network_if_addrs.items()
                },
            },
            'system': {
                'platform': platform.system(),
                'platform_release': platform.release(),
                'platform_version': platform.version(),
                'architecture': platform.machine(),
                'processor': platform.processor(),
                'hostname': platform.node(),
                'boot_time': boot_time.isoformat(),
                'uptime_seconds': int(uptime.total_seconds()),
                'uptime_days': uptime.days,
            },
            'processes': processes,
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
