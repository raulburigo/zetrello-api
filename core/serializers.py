from rest_framework import serializers
from .models import Card, List


class CreateCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_list', 'title', 'description']


class CardDetailSerializer(serializers.ModelSerializer):
    card_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Card
        fields = [
            'id',
            'title',
            'description',
            'completed',
            'deadline',
            'card_list'
        ]

    def get_card_list(self, obj):
        return obj.card_list.name


class CardSerializer(serializers.ModelSerializer):
    has_description = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Card
        fields = [
            'id',
            'title',
            'has_description',
            'completed',
            'deadline',
            'position',
        ]

    def get_has_description(self, obj):
        return obj.description is not None


class UpdateCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        partial = True
        fields = [
            'title',
            'position',
            'card_list'
        ]


class ListSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = List
        fields = ['id', 'name', 'cards']

    def get_cards(self, obj):
        return CardSerializer(obj.card_set.all(), many=True).data
