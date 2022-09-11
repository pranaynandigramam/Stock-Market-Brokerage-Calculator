from math import ceil
from math import floor


def intradayBrokerage(buyPrice: float, sellPrice: float, qty: int = 1):
    # Tax And Brokerage Percentages
    brokerage = 0.03 / 100
    stt_ctt = 0.025 / 100  # On Sell Side
    tc = 0.00345 / 100
    gst = 18 / 100  # On (Brokerage + tc)
    sebiCharges = 10 / 10000000
    stampCharges = 0.003 / 100  # On Buy Side

    # Buy And Sell Turnovers
    buyTurnover = round(buyPrice * qty, 2)
    sellTurnover = round(sellPrice * qty, 2)
    totalTurnover = round(buyTurnover + sellTurnover, 2)

    # Brokerage And Tax Calculations:
    brokerageValue = round(min(brokerage * buyTurnover, 20) + min(brokerage * sellTurnover, 20), 2)
    stt_ctt_value = ceil(stt_ctt * sellTurnover)
    tcValue = round((tc * buyTurnover) + (tc * sellTurnover), 2)
    buyBrokeragePlusTcValue = round(min(brokerage * buyTurnover, 20) + (tc * buyTurnover), 2)
    sellBrokeragePlusTcValue = round(min(brokerage * sellTurnover, 20) + (tc * sellTurnover), 2)
    gstValue = round((gst * buyBrokeragePlusTcValue) + (gst * sellBrokeragePlusTcValue), 2)
    sebiChargesValue = round((sebiCharges * buyTurnover) + (sebiCharges * sellTurnover), 2)
    stampChargesValue = round(stampCharges * buyTurnover, 2)

    totalBrokerageAndTax = round(brokerageValue + stt_ctt_value + tcValue + gstValue + sebiChargesValue + stampChargesValue, 2)
    breakEvenPoint = round(totalBrokerageAndTax / qty, 2)

    return totalBrokerageAndTax, breakEvenPoint


def equityDeliveryBrokerage(buyPrice: float, sellPrice: float, qty: int = 1):
    # Brokerage And Tax Percentages
    brokerage = 0
    stt_ctt = 0.1 / 100
    tc = 0.00345 / 100
    gst = 18 / 100  # On (Brokerage + tc)
    sebiCharges = 10 / 10000000
    stampCharges = 0.015 / 100  # On Buy Side

    # Buy And Sell Turnovers
    buyTurnover = buyPrice * qty
    sellTurnover = sellPrice * qty
    totalTurnover = buyTurnover + sellTurnover

    # Brokerage And Tax Calculations:
    stt_ctt_value = ceil((stt_ctt * buyTurnover) + (stt_ctt * sellTurnover))
    tcValue = (tc * buyTurnover) + (tc * sellTurnover)
    gstValue = gst * tcValue
    sebiChargesValue = (sebiCharges * buyTurnover) + (sebiCharges * sellTurnover)
    stampChargesValue = stampCharges * buyTurnover

    totalTaxAndBrokerage = round(stt_ctt_value + tcValue + gstValue + sebiChargesValue + stampChargesValue, 2)
    breakEvenPoint = round(totalTaxAndBrokerage / qty, 2)

    return totalTaxAndBrokerage, breakEvenPoint


def targetAndStopLoss(sharePrice: float,
                      budget: float,
                      profit: float,
                      loss: float, split: int = 1,
                      tradeDirection="buy",
                      orderType="mis",
                      cycles: int = 1,
                      specificShareTarget: float = 0):

    expectedCycleProfit = profit / cycles
    bearableCycleLoss = loss / cycles

    allottedCompanyBudget = budget / split
    expectedCompanyProfit = expectedCycleProfit / split
    bearableCompanyLoss = bearableCycleLoss / split

    noOfSharesCanBuy = 0

    if orderType == "cnc":
        noOfSharesCanBuy = allottedCompanyBudget / sharePrice
    elif orderType == "mis":
        noOfSharesCanBuy = allottedCompanyBudget / (0.2 * sharePrice)

    shareProfit = expectedCompanyProfit / noOfSharesCanBuy
    shareLoss = bearableCompanyLoss / noOfSharesCanBuy

    companyInvestment = sharePrice * noOfSharesCanBuy
    tempSellPrice = sharePrice + (expectedCompanyProfit / noOfSharesCanBuy)
    breakEvenPoint = 0

    if orderType == "cnc":
        breakEvenPoint = equityDeliveryBrokerage(sharePrice, tempSellPrice, noOfSharesCanBuy)[1]
    elif orderType == "mis":
        breakEvenPoint = intradayBrokerage(sharePrice, tempSellPrice, noOfSharesCanBuy)[1]

    sellPrice = sharePrice + breakEvenPoint


def cycleSplit(expectedProfit: float, bearableLoss: float, noOfCycles: int = 1):
    expectedCycleProfit = expectedProfit / noOfCycles
    bearableCycleLoss = bearableLoss / noOfCycles


def companySplit(budget: float, expectedProfit: float, bearableLoss: float, noOfCompanies: int = 1):
    allottedCompanyBudget = budget / noOfCompanies
    expectedCompanyProfit = expectedProfit / noOfCompanies
    bearableCompanyLoss = bearableLoss / noOfCompanies


def sharesAffordable(sharePrice: float, budget: float, expectedProfit: float, orderType: str = "cnc"):
    misBudget = budget * 5
    tempNoOfShares = 0

    if orderType == "cnc":
        tempNoOfShares = floor(budget / sharePrice)
    elif orderType == "mis":
        tempNoOfShares = floor(misBudget / sharePrice)

    expectedProfitPerShare = expectedProfit / tempNoOfShares
    sellPrice = sharePrice + expectedProfitPerShare
    brokerage = 0

    if orderType == "cnc":
        brokerage = equityDeliveryBrokerage(sharePrice, sellPrice, tempNoOfShares)[0]
    elif orderType == "mis":
        brokerage = intradayBrokerage(sharePrice, sellPrice, tempNoOfShares)[0]

    newBudget = budget - brokerage

    if orderType == "cnc":
        newBudget = budget - brokerage
    elif orderType == "mis":
        newBudget = misBudget - brokerage

    noOfShares = floor(newBudget / sharePrice)

    return noOfShares


def budget(budgetIssued):
    cncBudget = budgetIssued
    misBudget = cncBudget * 5

    return cncBudget, misBudget


def sharesAffordable2(sharePrice: float, budget: float):
    noOfShares = budget / sharePrice




