"""View module for handling requests about game types"""
from django.forms import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sylvanapi.models import Event, Player
from rest_framework.decorators import action

class EventView(ViewSet):
    """Level up game types view"""
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        player = Player.objects.get(user=request.auth.user)
        
        event = Event.objects.create(
            name = request.data["name"],
            date = request.data["date"],
            time = request.data["time"],
            venue = request.data["venue"],
            address = request.data["address"],
            description=request.data["description"],
            organizer=player
        )
        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try: 
            event.save()
            serializer = EventSerializer(event)
            return Response(serializer.data)
         # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk):
        """Handle PUT requests for a event
        Returns:
            Response -- Empty body with 204 status code
        """
        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Event, get the event record
        # from the database whose primary key is `pk`
        try:
            event = Event.objects.get(pk=pk)
            
            event.name = request.data["name"]
            event.date = request.data["date"]
            event.time = request.data["time"]
            event.venue = request.data["venue"]
            event.address = request.data["address"]
            event.description = request.data["description"]

            event.save()

            # 204 status code means everything worked but the
            # server is not sending back any data in the response
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response ({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types
        Returns:
            Response -- JSON serialized list of game types
        """
        events = Event.objects.all()
        player = Player.objects.get(user=request.auth.user)
        
        # Set the `joined` property on every event
        for event in events:
    # Check to see if the player is in the attendees list on the event
            event.joined = player in event.attendees.all()

               
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        """Delete Request"""
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True) #detail = True basically means to expect a pk 
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        player = Player.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(player)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        player = Player.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(player)
        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = ("__all__")
        depth = 2