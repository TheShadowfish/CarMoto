from rest_framework import serializers
from vehicle.models import Car, Moto, Mileage
from vehicle.validators import TitleValidator


class MileageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mileage
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    last_mileage = serializers.IntegerField(source='mileage.all.first.mileage', read_only=True)
    mileage = MileageSerializer(many=True, read_only=True)
    class Meta:
        model = Car
        fields = '__all__'


class MotoSerializer(serializers.ModelSerializer):
    last_mileage = serializers.SerializerMethodField()
    class Meta:
        model = Moto
        fields = '__all__'
        validators = [
            TitleValidator(field='title'),
            serializers.UniqueTogetherValidator(fields=['title', 'description'], queryset=Moto.objects.all())
        ]

    def get_last_mileage(self, instance):
        if instance.mileage.all().first():
            return instance.mileage.all().first().mileage
        else:
            return 0


class MotoMileageSerializer(serializers.ModelSerializer):
    moto = MotoSerializer()
    class Meta:
        model = Mileage
        fields = ('mileage', 'year', 'moto',)
        validators = [
            TitleValidator(field='title'),
            serializers.UniqueTogetherValidator(fields=['title', 'description'], queryset=Moto.objects.all())
        ]


class MotoCreateSerializer(serializers.ModelSerializer):
    mileage = MileageSerializer(many=True)
    class Meta:
        model = Moto
        fields = '__all__'
        validators=[
            TitleValidator(field='title'),
            serializers.UniqueTogetherValidator(fields=['title','description'], queryset=Moto.objects.all())
        ]

    def create(self, validated_data):
        mileage = validated_data.pop('mileage')

        moto_item = Moto.objects.create(**validated_data)

        for m in mileage:
            Mileage.objects.create(**m, moto=moto_item)

        return moto_item
