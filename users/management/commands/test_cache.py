from django.core.management.base import BaseCommand
import time
import requests

class Command(BaseCommand):
    help = 'Test cache performance'
    
    def handle(self, *args, **options):
        base_url = 'http://127.0.0.1:8000'
        
        self.stdout.write(self.style.WARNING('\n=== Testing Cache Performance ===\n'))
        
        # Test 1: View-level caching
        self.stdout.write('Test 1: View-level caching (/api/users/list/)')
        url = f'{base_url}/api/users/list/'
        
        start = time.time()
        try:
            r1 = requests.get(url)
            time1 = time.time() - start
            self.stdout.write(f'  First request: {time1:.3f}s (uncached)')
        except:
            self.stdout.write(self.style.ERROR('  Error: Make sure server is running!'))
            return
        
        start = time.time()
        r2 = requests.get(url)
        time2 = time.time() - start
        self.stdout.write(f'  Second request: {time2:.3f}s (cached)')
        
        improvement1 = ((time1 - time2) / time1) * 100
        self.stdout.write(self.style.SUCCESS(f'  Improvement: {improvement1:.1f}%\n'))
        
        # Test 2: Low-level caching
        self.stdout.write('Test 2: Low-level caching (/api/users/stats/)')
        url = f'{base_url}/api/users/stats/'
        
        start = time.time()
        r1 = requests.get(url)
        time1 = time.time() - start
        data1 = r1.json()
        self.stdout.write(f'  First request: {time1:.3f}s (cached={data1.get("cached")})')
        
        start = time.time()
        r2 = requests.get(url)
        time2 = time.time() - start
        data2 = r2.json()
        self.stdout.write(f'  Second request: {time2:.3f}s (cached={data2.get("cached")})')
        
        improvement2 = ((time1 - time2) / time1) * 100
        self.stdout.write(self.style.SUCCESS(f'  Improvement: {improvement2:.1f}%\n'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('=== Summary ==='))
        self.stdout.write(f'View-level caching improvement: {improvement1:.1f}%')
        self.stdout.write(f'Low-level caching improvement: {improvement2:.1f}%')