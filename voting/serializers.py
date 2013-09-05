# -*- mode: python; coding: utf-8; -*-
from rest_framework import serializers
from .models import Vote, ViewsObj


class ItemViewSerializer(serializers.Serializer):
    id = serializers.Field(source='object_id')
    views = serializers.Field(source='views')

    class Meta:
        model = ViewsObj


class ItemVoteSerializer(serializers.Serializer):
    id = serializers.Field(source='object_id')
    score = serializers.Field(source='score')
    num_votes = serializers.Field(source='num_votes')

    class Meta:
        model = Vote


class ItemVoteDisableSerializer(serializers.Serializer):
    id = serializers.Field(source='object_id')

    class Meta:
        model = Vote