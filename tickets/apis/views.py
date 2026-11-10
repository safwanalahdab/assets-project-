from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from tickets.models import Ticket ,TicketComment
from .permissions import is_staff
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    TicketCreateInputSerializer,
    TicketStatusFilterInputSerializer,
    TicketModelSerializer,
    TicketUpdateInputSerializer,
    TicketCommentModelSerializer,
    TicketCommentCreateInputSerializer
)
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def ticket_list_create_api(request):
    user = request.user
    if request.method == "GET":
        if is_staff(user):
            ticket = Ticket.objects.all()
        else:
            ticket = Ticket.objects.filter(creator=user)

        filters = TicketStatusFilterInputSerializer(data=request.query_params)
        filters.is_valid(raise_exception=True)
        if "status" in filters.validated_data:
            ticket = ticket.filter(status=filters.validated_data["status"])
        serilizer = TicketModelSerializer(ticket, many=True)
        return Response(serilizer.data, status=status.HTTP_200_OK)

    seralizer = TicketCreateInputSerializer(
        data=request.data, context={"request": request}
    )
    seralizer.is_valid(raise_exception=True)
    data = seralizer.save(creator=request.user)
    output = TicketModelSerializer(data, many=False)
    return Response(output.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "DELETE", "PATCH"])
@permission_classes([IsAuthenticated])
def ticket_detail_update_delete_api(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    user = request.user
    if ticket.creator_id != user.id and not is_staff(user):
        raise PermissionDenied()

    if request.method == "PATCH":
        serializer = TicketUpdateInputSerializer(
            ticket, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        output = TicketModelSerializer(data, many=False)
        return Response(output.data, status=status.HTTP_200_OK)

    if request.method == "GET":
        serializer = TicketModelSerializer(ticket, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    ticket.delete()
    return Response({"Message" : "تم الحذف بنجاح"},status=status.HTTP_204_NO_CONTENT)


@api_view(["GET","POST"]) 
@permission_classes([IsAuthenticated])
def ticket_comments_list_create_api(request,pk) : 
    ticket = get_object_or_404(Ticket,pk=pk)
    user = request.user
    if not is_staff(user) and ticket.creator_id != user.id : 
        raise PermissionDenied()
    
    if request.method == "GET" : 
        if is_staff(user) : 
            comments = TicketComment.objects.filter(ticket=ticket) 
        else : 
            comments = TicketComment.objects.filter(ticket=ticket,is_internal=False)
        output = TicketCommentModelSerializer(comments,many=True)
        return Response(output.data,status=status.HTTP_200_OK)

    context = {
        "request" : request ,
        "ticket" : ticket
    }
    serializer = TicketCommentCreateInputSerializer(data=request.data,context=context)
    serializer.is_valid(raise_exception=True) 
    comment = serializer.save(author=user,ticket=ticket)
    output = TicketCommentModelSerializer(comment)
    return Response(output.data,status=status.HTTP_201_CREATED)

 


        