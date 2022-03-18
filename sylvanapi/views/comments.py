
from django.forms import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sylvanapi.models import Player
from sylvanapi.models.comments import Comments
from sylvanapi.models.deck import Deck



class CommentView(ViewSet):
    """ Players VIEW"""

    def retrieve(self, request, pk):
        """Handle GET requests for single comment
        Returns:
            Response -- JSON serialized comment
        """
        try:
            comment = Comments.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all app players
        Returns:
            Response -- JSON serialized list of app players
        """
        comments = Comments.objects.all()
        deckId = self.request.query_params.get('deckId', None)
        if deckId is not None:
            comments = comments.filter(deck_id = deckId)
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        player = Player.objects.get(user=request.auth.user.id)
        comment = Comments.objects.create(
            comments = request.data["comment"],
            deck_id = request.data["deck_id"],
            player=player
        )
        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try: 
            comment.save()
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
         # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        """Handle DELETE requests for a single deck

        Returns:
            Response -- 200, 404, or 500 status code
        """
        
        comment = Comments.objects.get(pk=pk)
        comment.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, pk):
        """Handle PUT requests for a deck

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            player = Player.objects.get(user=request.auth.user)
            comment = Comments.objects.get(pk=pk)
            # Do mostly the same thing as POST, but instead of
            # creating a new instance of Game, get the game record
            # from the database whose primary key is `pk`
            # deck = Deck.objects.get(pk=pk)
            comment.comments = request.data["comments"]
            comment.deck_id = request.data["deck_id"]
            comment.player = player
                                
            comment.save()
        except Exception as ex:
            return HttpResponseServerError(ex)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    
    
class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for players
    """
    class Meta:
        model = Comments
        fields = "__all__"
        depth = 2