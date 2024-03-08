import contextlib
import json
import logging
from collections import deque
from dataclasses import dataclass, field
from typing import Optional

from django.apps import apps
from django.core import serializers as core_serializers
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q

from .base_enum import Values
from .exception import (
    FlowModelNotFound,
    ModelNotFound,
    ReturnModelNotFound,
    TransitionNotAllowed,
)
from .middleware import get_current_user
from .models import (
    Action,
    Flowmodel,
    SignList,
    TransitionManager,
    workevents,
    workflowitems,
)

logging.basicConfig(
    filename="finflo.log", format="%(asctime)s %(message)s", filemode="w"
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
####################################################
#############       CORE     #######################
####################################################


@dataclass
class FinFlotransition:
    # BASE CONSTRUCTORS #

    t_id: int
    model_type: str
    source: str
    destination: str
    interim: Optional[str] = None
    action: Optional[str] = None
    party: Optional[str] = None
    from_party: Optional[str] = None
    to_party: Optional[str] = None
    record_datas: Optional[None] = None
    event_user_obj: Optional[object] = None
    current_user: Optional[object] = field(default=get_current_user())

    def __post_init__(self):
        self.check_event_user_instance()
        self.current_user = (
            self.event_user_obj if self.event_user_obj else get_current_user()
        )
        self.action = self.action.upper() if self.action else None
        if self.action:
            if self.action == self.gets_default_return_action().description:
                self.return_transition()
            else:
                self.transition()
        else:
            self.manualtransitions()

    def __repr__(self):
        return f"the id is {self.t_id} and type is {self.model_type}"

    def __str__(self):
        return f"the id is {self.t_id} and type is {self.model_type}"

    def check_event_user_instance(self):
        if self.event_user_obj:
            try:
                apps.get_model(self.event_user_obj)
            except:
                raise ImproperlyConfigured(
                    f"No model named as {self.event_user_obj} present in your django application , re-enter the model name properly"
                )

    def gets_base_action(self):
        try:
            return Action.objects.get(
                description=self.action, model__description=self.model_type
            )
        except:
            logger.error("Action not found")
            raise ModelNotFound()

    # RETURN ACTION
    @staticmethod
    def gets_default_return_action():
        try:
            return Action.objects.get(id=1)
        except:
            logger.error("Return Action not found")
            raise ReturnModelNotFound()

    def gets_wf_item(self, model):
        return workflowitems.objects.get(transitionmanager=model)

    def get_flow_model(self):
        try:
            return Flowmodel.objects.get(description__icontains=self.model_type)
        except Exception as exce:
            raise FlowModelNotFound() from exce

    def gets_base_model(self):
        try:
            return TransitionManager.objects.get(type=self.model_type, t_id=self.t_id)
        except Exception as e:
            logger.error(
                f"Matching transition manager not found for {self.model_type} and t_id of {self.t_id}"
            )
            raise ModelNotFound() from e

    def sign_reset(self, overall_model):
        overall_model[0].sub_sign = 0
        overall_model[0].in_progress = False
        overall_model[0].save()

    def get_record_datas(self):
        try:
            overall_model = self.gets_base_model()
            gets_model = apps.get_model(overall_model.type)
            query_data = gets_model.objects.filter(id=overall_model.t_id)
            base_serialized_Data = core_serializers.serialize("json", query_data)
            if query_data.exists():
                return {"values": json.loads(base_serialized_Data)}
        except Exception:
            return {"values": None}

    # GETS ALL ACTION
    def gets_all_models(self):
        try:
            gets_model = TransitionManager.objects.get(
                type__icontains=self.model_type, t_id=self.t_id
            )
            gets_flows = Flowmodel.objects.get(description__icontains=self.model_type)
            gets_action = Action.objects.get(
                Q(model=gets_flows.id) | Q(model=None),
                description=self.action,
                party__id=self.party or None,
            )
            gets_wf = self.gets_wf_item(gets_model.id)
            sign_lists = []
            sub_action_list = []
            try:
                for item in SignList.objects.all():
                    sign_lists.append(item.name)
                    sub_action_list.append(item.sub_action_name)
                    if item.name == gets_action.stage_required.name:
                        break
                next_avail_trans = sign_lists[gets_model.sub_sign :]
                next_avail_trans_value = deque(next_avail_trans)
                next_avail_trans_value.popleft()
                next_avail_Transition = {"values": list(next_avail_trans_value)}
            except Exception:
                next_avail_Transition = None
            return (
                gets_model,
                gets_action,
                gets_flows,
                gets_wf,
                sign_lists,
                next_avail_Transition,
                sub_action_list,
            )
        except:
            logger.error(
                "Matching Action or Flow model not found , may be improperly configured"
            )
            raise ModelNotFound()

    def return_transition(self):
        overall_model = self.gets_all_models()
        obj, created = workflowitems.objects.update_or_create(
            transitionmanager=overall_model[0] or overall_model[0].id,
            defaults={
                "initial_state": (
                    overall_model[1].from_state.description
                    if overall_model[1].from_state
                    else overall_model[3].initial_state
                ),
                "interim_state": overall_model[1].to_state.description,
                "final_state": overall_model[1].to_state.description,
                "action": self.action,
                "record_datas": self.get_record_datas(),
                "subaction": self.action,
                "previous_action": overall_model[3].action,
                "next_available_transitions": None,
                "model_type": self.model_type,
                "event_user": self.current_user,
                "final_value": True,
                "from_party": overall_model[1].from_party or self.from_party,
                "to_party": overall_model[1].to_party or self.to_party,
            },
        )
        obj.save()
        workevents.objects.create(
            workflowitems=overall_model[3],
            event_user=self.current_user,
            initial_state=(
                overall_model[1].from_state.description
                if overall_model[1].from_state
                else overall_model[3].initial_state
            ),
            final_value=True,
            record_datas=self.get_record_datas(),
            interim_state=overall_model[1].to_state.description,
            final_state=overall_model[1].to_state.description,
            action=self.action,
            subaction=self.action,
            model_type=self.model_type,
            from_party=overall_model[1].from_party or self.from_party,
            to_party=overall_model[1].to_party or self.to_party,
        )
        self.sign_reset(overall_model)

    # MANUAL TRANSITION WITH SOURCE , INTERIM , AND destination STATES

    def gets_default_model(self):
        obj, created = TransitionManager.objects.get_or_create(
            t_id=self.t_id, type=self.model_type
        )
        return obj

    def manualtransitions(self):
        try:
            workflowitems.objects.filter(
                transitionmanager=self.gets_default_model()
            ).update(
                initial_state=self.source,
                interim_state=self.interim,
                final_state=self.destination,
                next_available_transitions=None,
                record_datas=self.get_record_datas(),
                model_type=self.model_type,
                event_user=self.current_user,
                from_party=self.from_party,
                to_party=self.to_party,
                final_value=True,
            )
            workevents.objects.create(
                workflowitems=workflowitems.objects.get(
                    transitionmanager=self.gets_default_model()
                ),
                event_user=self.current_user,
                initial_state=self.source,
                interim_state=self.interim,
                final_state=self.destination,
                model_type=self.model_type,
                record_datas=self.get_record_datas(),
                from_party=self.from_party,
                to_party=self.to_party,
                final_value=True,
            )
        except Exception:
            data = workflowitems.objects.create(
                transitionmanager=self.gets_default_model(),
                initial_state=self.source,
                interim_state=self.interim,
                final_state=self.destination,
                next_available_transitions=None,
                record_datas=self.get_record_datas(),
                model_type=self.model_type,
                event_user=self.current_user,
                from_party=self.from_party,
                to_party=self.to_party,
                final_value=True,
            )
            workevents.objects.create(
                workflowitems=data,
                event_user=self.current_user,
                initial_state=self.source,
                interim_state=self.interim,
                final_state=self.destination,
                model_type=self.model_type,
                record_datas=self.get_record_datas(),
                from_party=self.from_party,
                to_party=self.to_party,
                final_value=True,
            )

        # except Exception as e:
        #     raise TransitionNotAllowed() from e

    ## CORE TRANSITION ###
    def gets_subaction_name(self):
        with contextlib.suppress(Exception):
            overall_model = self.gets_all_models()
            data = overall_model[6][overall_model[0].sub_sign - 1]
            return "" if data == Values.INITIAL_SIGN else data
        return None

    def transition(self):
        overall_model = self.gets_all_models()

        if overall_model[0] is None:
            raise TransitionNotAllowed()
        try:
            wf_item = workflowitems.objects.update_or_create(
                transitionmanager=overall_model[0] or overall_model[0].id,
                defaults={
                    "initial_state": overall_model[1].from_state.description,
                    "interim_state": overall_model[4][1 + overall_model[0].sub_sign],
                    "final_state": overall_model[1].to_state.description,
                    "next_available_transitions": overall_model[5],
                    "action": self.action,
                    "subaction": overall_model[6][overall_model[0].sub_sign],
                    "model_type": self.model_type,
                    "record_datas": self.get_record_datas(),
                    "event_user": self.current_user,
                    "from_party": overall_model[1].from_party or self.from_party,
                    "to_party": overall_model[1].to_party or self.to_party,
                },
            )
            workevents.objects.create(
                workflowitems=overall_model[3],
                event_user=self.current_user,
                initial_state=overall_model[1].from_state.description,
                interim_state=overall_model[4][1 + overall_model[0].sub_sign],
                record_datas=self.get_record_datas(),
                final_state=overall_model[1].to_state.description,
                action=self.action,
                subaction=overall_model[6][overall_model[0].sub_sign],
                model_type=self.model_type,
                from_party=overall_model[1].from_party or self.from_party,
                to_party=overall_model[1].to_party or self.to_party,
            )
            overall_model[0].sub_sign += 1
            overall_model[0].in_progress = True
            overall_model[0].save()
            logger.info(
                f"Transition done for {self.model_type} with action of {self.action}"
            )
        except Exception:
            wf_item = workflowitems.objects.update_or_create(
                transitionmanager=overall_model[0] or overall_model[0].id,
                defaults={
                    "initial_state": overall_model[1].from_state.description,
                    "interim_state": overall_model[1].to_state.description,
                    "final_state": overall_model[1].to_state.description,
                    "action": self.action,
                    "next_available_transitions": None,
                    "subaction": self.action,
                    "model_type": self.model_type,
                    "record_datas": self.get_record_datas(),
                    "event_user": self.current_user,
                    "from_party": overall_model[1].from_party or self.from_party,
                    "to_party": overall_model[1].to_party or self.to_party,
                    "final_value": True,
                },
            )
            workevents.objects.create(
                workflowitems=overall_model[3],
                event_user=self.current_user,
                initial_state=overall_model[1].from_state.description,
                interim_state=overall_model[1].to_state.description,
                record_datas=self.get_record_datas(),
                final_state=overall_model[1].to_state.description,
                action=self.action,
                subaction=self.action,
                model_type=self.model_type,
                from_party=overall_model[1].from_party or self.from_party,
                to_party=overall_model[1].to_party or self.to_party,
                final_value=True,
            )
            # self.sign_reset(overall_model)
            overall_model[0].sign_reset
            logger.info(
                f"Last Transition done for model type {self.model_type} with action of {self.action}"
            )


@dataclass
class DefaultModelValues:
    model_type: str
    id: str

    def get_record_datas(self):
        try:
            gets_model = apps.get_model(self.model_type)
            query_data = gets_model.objects.filter(id=self.id)
            base_serialized_Data = core_serializers.serialize("json", query_data)
            if query_data.exists():
                return {"values": json.loads(base_serialized_Data)}
        except Exception:
            return {"values": None}
