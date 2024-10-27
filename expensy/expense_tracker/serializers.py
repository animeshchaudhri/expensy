from rest_framework import serializers
from .models import Profile, Expense, ExpenseSplit
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404

class UserSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(source='profile.mobile')
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'mobile']
        
    @transaction.atomic
    def create(self, validated_data):
       
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(
            username=validated_data['email'],
            **validated_data
        )
        Profile.objects.create(user=user, **profile_data)
        return user

class ExpenseSplitSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True)
    
    class Meta:
        model = ExpenseSplit
        fields = ['user_email', 'amount', 'percentage']

class ExpenseSerializer(serializers.ModelSerializer):
    splits = ExpenseSplitSerializer(many=True)
    paid_by_email = serializers.EmailField(write_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'title', 'amount', 'paid_by_email', 
                  'split_type', 'splits', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        split_type = data['split_type']
        splits = data['splits']
        amount = data['amount']

    
        if split_type == 'PERCENTAGE':
            total_percentage = sum(split['percentage'] or 0 for split in splits)
            if total_percentage != 100:
                raise serializers.ValidationError("Percentages must sum to 100%")
        elif split_type == 'EXACT':
            total_split = sum(split['amount'] or 0 for split in splits)
            if total_split != amount:
                raise serializers.ValidationError("Split amounts must equal total amount")
        return data

    @transaction.atomic
    def create(self, validated_data):
        splits_data = validated_data.pop('splits')
        paid_by_email = validated_data.pop('paid_by_email')
        
        paid_by = get_object_or_404(User, email=paid_by_email)

        expense = Expense.objects.create(paid_by=paid_by, **validated_data)


        if expense.split_type == 'EQUAL':
            split_amount = expense.amount / len(splits_data)  
            for split_data in splits_data:
                user_email = split_data.pop('user_email')
                user = get_object_or_404(User, email=user_email)
                ExpenseSplit.objects.create(
                    expense=expense,
                    user=user,
                    amount=split_amount,
                    percentage=100 / len(splits_data)  
                )
        elif expense.split_type == 'EXACT':
            for split_data in splits_data:
                user_email = split_data.pop('user_email')
                user = get_object_or_404(User, email=user_email)
                amount = split_data['amount']

                percentage = (amount / expense.amount) * 100

                ExpenseSplit.objects.create(
                    expense=expense,
                    user=user,
                    amount=amount,
                    percentage=percentage  
                )
        elif expense.split_type == 'PERCENTAGE':
            for split_data in splits_data:
                user_email = split_data.pop('user_email')
                user = get_object_or_404(User, email=user_email)
                split_data['amount'] = (
                    expense.amount * split_data['percentage'] / 100
                )
                ExpenseSplit.objects.create(
                    expense=expense,
                    user=user,
                    **split_data
                )

        return expense
