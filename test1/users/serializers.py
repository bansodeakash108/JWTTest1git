from rest_framework.serializers import ModelSerializer
from .models import User

class serialize(ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email','password']
        extra_fields={'password':{'write_only':True}}


    def create(self, validated_data):
        password=validated_data.pop('password')
        instance=self.Meta.model(**validated_data)
        if instance.check_password(password):
            instance.set_password(password)
        instance.save()
        return instance
