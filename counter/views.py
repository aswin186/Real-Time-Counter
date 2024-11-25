from django.http import JsonResponse
from django.shortcuts import render

from .models import Counter
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def counter_view(request):
    count = Counter.objects.get(pk=1)
    return render(request, 'index.html', {'count': count})


# Signal to broadcast updates
@receiver(post_save, sender=Counter)
def broadcast_counter_update(sender, instance, **kwargs):
    print(f"Broadcasting counter value: {instance.value}")
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'counter_updates',
        {
            'type': 'send_counter_update',
            'value': instance.value
        }
    )

def increment_counter(request):
    counter, created = Counter.objects.get_or_create(pk=1)
    counter.increment()
    return JsonResponse({'value': counter.value})
