from dashboard.models import Investment
from datetime import timedelta
from django.utils import timezone
from django.db.models import F


def update_wallet_balance():
    # Get investments older than 14 days
    threshold_date = timezone.now() - timedelta(days=14)
    recent_investments = Investment.objects.filter(created_at__gte=threshold_date)

    for investment in recent_investments:
        print(investment.user.email)
        # Calculate 20% of the investment amount
        bonus_amount = investment.amount * 0.20

        # Update the user's wallet balance
        investment.user.wallet_balance = F("wallet_balance") + bonus_amount
        investment.user.save()

    print("Successfuly Updated Balances")
