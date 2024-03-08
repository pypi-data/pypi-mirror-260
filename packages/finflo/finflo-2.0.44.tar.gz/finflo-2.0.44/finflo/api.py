from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (Action, Flowmodel, Party, SignList, States,
                     TransitionManager, workevents, workflowitems)
from .serializer import (Actionseriaizer, FlowmodelsSerializer,
                         StatesSerializer, TransitionManagerserializer,
                         Workitemserializer, partytypeserializer,
                         signlistserialzier, workeventslistserializer)
from .transition import FinFlotransition

####################################################
################      API       ####################
####################################################


# 1 . TRANSITION MAKING API


class TransitionApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        model_type = request.data.get("type")
        action = request.data.get("action")
        t_id = request.data.get("t_id")
        # extra datas for manual transitions
        party = request.data.get("party")
        source = request.data.get("source")
        interim = request.data.get("interim")
        destination = request.data.get("destination")
        from_party = request.data.get("from_party")
        to_party = request.data.get("to_party")
        record_datas = request.data.get("record_datas")
        event_user_obj = request.data.get("event_user")

        if model_type and t_id is not None:
            transitions = FinFlotransition(
                action=action.upper(),
                model_type=model_type,
                t_id=t_id,
                source=source,
                interim=interim,
                destination=destination,
                party=party,
                from_party=from_party,
                to_party=to_party,
                record_datas=record_datas,
                event_user_obj=event_user_obj
            )
            return Response(
                {
                    "status": f"Transition {transitions.gets_subaction_name()} success".replace(
                        "  ", " "
                    )
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": "Transition failure"}, status=status.HTTP_204_NO_CONTENT
        )


class TransitionResetApiview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        t_id = request.data.get("t_id")
        model_type = request.data.get("type")
        if type and t_id:
            TransitionManager.objects.filter(t_id=t_id, model_type=model_type).update(
                in_progress=False
            )
            return Response(
                {"status": "Status updated successfully"}, status=status.HTTP_200_OK
            )
        return Response({"status": "Failure"}, status=status.HTTP_204_NO_CONTENT)


#  2 . ALL WORK_MODEL LIST


class DetailsListApiView(ListAPIView):
    queryset = TransitionManager.objects.all()
    serializer_class = TransitionManagerserializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # sourcery skip: lift-return-into-if, remove-redundant-if
        model_type = self.request.query_params.get("type", None)
        t_id = self.request.query_params.get("t_id", None)
        if t_id:
            queryset = TransitionManager.objects.filter(t_id=t_id)
        if model_type and t_id:
            queryset = TransitionManager.objects.filter(
                model_type=model_type, t_id=t_id
            )
        else:
            queryset = TransitionManager.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = TransitionManagerserializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "type": settings.FINFLO["WORK_MODEL"],
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# 3 . WORFLOW API


class WorkFlowitemsListApi(RetrieveUpdateAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = workflowitems.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = Workitemserializer(user)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )


# WORKEVENTS API


class WorkEventsListApi(RetrieveUpdateAPIView):
    queryset = workevents.objects.all()
    serializer_class = workeventslistserializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = workevents.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = workeventslistserializer(user)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )


# ACTION CREATE AND LIST API


class ActionListApi(ListCreateAPIView):
    queryset = Action.objects.all()
    serializer_class = Actionseriaizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        action = self.request.query_params.get("action", None)
        model = self.request.query_params.get("model", None)
        party_id = self.request.query_params.get("party_id", None)
        if (party_id and model and action) is not None:
            return Action.objects.filter(
                party__id=party_id,
                description__icontains=action,
                model__description__icontains=model,
            )
        elif (party_id and model) is not None:
            return Action.objects.filter(
                party__id=party_id, model__description__icontains=model
            )
        elif (action and model) is not None:
            return Action.objects.filter(
                description__icontains=action, model__description__icontains=model
            )
        elif model:
            return Action.objects.filter(model__description__icontains=model)
        elif action:
            return Action.objects.filter(description__icontains=action)
        elif party_id:
            return Action.objects.filter(party__id=party_id)
        else:
            return Action.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = Actionseriaizer(queryset, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = Actionseriaizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "failure", "data": serializer.errors},
            status=status.HTTP_204_NO_CONTENT,
        )


class ActionRetrieveUpdateApi(RetrieveUpdateDestroyAPIView):
    queryset = Action.objects.all()
    serializer_class = Actionseriaizer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = Action.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = Actionseriaizer(user)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk=None):
        queryset = Action.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = Actionseriaizer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "failure", "data": serializer.errors},
            status=status.HTTP_204_NO_CONTENT,
        )


# STATES API


class statesListCreateApi(ListCreateAPIView):
    queryset = States.objects.all()
    serializer_class = StatesSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = States.objects.all()
        serializer = StatesSerializer(queryset, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = StatesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "failure", "data": serializer.errors},
            status=status.HTTP_204_NO_CONTENT,
        )


class StatesRetrieveUpdateApi(RetrieveUpdateDestroyAPIView):
    queryset = States.objects.all()
    serializer_class = StatesSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = States.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = StatesSerializer(user)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk=None):
        queryset = States.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = StatesSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "failure", "data": serializer.errors},
            status=status.HTTP_204_NO_CONTENT,
        )


# FLOW MODEL GET API


class FlowModelGetApi(ListCreateAPIView):
    queryset = Flowmodel.objects.all()
    serializer_class = FlowmodelsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Flowmodel.objects.all()
        serializer = FlowmodelsSerializer(queryset, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = FlowmodelsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "failure", "data": serializer.errors},
            status=status.HTTP_204_NO_CONTENT,
        )


class FlowModelRetrieveUpdateApi(RetrieveUpdateDestroyAPIView):
    queryset = Flowmodel.objects.all()
    serializer_class = FlowmodelsSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = Flowmodel.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = FlowmodelsSerializer(user)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk=None):
        queryset = Flowmodel.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = FlowmodelsSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "failure", "data": serializer.errors},
            status=status.HTTP_204_NO_CONTENT,
        )


# PARTY TYPE API


class PartyTypeListCreateApi(ListCreateAPIView):
    queryset = Party.objects.all()
    serializer_class = partytypeserializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Party.objects.all()
        serializer = partytypeserializer(queryset, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = partytypeserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "failure", "data": serializer.errors},
            status=status.HTTP_204_NO_CONTENT,
        )


class PartyTypeRetrieveUpdateApi(RetrieveUpdateDestroyAPIView):
    queryset = Party.objects.all()
    serializer_class = partytypeserializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = Party.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = partytypeserializer(user)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk=None):
        queryset = Party.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = partytypeserializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "failure", "data": serializer.errors},
            status=status.HTTP_204_NO_CONTENT,
        )


# SIGN LIST API


class SignListListCreateApi(ListCreateAPIView):
    queryset = SignList.objects.all()
    serializer_class = signlistserialzier
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = SignList.objects.all()
        serializer = signlistserialzier(queryset, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = signlistserialzier(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "failure", "data": serializer.errors},
            status=status.HTTP_204_NO_CONTENT,
        )


class SignListRetrieveUpdateApi(RetrieveUpdateDestroyAPIView):
    queryset = SignList.objects.all()
    serializer_class = signlistserialzier
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = SignList.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = signlistserialzier(user)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk=None):
        queryset = SignList.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = signlistserialzier(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "failure", "data": serializer.errors},
            status=status.HTTP_204_NO_CONTENT,
        )
