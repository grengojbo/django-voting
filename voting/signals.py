__author__ = 'abdulaziz'

from django.contrib.contenttypes.models import ContentType
from models import Vote

def delete_votes(sender, **kwargs):
    """
    Delete all votes on the sender. Used in signals.
    E.g. models.signals.post_delete(delete_votes, sender=YourModel)
    """
    ctype = ContentType.objects.get_for_model(sender)
    Vote.objects.filter(content_type=ctype, object_id=kwargs['instance'].id).delete()
