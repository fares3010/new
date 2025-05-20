from rest_framework import serializers
from .models import Agent

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at', 'agent_id', 'is_deleted')
        extra_kwargs = {
            'visibility': {'required': True},
            'name': {'required': True},
            'description': {'required': True}
        }

    def validate_visibility(self, value):
        valid_choices = ['public', 'private']
        if value not in valid_choices:
            raise serializers.ValidationError(f"Visibility must be one of {valid_choices}")
        return value

    def validate_name(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long")
        return value.strip()

    def validate_description(self, value):
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters long")
        return value.strip()

    def validate(self, data):
        """
        Validate the entire data set.
        """
        # Remove validation methods for read-only fields since they're handled by the model
        # and Meta.read_only_fields
        return data
