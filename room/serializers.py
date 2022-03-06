from rest_framework import serializers


class BorrowTimeSerializer(serializers.Serializer):
    room = serializers.CharField(max_length=10)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    borrower = serializers.CharField()
    borrow_reason = serializers.CharField()


class RoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)
    location = serializers.CharField(max_length=30)
    contain_num = serializers.IntegerField()
