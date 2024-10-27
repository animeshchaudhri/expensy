from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Sum
import csv
from .models import Expense, ExpenseSplit
from .serializers import UserSerializer, ExpenseSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    @action(detail=False, methods=['get'])
    def user_expenses(self, request):
        user_email = request.query_params.get('email')
        if not user_email:
            return Response({"error": "Email parameter is required"})

        user = User.objects.filter(email=user_email).first()
        if not user:
            return Response({"error": "User not found"})

        expenses = Expense.objects.filter(splits__user=user)
        serializer = self.get_serializer(expenses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def download_balance_sheet(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['User', 'Total Paid', 'Total Owed', 'Net Balance'])
        
        users = User.objects.all()
        for user in users:
            paid = Expense.objects.filter(paid_by=user).aggregate(Sum('amount'))['amount__sum'] or 0
            owed = ExpenseSplit.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
            net_balance = paid - owed
            writer.writerow([user.email, paid, owed, net_balance])
        
        return response