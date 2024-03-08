from django.apps import apps
from django.conf import settings
from rest_framework import serializers

from .models import (Action, Flowmodel, Party, SignList, States,
                     TransitionManager, workevents, workflowitems)


class Workeventsserializer(serializers.ModelSerializer):
    work_model = serializers.SerializerMethodField()

    class Meta:
        model = workevents
        fields = [
            'work_model',
            'id',
            'action',
            'subaction',
            'initial_state',
            'interim_state',
            'final_state',
            'event_user',
            'record_datas',
            'from_party',
            'to_party',
            'model_type',
            'final_value',
            'created_date',
            'updated_at'
        ]

    def get_work_model(self,obj):
        try:
            return {"t_id" : obj.workflowitems.transitionmanager.t_id ,"model_type" : obj.workflowitems.transitionmanager.type }
        except Exception:
            return None




class Workitemserializer(serializers.ModelSerializer):
    WorkFlowEvents = Workeventsserializer(many=True, read_only=True)
    work_model = serializers.SerializerMethodField()

    class Meta:
        model = workflowitems
        fields = [
            'work_model',
            'id',
            'initial_state',
            'interim_state',
            'final_state',
            'event_user',
            'action',
            'subaction',
            'next_available_transitions',
            'model_type',
            'created_date',
            'updated_at',
            'from_party',
            'to_party',
            'users_in',
            'is_read_by',
            'WorkFlowEvents',
        ]
    

    def get_work_model(self,obj):
        try:
            return {"t_id" : obj.transitionmanager.t_id ,"model_type" : obj.transitionmanager.type }
        except Exception:
            return None




class TransitionManagerserializer(serializers.ModelSerializer):
    workflowitems = Workitemserializer(read_only = True)
    model = serializers.SerializerMethodField()
    wf_item_id = serializers.SerializerMethodField()
    class Meta:
        model = TransitionManager
        fields = [
            'id',
            'type',
            't_id',
            'in_progress',
            'wf_item_id',
            'model',
            'workflowitems'
        ]

    def get_model(self,obj):
        try:
            arr = settings.FINFLO['WORK_MODEL']
            for i in arr:
                user = apps.get_model(i)
                qs = user.objects.filter(id = obj.t_id ).values()
                if qs.exists():
                    break
            return qs
        except Exception:
            return None
                    

    def get_wf_item_id(self,obj):
        return obj.workflowitems.id



class Actionseriaizer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'



class StatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = '__all__'


class FlowmodelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flowmodel
        fields = '__all__'


class partytypeserializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'



class signlistserialzier(serializers.ModelSerializer):
    class Meta:
        model = SignList
        fields = '__all__'
    

class workflowitemslistserializer(serializers.ModelSerializer):
    class Meta:
        model = workflowitems
        fields = '__all__'


class workeventslistserializer(serializers.ModelSerializer):
    class Meta:
        model = workevents
        fields = '__all__'




