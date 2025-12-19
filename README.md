# System Monitor Dashboard

A beautiful Django-based live system monitoring dashboard for Linux systems with scheduled CPU/RAM stress testing.

## Features

- 🖥️ **Real-time System Monitoring**: Live updates of CPU, Memory, Disk, Network, and Process information
- 📊 **Interactive Charts**: Beautiful line charts showing CPU and Memory usage over time
- 🎨 **Modern UI**: Glassmorphic design with smooth animations
- ⚡ **Scheduled Stress Testing**: Automatically spikes CPU and RAM usage (30-50%) every few hours
- 🔥 **Top Processes**: View the most resource-intensive processes
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /home/riyad/Desktop/oracle-project
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Set up cron jobs for scheduled tasks:**

   **Option 1: Using django-crontab (recommended):**
   ```bash
   python manage.py crontab add
   ```

   **Option 2: Using the setup script:**
   ```bash
   ./setup_cron.sh
   ```

   **Option 3: Manual cron setup:**
   ```bash
   crontab -e
   ```
   Then add this line:
   ```
   0 */2 * * * cd /home/riyad/Desktop/oracle-project && python3 manage.py spike_cpu_ram >> /tmp/system_monitor_spike.log 2>&1
   ```

   This will add the scheduled task that spikes CPU/RAM every 2 hours.

6. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application

1. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

2. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:8000/
   ```

## Scheduled Tasks

The application includes a scheduled task that automatically spikes CPU and RAM usage:
- **Frequency**: Every 2 hours (configurable in `settings.py`)
- **CPU Usage**: Randomly between 30-50% of available CPU cores
- **RAM Usage**: Randomly between 30-50% of available memory
- **Duration**: Randomly between 5-15 minutes per spike

### Manual Task Execution

You can manually trigger the CPU/RAM spike task:
```bash
python manage.py spike_cpu_ram
```

### Managing Cron Jobs

- **View active cron jobs:**
  ```bash
  python manage.py crontab show
  ```

- **Remove cron jobs:**
  ```bash
  python manage.py crontab remove
  ```

## Project Structure

```
oracle-project/
├── manage.py
├── requirements.txt
├── README.md
├── system_monitor/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── monitor/                  # Main monitoring app
    ├── views.py              # API endpoints
    ├── urls.py               # URL routing
    ├── tasks.py              # Scheduled task functions
    ├── templates/
    │   └── monitor/
    │       └── dashboard.html # Main dashboard UI
    └── management/
        └── commands/
            └── spike_cpu_ram.py # Management command
```

## API Endpoints

- `GET /` - Main dashboard page
- `GET /api/system-info/` - JSON API endpoint for system information

## Technologies Used

- **Django 4.2**: Web framework
- **psutil**: System and process utilities
- **Chart.js**: Interactive charts
- **django-crontab**: Scheduled task management

## Notes

- The dashboard updates every 2 seconds automatically
- The scheduled task runs in the background using cron
- CPU/RAM spikes are designed to be safe and won't crash your system
- All data is fetched in real-time from the system

## Docker Deployment

### Quick Start
```bash
docker build -t system-monitor .
docker run -p 8000:8000 system-monitor
```

### Dokploy Deployment
See [DOKPLOY.md](DOKPLOY.md) for detailed Dokploy deployment instructions.

**Quick steps:**
1. Push code to Git repository
2. In Dokploy: New Application → Dockerfile
3. Set repository URL and port 8000
4. Deploy!

## Troubleshooting

### Database Permission Error
If you see `unable to open database file`:
- The database is now stored in `/app/data/` directory
- Make sure the container has write permissions
- The Dockerfile automatically creates this directory

### Cron Jobs Not Working
If cron jobs are not working:
1. Make sure `django-crontab` is installed
2. Check that cron service is running: `sudo service cron status`
3. Verify cron jobs: `python manage.py crontab show`

## Docker Deployment

See [DOCKER.md](DOCKER.md) for detailed Docker deployment instructions.

**Quick answer**: By default, Docker shows **container data**. To show **host system data**, use:
```bash
docker-compose -f docker-compose.host.yml up
```

## License

This project is open source and available for personal and educational use.

