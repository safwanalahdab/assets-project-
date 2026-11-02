from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsITStaffOrReadOnly
from rest_framework.response import Response
from inventory.models import Asset
from .serializers import AssetModelSerializer, AssetCreateUpdateModelSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated, IsITStaffOrReadOnly])
def asset_list_create_api(request):
    if request.method == "GET":
        assets = Asset.objects.all()
        serializer = AssetModelSerializer(assets, many=True)
        return Response(serializer.data)

    serializer = AssetCreateUpdateModelSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    asset = serializer.save()
    output = AssetModelSerializer(asset, many=False)

    return Response(output.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated, IsITStaffOrReadOnly])
def asset_detail_api(request, pk):
    asset = get_object_or_404(Asset, pk=pk)

    if request.method == "GET":
        serializer = AssetModelSerializer(asset, many=False)
        return Response(serializer.data)
    serializer = AssetCreateUpdateModelSerializer(asset, data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.save()
    seri = AssetModelSerializer(data, many=False)
    return Response(seri.data, status=status.HTTP_200_OK)
