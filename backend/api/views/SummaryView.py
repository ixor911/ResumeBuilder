from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, status
from rest_framework.decorators import api_view

from Api.models import Summary, SummarySerializer
from django.core.exceptions import ObjectDoesNotExist

class SummaryView(APIView):
    @staticmethod
    def get_one(request, pk):
        try:
            summary = Summary.objects.get(id=pk)
            serializer = SummarySerializer(summary)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(NotFound.default_detail, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_all(request):
        objects = Summary.objects.all()
        return Response(SummarySerializer(objects, many=True).data, status=status.HTTP_200_OK)

    @staticmethod
    def get(request, pk = None):
        if pk:
            return SummaryView.get_one(request, pk)
        else:
            return SummaryView.get_all(request)

    @staticmethod
    def post(request):
        serializer = SummarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk = None):
        try:
            summary = Summary.objects.get(id=pk)
            serializer_init = SummarySerializer(summary)
            serializer_new = SummarySerializer(summary, data={
                **serializer_init.data,
                **request.data
            })

            if serializer_new.is_valid():
                serializer_new.save()
                return Response(serializer_new.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer_new.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response(NotFound.default_detail, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def delete(request, pk = None):
        try:
            summary = Summary.objects.get(id=pk)
            summary.delete()
            return Response(status.HTTP_200_OK, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(NotFound.default_detail, status=status.HTTP_404_NOT_FOUND)