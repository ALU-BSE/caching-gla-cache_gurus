from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import User
import time

# Example 1: View-level caching (decorator-based)
@cache_page(60 * 5)  # Cache for 5 minutes
def user_list(request):
    """List all users - demonstrates @cache_page decorator"""
    time.sleep(1)  # Simulate slow database query
    
    users = User.objects.all()[:20]
    data = [{
        'id': user.id,
        'email': user.email,
        'user_type': user.user_type,
        'phone': user.phone_number
    } for user in users]
    
    return JsonResponse({
        'users': data,
        'count': len(data),
        'message': 'View-level caching with @cache_page'
    })


# Example 2: Low-level caching (manual cache management)
def user_stats(request):
    """Get user statistics - demonstrates manual caching"""
    cache_key = 'user_stats_data'
    
    # Try to get from cache first
    cached_stats = cache.get(cache_key)
    if cached_stats:
        cached_stats['cached'] = True
        return JsonResponse(cached_stats)
    
    # Not in cache, calculate stats (slow operation)
    time.sleep(1)  # Simulate expensive calculation
    
    stats = {
        'total_users': User.objects.count(),
        'total_passengers': User.objects.filter(user_type='passenger').count(),
        'total_riders': User.objects.filter(user_type='rider').count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'cached': False
    }
    
    # Store in cache for 10 minutes
    cache.set(cache_key, stats, 60 * 10)
    
    return JsonResponse(stats)