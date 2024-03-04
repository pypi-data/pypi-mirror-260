from typing import Dict, Optional, Type, Union

from django.db.models import Model
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer


class DjeasyListCreateAPI(ListCreateAPIView):
    model: Type[Model]
    create_serializer_class: Type[BaseSerializer]
    list_serializer_class: Type[BaseSerializer]
    context: Optional[Dict[str, any]] = None
    serializer_save: Optional[Dict[str, any]] = None

    def get_create_serializer(self, data: Dict[str, any]) -> BaseSerializer:
        return self.create_serializer_class(data=data)

    def get_list_serializer(self, instance: Model) -> BaseSerializer:
        return (
            self.list_serializer_class(instance, context=self.context, many=True)
            if self.context
            else self.list_serializer_class(instance, many=True)
        )

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        serializer = self.get_list_serializer(queryset)
        return Response({"status": "Success", "data": serializer.data})

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_create_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            (
                serializer.save(**self.serializer_save)
                if self.serializer_save
                else serializer.save()
            )
            return Response({"status": "Success", "data": serializer.data})
        return Response({"status": "Failure", "data": serializer.errors})


class DjeasyRetrieveUpdateAPI(RetrieveUpdateDestroyAPIView):
    model: Type[Model]
    retrieve_serializer_class: Type[BaseSerializer]
    update_serializer_class: Type[BaseSerializer]
    serializer_save: Optional[Dict[str, any]] = None
    context: Optional[Dict[str, any]] = None

    def get_retrieve_serializer(self, instance: Model) -> BaseSerializer:
        return (
            self.retrieve_serializer_class(instance, context=self.context)
            if self.context
            else self.retrieve_serializer_class(instance)
        )

    def get_update_serializer(
        self, instance: Model, data: Dict[str, any]
    ) -> BaseSerializer:
        return self.update_serializer_class(instance, data=data)

    def get_object(self, pk: Union[int, str]) -> Model:
        return get_object_or_404(self.model, pk=pk)

    def retrieve(
        self, request: Request, pk: Union[int, str] = None, *args, **kwargs
    ) -> Response:
        instance = self.get_object(pk)
        serializer = self.get_retrieve_serializer(instance)
        return Response({"status": "Success", "data": serializer.data})

    def update(
        self, request: Request, pk: Union[int, str] = None, *args, **kwargs
    ) -> Response:
        instance = self.get_object(pk)
        serializer = self.get_update_serializer(instance, request.data)
        if serializer.is_valid():
            (
                serializer.save(**self.serializer_save)
                if self.serializer_save
                else serializer.save()
            )
            return Response({"status": "Success", "data": serializer.data})
        return Response({"status": "Failure", "data": serializer.errors})

    def delete(
        self, request: Request, pk: Union[int, str] = None, *args, **kwargs
    ) -> Response:
        self.model.objects.filter(id=pk).delete()
        return Response({"status": "Success", "data": "Deleted Successfully"})
