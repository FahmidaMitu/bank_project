from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from .forms import UserRegistrationForm, TransactionForm
from .models import BankAccount, Transaction

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            holder_name = f"{user.first_name} {user.last_name}".strip() or user.username
            BankAccount.objects.create(user=user, account_holder_name=holder_name)

            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    account = request.user.account
    transactions = account.transactions.all()

    total_deposits = transactions.filter(transaction_type='DEPOSIT').aggregate(Sum('amount'))['amount__sum'] or 0
    total_withdrawals = transactions.filter(transaction_type='WITHDRAWAL').aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'account': account,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'total_transactions': transactions.count()
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def deposit_view(request):
    account = request.user.account
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()

            Transaction.objects.create(
                account=account,
                transaction_type='DEPOSIT',
                amount=amount,
                balance_after_transaction=account.balance
            )
            messages.success(request, f"Deposited ${amount:.2f} successfully!")
            return redirect('dashboard')
    else:
        form = TransactionForm()

    return render(request, 'accounts/deposit.html', {'form': form})


@login_required
def withdraw_view(request):
    account = request.user.account
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            if amount > account.balance:
                messages.error(request, "Insufficient balance! Overdraft not allowed.")
            else:
                account.balance -= amount
                account.save()

                Transaction.objects.create(
                    account=account,
                    transaction_type='WITHDRAWAL',
                    amount=amount,
                    balance_after_transaction=account.balance
                )
                messages.success(request, f"Withdrew ${amount:.2f} successfully!")
                return redirect('dashboard')
    else:
        form = TransactionForm()

    return render(request, 'accounts/withdraw.html', {'form': form})


@login_required
def transaction_history_view(request):
    account = request.user.account
    transactions = account.transactions.all()

    tx_type = request.GET.get('type', '').strip()
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()

    
    if tx_type:
        transactions = transactions.filter(transaction_type=tx_type)

    if start_date and end_date:
        transactions = transactions.filter(timestamp__date__range=[start_date, end_date])
    elif start_date:
        transactions = transactions.filter(timestamp__date=start_date)
    elif end_date:
        transactions = transactions.filter(timestamp__date=end_date)

    paginator = Paginator(transactions, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'accounts/transactions.html', {
        'page_obj': page_obj,
        'selected_type': tx_type,
        'start_date': start_date,
        'end_date': end_date,
    })