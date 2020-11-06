from rest_framework.views import APIView
from rest_framework import authentication, permissions
from .models import Card, List
from rest_framework.response import Response
from .serializers import (
    CardSerializer,
    CreateCardSerializer,
    ListSerializer,
    CardDetailSerializer,
    UpdateCardSerializer
)
from django.core.exceptions import ObjectDoesNotExist


class Cards(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data, status=200)

    def post(self, request, format=None):
        new_card = request.data
        serializer = CreateCardSerializer(data=new_card)
        if serializer.is_valid():
            card_list = serializer.validated_data.get('card_list')
            list_length = card_list.card_set.count()
            serializer.save(position=list_length)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class CardDetail(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def _get_card(self, _id):
        try:
            return Card.objects.filter(id=_id).get()
        except ObjectDoesNotExist:
            return

    def get(self, request, id, format=None):
        card = self._get_card(id)
        if not card:
            return Response({"message": "card does not exist"}, status=404)
        serializer = CardDetailSerializer(card)
        return Response(serializer.data, status=200)

    def patch(self, request, id, format=None):
        card = self._get_card(id)
        if not card:
            return Response({"message": "card does not exist"}, status=404)
        original_list = card.card_list
        original_position = card.position
        serializer = UpdateCardSerializer(card, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            new_position = serializer.validated_data.get('position')
            new_list = serializer.validated_data.get('card_list')
            if new_list and original_list != new_list:
                self._update_list_positions(original_list)
                self._update_list_positions(new_list)
            elif new_position and new_position != original_position:
                self._update_list_positions(new_list)
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        card = self._get_card(id)
        if not card:
            return Response({"message": "card does not exist"}, status=404)
        original_list = card.card_list
        card.delete()
        self._update_list_positions(original_list)
        return Response({"message": "card successfull deleted"}, status=200)

    def _update_list_positions(self, card_list):
        counter = 0
        for card in card_list.card_set.all():
            card.position = counter
            counter += 1
            card.save()
        return


class Lists(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        lists = List.objects.all()
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data, status=200)

    def post(self, request, format=None):
        new_list = request.data
        serializer = ListSerializer(data=new_list)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
