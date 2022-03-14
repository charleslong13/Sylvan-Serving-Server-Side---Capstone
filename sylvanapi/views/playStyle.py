"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from sylvanapi.models import PlayStyle


class PlayStyleView(ViewSet):
    """Sylvan API PlayStyles"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            playStyle = PlayStyle.objects.get(pk=pk)
            serializer = PlayStyleSerializer(playStyle, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        playStyles = PlayStyle.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PlayStyleSerializer(
            playStyles, many=True, context={'request': request})
        return Response(serializer.data)
    
class PlayStyleSerializer(serializers.ModelSerializer):
    """JSON serializer for game types

    Arguments:
        serializers
    """
    class Meta:
        model = PlayStyle
        fields = "__all__"