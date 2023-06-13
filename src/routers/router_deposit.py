from fastapi import APIRouter
from typing import Dict
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
import calendar

from schema.deposit_api_schema import DepositInputSchema

router = APIRouter(prefix="/deposit_service")


@router.post("/calculate_deposit", response_model=Dict)
async def calculate_deposit(deposit: DepositInputSchema):
    # все числа переведены в Desimal для точности расчётов
    result_dict = {}
    months = Decimal(12).quantize(Decimal("1"))
    amount = Decimal(deposit.amount)
    rate = Decimal(deposit.rate/100).quantize(Decimal("1.0000"))
    date = datetime.strptime(deposit.date, "%d.%m.%Y").date()

    for month in range(deposit.periods):
        income = Decimal(amount * rate / months).quantize(Decimal("1.0000"))
        amount += income
        # по мере расчётов приход не округляется, но на выходе должно отдаваться корректное число с 2 знаками \
        # после запятой, поэтому отдаём округлённое
        result_dict[date.strftime('%d.%m.%Y')] = amount.quantize(Decimal("1.00"), ROUND_HALF_UP)
        # новую дату считаем по количеству дней следующего месяца
        days = calendar.monthrange(date.year, (date.month+1))[1]
        date = date + timedelta(days=days)

    return result_dict
