from .models import Rating
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class RatingSerializer(serializers.ModelSerializer):
	user = serializers.PrimaryKeyRelatedField(
		queryset = User.objects.all(),
		default = serializers.CurrentUserDefault()
	)
	class Meta:
		model = Rating
		fields = ['user', 'menuitem_id', 'rating']
		validators = [UniqueTogetherValidator(
			queryset=Rating.objects.all(),
			fields=['menuitem_id', 'user']
		)]
		extra_kwargs = {
			'rating' : {'min_value':0,'max_value':5},}