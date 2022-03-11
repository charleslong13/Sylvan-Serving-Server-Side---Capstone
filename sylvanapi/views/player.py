from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from sylvanapi.models import Player



class PlayerView(ViewSet):
    """SHOTGUN APP USERS VIEW"""

    def retrieve(self, request, pk):
        """Handle GET requests for single player
        Returns:
            Response -- JSON serialized player
        """
        
        player = Player.objects.get(pk=pk)
        serializer = PlayerSerializer(player)
        return Response(serializer.data)
        

    def list(self, request):
        """Handle GET requests to get all app players
        Returns:
            Response -- JSON serialized list of app players
        """
        player = Player.objects.all()
        serializer = PlayerSerializer(player, many=True)
        return Response(serializer.data)
    
class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for app users
    """
    class Meta:
        model = Player
        fields = "__all__"
        depth = 3