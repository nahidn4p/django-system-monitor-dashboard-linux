from monitor.tasks import spike_cpu_ram
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Spike CPU and RAM usage for testing'

    def handle(self, *args, **options):
        spike_cpu_ram()

