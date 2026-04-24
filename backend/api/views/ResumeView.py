from psycopg.pq import error_message
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, status

from Api.models import Resume, ResumeSerializer, DetailsSerializer
from django.core.exceptions import ObjectDoesNotExist


class ResumeView(APIView):
    @staticmethod
    def get_all(request):
        objects = Resume.objects.all()
        return Response(ResumeSerializer(objects, many=True).data, status=status.HTTP_200_OK)

    @staticmethod
    def get_one(request, pk):
        try:
            resume = Resume.objects.get(id=pk)
            serializer = ResumeSerializer(resume)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(NotFound.default_detail, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get(request, pk=None):
        if pk:
            return ResumeView.get_one(request, pk)
        else:
            return ResumeView.get_all(request)

    @staticmethod
    def post(request):
        resume_serializer = ResumeSerializer(data=request.data)

        if resume_serializer.is_valid():
            resume_serializer.save()
        else:
            return Response(resume_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        details_serializer = DetailsSerializer(data={
            **request.data.pop('details'),
            'resume': resume_serializer.instance.id,
            'position': 0,
            'status': True,
            'locked': True
        })

        if details_serializer.is_valid():
            details_serializer.save()
            return Response(resume_serializer.data, status=status.HTTP_201_CREATED)
        else:
            resume_serializer.instance.delete()
            return Response(details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk = None):
        try:
            resume = Resume.objects.get(id=pk)
            serializer = ResumeSerializer(resume, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            err = NotFound.default_detail if pk else NotFound.default_detail + " Primary key field is empty"
            return Response(err, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def delete(request, pk = None):
        try:
            resume = Resume.objects.get(id=pk)
            resume.delete()
            return Response(status.HTTP_200_OK, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            err = NotFound.default_detail if pk else NotFound.default_detail + " Primary key is empty"
            return Response(err, status=status.HTTP_404_NOT_FOUND)