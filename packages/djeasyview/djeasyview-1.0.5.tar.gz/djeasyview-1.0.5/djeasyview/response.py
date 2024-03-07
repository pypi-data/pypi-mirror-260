from rest_framework.response import Response
from rest_framework import status
from enum import StrEnum


class ResponseStatus(StrEnum):
    SUCCESS = "Success"
    FAILURE = "Failure"

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return f"{self.value}"


def SuccessResponse(data):
    return Response(
        {"status": ResponseStatus.SUCCESS, "data": data},
        status=status.HTTP_200_OK,
    )


def FailureResponse(data):
    return Response(
        {"status": ResponseStatus.FAILURE, "data": data},
        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
    )


def CreatedResponse(data):
    return Response(
        {"status": ResponseStatus.SUCCESS, "data": data}, status=status.HTTP_201_CREATED
    )
