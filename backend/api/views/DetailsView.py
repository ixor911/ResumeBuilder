from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, status

from Api.models import DetailsSerializer, Details
from django.core.exceptions import ObjectDoesNotExist


class DetailsView(APIView):
    @staticmethod
    def get_one(request, pk):
        try:
            details = Details.objects.get(resume=pk)
            serializer = DetailsSerializer(details)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(NotFound.default_detail, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_all(request):
        details = Details.objects.all()
        return Response(DetailsSerializer(details, many=True).data, status=status.HTTP_200_OK)

    @staticmethod
    def get(request, pk = None):
        if pk:
            return DetailsView.get_one(request, pk)
        else:
            return DetailsView.get_all(request)

    # @staticmethod
    # def post(request):
    #     serializer = DetailsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk = None):
        try:
            details = Details.objects.get(resume=pk)
            serializer_init = DetailsSerializer(details)
            serializer_new = DetailsSerializer(details, data={
                **serializer_init.data,
                **request.data
            })

            if serializer_new.is_valid():
                serializer_new.save()
                return Response(serializer_new.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer_new.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            err = NotFound.default_detail if pk else NotFound.default_detail + " Primary key field is empty"
            return Response(err, status=status.HTTP_404_NOT_FOUND)

    # @staticmethod
    # def delete(request, pk = None):
    #     try:
    #         details = Details.objects.get(id=pk)
    #         details.delete()
    #         Response(status.HTTP_200_OK, status=status.HTTP_200_OK)
    #     except ObjectDoesNotExist:
    #         err = NotFound.default_detail if pk else NotFound.default_detail + " Primary key field is empty"
    #         return Response(err, status=status.HTTP_404_NOT_FOUND)