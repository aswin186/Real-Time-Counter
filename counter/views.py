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


'''It will execute when any updates in the Counter object 
 and it will create an event to the WebSockets with new value of count as message
 Here django signals decorater post_save is used to check the updates in the counter value object 
 and if changes this will execute'''
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


# It will execute when pressed the increment button and increment the value of count and return a JsonResponse
def increment_counter(request):
    counter, created = Counter.objects.get_or_create(pk=1)
    counter.increment()
    return JsonResponse({'value': counter.value})

# It will execute when pressed the decrement button and decrement the value of count and return a JsonResponse
def decrement_counter(request):
    counter, created = Counter.objects.get_or_create(pk=1)
    counter.decrement()
    return JsonResponse({'value': counter.value})