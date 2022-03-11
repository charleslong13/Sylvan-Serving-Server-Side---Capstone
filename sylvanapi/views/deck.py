"""View module for handling requests about decks"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sylvanapi.models import Player, Deck, PlayStyle

class DeckViewSet(ViewSet):
    """Deck list view"""
    
    def create(self, request):
        
        """Handle Post operations
        Returns: Response -- JSON serialized deck instance
        """
        
        player = Player.objects.get(user=request.auth.user)
        play_style = PlayStyle.objects.get(pk=request.data["playStyle"]["id"])
       
        # Create a new Python instance of the Deck class
        # and set its properties from what was sent in the
        # body of the request from the client.
        deck = Deck.objects.create(
            title = request.data["title"],
            commander = request.data["commander"],
            creatures = request.data["creatures"],
            artifacts = request.data["artifacts"],
            enchantments = request.data["enchantments"],
            instants = request.data["instants"],
            sorceries = request.data["sorceries"],
            lands = request.data["lands"],
            wins = request.data["wins"],
            losses = request.data["losses"],
            powerLevel = request.data["powerLevel"],
            primer = request.data["primer"],
            player = player,
            playStyle = play_style
        )
        
        try:
            deck.save()
            serializer = DeckSerializer(deck)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        """Handle GET requests to decks resource
        Returns: Response -- JSON serialized list of games 
        """
        #get all deck records from the database
        decks = Deck.objects.all()
        play_style = self.request.query_params.get('type', None)
        if play_style is not None:
            decks = decks.filter(play_style__id=play_style)
        
        serializer = DeckSerializer(decks, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """Handle GET requests for a single deck

        Returns:
            Response -- JSON serialized deck instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/decks/2
            #
            # The `2` at the end of the route becomes `pk`
            deck = Deck.objects.get(pk=pk)
            serializer = DeckSerializer(deck, context={'request': request})
            return Response(serializer.data)
        except Deck.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def update(self, request, pk):
        """Handle PUT requests for a deck

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            player = Player.objects.get(user=request.auth.user)

            # Do mostly the same thing as POST, but instead of
            # creating a new instance of Game, get the game record
            # from the database whose primary key is `pk`
            deck = Deck.objects.get(pk=pk)
            deck.title = request.data["title"]
            deck.commander = request.data["commander"]
            deck.artifacts = request.data["artifacts"]
            deck.enchantments = request.data["enchantments"]
            deck.instants = request.data["instants"]
            deck.sorceries = request.data["sorceries"]
            deck.lands = request.data["lands"]
            deck.wins = request.data["wins"]
            deck.losses = request.data["losses"]
            deck.power_level = request.data["powerLevel"]
            deck.primer = request.data["primer"]
            deck.player = player
                                #
            play_style = PlayStyle.objects.get(pk=request.data["playStyle"]["id"])
            deck.play_style = play_style
            deck.save()
        except Exception as ex:
            return HttpResponseServerError(ex)
        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    def destroy(self, request, pk):
        """Handle DELETE requests for a single deck

        Returns:
            Response -- 200, 404, or 500 status code
        """
        
        deck = Deck.objects.get(pk=pk)
        deck.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class DeckSerializer(serializers.ModelSerializer):
    """JSON serializer for decks"""
    class Meta:
        model = Deck
        fields = "__all__"
        depth = 2