from django.conf import settings
from django.db.models.signals import post_delete, post_save

from .compatability import check_version_compatibility
from .exception import DefaultsNotFoundError
from .middleware import get_current_user
from .models import States, TransitionManager, workevents, workflowitems
from .transition import DefaultModelValues


Base_link = "https://pypi.org/project/finflo/"


# CORE LIST ITERATED FROM THE DEFAULT SETTINGS -- PRODUCTION : 27/10/2022
try:
    check_version_compatibility()
    WORK_MODEL_SENDER = list(settings.FINFLO["WORK_MODEL"])
    PARTY_MODEL_SENDER = list(settings.FINFLO["PARTY_MODEL"])
except:
    raise DefaultsNotFoundError(
        "unable to find WORK_MODEL and PARTY_MODEL in your settings.py file , \
        check the documentation for more details",
        Base_link,
    )


def finflo_receiver(signal, senders, **kwargs):
    def decorator(receiver_func):
        for sender in senders:
            if isinstance(signal, (list, tuple)):
                for s in signal:
                    s.connect(receiver_func, sender=sender, **kwargs)
            else:
                signal.connect(receiver_func, sender=sender, **kwargs)
        return receiver_func

    return decorator


def check_existing_record(model, t_id):
    return TransitionManager.objects.filter(type=model, t_id=t_id)


@finflo_receiver(post_save, senders=WORK_MODEL_SENDER)
def creates_finflo_work_models(sender, instance, created, **kwargs):
    if created:
        model = sender._meta.label_lower
        if check_existing_record(model, instance.id).exists():
            pass
        else:
            states = States.objects.first()
            obj = TransitionManager.objects.create(type=model, t_id=instance.id)
            obj2 = workflowitems.objects.create(
                transitionmanager=obj,
                model_type=model,
                record_datas=DefaultModelValues(
                    model_type=obj.type, id=obj.t_id
                ).get_record_datas(),
                event_user=get_current_user(),
                initial_state=states.description,
                interim_state=states.description,
                final_state=states.description,
            )
            workevents.objects.create(
                workflowitems=obj2,
                model_type=model,
                event_user=get_current_user(),
                record_datas=DefaultModelValues(
                    model_type=obj.type, id=obj.t_id
                ).get_record_datas(),
                initial_state=states.description,
                interim_state=states.description,
                final_state=states.description,
            )


@finflo_receiver(post_delete, senders=WORK_MODEL_SENDER)
def delete(sender, instance, **kwargs):
    TransitionManager.objects.filter(
        type=sender._meta.label_lower, t_id=instance.id
    ).delete()
