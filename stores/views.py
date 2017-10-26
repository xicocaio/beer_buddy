from stores.models import PDV
from stores.serializers import PDVSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from pycpfcnpj import cpfcnpj


class PDVList(APIView):
    def get(self, request, format=None):
        pdvs = PDV.objects.all()
        serializer = PDVSerializer(pdvs, many=True)
        custom_data = {'pdvs': serializer.data}
        return Response(custom_data)

    def post(self, request, format=None):
        # make sure there only raw cnpj on DB
        # this way of handling objects is not good
        # it probably should be done on the serializer
        # tried, but did not work
        data = request.data
        document_clear = cpfcnpj.clear_punctuation(data['document'])
        data['document'] = document_clear

        serializer = PDVSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PDVDetail(APIView):
    def get_object(self, pk):
        try:
            return PDV.objects.get(pk=pk)
        except PDV.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pdv = self.get_object(pk)
        serializer = PDVSerializer(pdv)
        return Response(serializer.data)


class PDVSearch(APIView):
    def get(self, request, format=None):
        query_param = request.GET.get('longlat').split(',')

        long = float(query_param[0].strip())
        lat = float(query_param[1].strip())

        point = Point(long, lat)

        # select only PDVs that cover the location provided
        # and order them by distance, selecting only the nearest
        pdvs = PDV.objects.filter(coverageArea__contains=point) \
                   .annotate(distance=Distance('address', point)) \
                   .order_by('distance', 'id')[:1]

        # could return only a object but, to guarantee scalability
        # preferred to always use list
        serializer = PDVSerializer(pdvs, many=True)
        custom_data = {'pdvs': serializer.data}
        return Response(custom_data)
