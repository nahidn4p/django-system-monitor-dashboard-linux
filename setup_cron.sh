#!/bin/bash
# Alternative cron setup script
# This adds a cron job to run the CPU/RAM spike task every 2 hours

# Get the absolute path to the project
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH=$(which python3)

# Create cron job entry
CRON_JOB="0 */2 * * * cd $PROJECT_DIR && $PYTHON_PATH manage.py spike_cpu_ram >> /tmp/system_monitor_spike.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "spike_cpu_ram"; then
    echo "Cron job already exists!"
else
    # Add cron job
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Cron job added successfully!"
    echo "The task will run every 2 hours"
fi

# Show current cron jobs
echo ""
echo "Current cron jobs:"
crontab -l | grep spike_cpu_ram

