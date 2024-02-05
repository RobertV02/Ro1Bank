from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from decimal import Decimal
from .form import RegistrationForm, LoginForm
from .models import Balance, Check
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout
from .serializers import UserSerializer, CheckSerializer


@login_required(login_url='/api/auth/log/')
def logout_v(request):
    try:
        logout(request)
    except:
        pass
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def log(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return Response({"status": "ok"})
        else:
            return Response({"err": "error "})
    else:
        return Response({"err": "error"})

@api_view(['POST'])
def reg(request):
    if request.method == 'POST':
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if username and password:

                user = User.objects.create_user(username=username, password=password)
                balance = Balance(user=user, balance_amount=1000)
                balance.save()
                # Авторизуем пользователя
                auth_login(request, user)

                # Возвращаем ответ с JSON-объектом
                return Response({"status": "ok"})
            else:
                # Возвращаем ответ с ошибкой в формате JSON
                return Response({"error": "Invalid username or password"})
        except:
            return JsonResponse({"error": "There is already a user with this name"})


@login_required(login_url='/api/auth/log/')
@api_view(['GET'])
def get_profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response({'user': serializer.data,
                     'balance': Balance.objects.get(user=user).balance_amount,
                     'check': CheckSerializer(Check.objects.filter(user=user), many=True).data,
                     })

@api_view(['GET'])
def get_user_balances(request):
    balances = Balance.objects.all()
    user_balances = {balance.user.username: balance.balance_amount for balance in balances}
    return JsonResponse(user_balances)



@login_required(login_url='/api/auth/log/')
@api_view(['POST'])
def translate(request):
    if request.method == 'POST':
        try:
            user = request.user
            send_user = request.data.get('send_user')
            amount = Decimal(request.data.get('amount'))

            if send_user and amount and amount > 0:

                balance = Balance.objects.filter(user=user).first()

                if balance.balance_amount >= Decimal(amount):



                    send_user_name = request.data.get('send_user')

                    send_user = User.objects.get(username=send_user_name)
                    balance.balance_amount -= amount

                    balance.save()
                    balance = Balance.objects.filter(user=send_user).first()
                    balance.balance_amount += amount

                    balance.save()
                    check = Check(user=user,
                                  amount=amount,
                                  description=str(user.username) + ' перевёл ' + send_user_name + ' ' + str(amount)
                                  )
                    check.save()
                    return Response({"status": "ok"})
                else:
                    return Response({"error": "Недостаточно средств"})
            return Response({"error": "Неверно введена сумма, ваш баланс: "+
                                      str(Balance.objects.filter(user=user).first().balance_amount)})
        except:
            return Response({"error": "Неверно указан пользователь или сумма перевода не корректна"})