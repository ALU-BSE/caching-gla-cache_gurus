\# SafeBoda Caching Implementation Report



\*\*Student Name:\*\* John Obure  

\*\*Date:\*\* January 21, 2026



\## 1. Types of Caching Implemented



\### A. View-Level Caching

\- \*\*Location:\*\* `users/views.py` - `user\_list()` function

\- \*\*Implementation:\*\* Using `@cache\_page(60 \* 5)` decorator

\- \*\*Cache Duration:\*\* 5 minutes (300 seconds)

\- \*\*Use Case:\*\* Caching entire view response for listing users

\- \*\*Advantage:\*\* Simple to implement, automatic cache key management



\### B. Low-Level Caching

\- \*\*Location:\*\* `users/views.py` - `user\_stats()` function

\- \*\*Implementation:\*\* Manual `cache.get()` and `cache.set()` calls

\- \*\*Cache Duration:\*\* 10 minutes (600 seconds)

\- \*\*Use Case:\*\* Caching expensive statistical calculations

\- \*\*Advantage:\*\* Fine-grained control, can check if data is cached



\## 2. Redis Configuration



\*\*Backend:\*\* django-redis  

\*\*Location:\*\* redis://127.0.0.1:6379/1  

\*\*Default Timeout:\*\* 300 seconds



Configuration in `safeboda/settings.py`:

```python

CACHES = {

&nbsp;   'default': {

&nbsp;       'BACKEND': 'django\_redis.cache.RedisCache',

&nbsp;       'LOCATION': 'redis://127.0.0.1:6379/1',

&nbsp;       'OPTIONS': {

&nbsp;           'CLIENT\_CLASS': 'django\_redis.client.DefaultClient',

&nbsp;       },

&nbsp;       'TIMEOUT': 300,

&nbsp;   }

}

```



\## 3. Cache Invalidation Strategy



\*\*Implementation:\*\* Django signals in `users/models.py`



\- `post\_save` signal clears cache when user is created/updated

\- `post\_delete` signal clears cache when user is deleted

\- Ensures cache stays consistent with database



\## 4. Performance Results



\### Test Results from `python manage.py test\_cache`:



\*\*View-Level Caching (`/api/users/list/`):\*\*

\- First request (uncached): ~1.0s

\- Second request (cached): ~0.05s

\- \*\*Improvement: ~95%\*\*



\*\*Low-Level Caching (`/api/users/stats/`):\*\*

\- First request (uncached): ~1.0s

\- Second request (cached): ~0.05s

\- \*\*Improvement: ~95%\*\*



\## 5. Best Practices Applied



✅ \*\*Appropriate TTL:\*\* Different cache durations based on data volatility  

✅ \*\*Automatic Invalidation:\*\* Using Django signals for cache clearing  

✅ \*\*Low-level for complex operations:\*\* Manual caching for statistics  

✅ \*\*View-level for simple queries:\*\* Decorator-based for user lists  

✅ \*\*Performance monitoring:\*\* Custom management command for testing  



\## 6. Learning Outcomes Achieved



1\. ✅ Understood different types of caching (view-level vs low-level)

2\. ✅ Implemented Redis-based caching with django-redis

3\. ✅ Created cache invalidation using Django signals

4\. ✅ Monitored cache performance with custom command

5\. ✅ Applied caching best practices (appropriate TTL, invalidation strategy)



\## 7. Conclusion



This implementation demonstrates effective caching strategies for a Django application. The performance improvements of ~95% show significant benefits of caching, especially for frequently accessed but rarely changing data.

