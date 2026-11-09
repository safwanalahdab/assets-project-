from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from models import Ticket
from .permissions import is_staff 
from rest_framework.response import Response
from rest_framework import status
from serializers import TicketCreateInputSerializer,TicketStatusFilterInputSerializer ,TicketModelSerializer

@api_view(["GET","POST"]) 
@permission_classes([IsAuthenticated])
def ticket_list_create_api(request) :
    user = request.user 
    if request.method == "GET" :
         if is_staff(user) : 
              ticket = Ticket.objects.all()
         else :
              ticket = Ticket.objects.filter(creator=user)

         filters = TicketStatusFilterInputSerializer(data=request.query_params)
         filters.is_valid(raise_exception=True)
         if "status" in filters.validated_data : 
            ticket = ticket.filter(status=filters.validated_data["status"])
         serilizer = TicketModelSerializer(ticket,many=True)
         return Response(serilizer.data, status=status.HTTP_200_OK)


    seralizer = TicketCreateInputSerializer(data=request.data,context={"request": request}) 
    seralizer.is_valid(raise_exception=True) 
    data = seralizer.save(creator=request.user) 
    output = TicketModelSerializer(data,many=False) 
    return Response(output.data,status=status.HTTP_201_CREATED)
        
    
    
        
     