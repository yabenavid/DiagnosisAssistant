# serializers.py
from rest_framework import serializers
from .models import Doctor, Belong
from managementhospital.models import Hospital
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False},
        }

    def validate(self, data):
        if not data.get('username'):
            data['username'] = data.get('email')  # Use email as username
        return data

# class CredentialSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Credential
#         fields = ['email', 'password']
#         extra_kwargs = {
#             'password': {'required': False, 'allow_blank': True},  # Make that field optional
#         }

#     def get_fields(self):
#         fields = super().get_fields()
#         fields['email'].validators = []  # Disable automatic validation
#         return fields

#     def to_representation(self, instance):
#         # Get the original representation
#         representation = super().to_representation(instance)
        
#         # Always remove the 'password' field from the representation
#         representation.pop('password', None)
        
#         return representation
    
#     def validate(self, data):   
#         # Required password field in creation requests
#         if self.context['request'].method == 'POST':
#             if not data.get('password'):
#                 raise serializers.ValidationError({"password": "Este campo es obligatorio."})
        
#         return data


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    hospital = serializers.CharField(write_only=True)
    hospital_id = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'last_name', 'second_last_name', 'specialism', 'user', 'hospital', 'hospital_id']

    def get_hospital_id(self, obj):
        belong = Belong.objects.filter(doctor=obj).first()
        return belong.hospital.id if belong else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['hospital'] = representation.pop('hospital_id', None)
        return representation

    def validate(self, data):
        user_data = data.get('user')
        if not user_data:
            return data

        email = user_data.get('email')
        instance = getattr(self, 'instance', None)

        if instance and instance.user.email == email:
            return data

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Este email ya está registrado."})

        hospital_id = data.get('hospital')
        if hospital_id and not Hospital.objects.filter(id=hospital_id).exists():
            raise serializers.ValidationError({"hospital": "El hospital especificado no existe."})

        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        hospital_id = validated_data.pop('hospital')

        # Si no se proporciona un username, usa el email como username
        if not user_data.get('username'):
            user_data['username'] = user_data['email']

        # Create a new django User
        user = User.objects.create_user(
            username=user_data['email'],  # Usa el username proporcionado o el email
            email=user_data['email'],
            password=user_data['password']
        )

        # Create Doctor related to the User
        doctor = Doctor.objects.create(user=user, **validated_data)

        # Create the relationship with the Hospital
        Belong.objects.create(doctor=doctor, hospital_id=hospital_id)

        return doctor

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        hospital_id = validated_data.pop('hospital', None)

        # Update Doctor fields
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.second_last_name = validated_data.get('second_last_name', instance.second_last_name)
        instance.specialism = validated_data.get('specialism', instance.specialism)

        if user_data:
            user = instance.user
            new_email = user_data.get('email', user.email)

            user.email = new_email
            user.username = new_email

            if 'password' in user_data and user_data['password']:
                user.set_password(user_data['password'])  # Hash the password

            user.save()

        if hospital_id:
            if not Hospital.objects.filter(id=hospital_id).exists():
                raise serializers.ValidationError({"hospital": "El hospital especificado no existe."})

            belong, created = Belong.objects.get_or_create(doctor=instance)
            belong.hospital_id = hospital_id
            belong.save()

        instance.save()
        return instance