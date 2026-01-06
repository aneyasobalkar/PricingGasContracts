"""
The input parameters that should be taken into account for pricing are:  
- Injection dates.  
- Withdrawal dates. 
- The prices at which the commodity can be purchased/sold on those dates. 
- The rate at which the gas can be injected/withdrawn. 
- The maximum volume that can be stored. 
- Storage costs. 
"""
import numpy as np
import pandas as pd
from Logger import Logger

price_data = pd.read_csv("Data/pricing_forecast_results.csv")
best_IW_dates = pd.read_csv("Data/pricing_by_dates.csv")

def pricing_model(injection_dates, withdrawal_dates, price_data: pd.DataFrame, gas_rate, IW_rate, max_volume, storage_costs_per_month):
    volume = 0
    revenue = 0
    costs = 0
    all_dates = sorted(set(injection_dates).union(set(withdrawal_dates)))
    for date in all_dates:
        price = price_data.loc[price_data["Time"] == date, "Prediction"].iloc[0]
        #Buy on these dates
        if date in injection_dates:
            if (volume + gas_rate) <= max_volume:
                volume += gas_rate
                costs += (gas_rate * price) #buying gas
                injection_cost = gas_rate * IW_rate #cost of injecting gas into facility
                costs += injection_cost
                Logger.logger.info(f"\nVolume: {volume}\nRevenue: {revenue} \nCosts: {costs}")
            else:
                Logger.logger.info(f"We cannot buy on {date}.")
        #Sell on these dates
        elif date in withdrawal_dates:
            if (volume - gas_rate) >= 0:
                volume -= gas_rate
                revenue += (gas_rate * price)
                withdrawal_cost = gas_rate * IW_rate #cost of withdrawing gas from facility
                costs += withdrawal_cost
                Logger.logger.info(f"\nVolume: {volume}\nRevenue: {revenue} \nCosts: {costs}")
            else:
                Logger.logger.info(f"We cannot sell on {date}.")

    days = (max(pd.to_datetime(all_dates, unit='s', utc=True)) - min(pd.to_datetime(all_dates, unit='s', utc=True)))
    months = days.days//30
    total_storage_costs = storage_costs_per_month * months
    return revenue - costs - total_storage_costs

            

injection_dates = best_IW_dates["Injection Times"].to_list()
withdrawal_dates = best_IW_dates["Withdrawing Times"].to_list()
Logger.logger.info(f"The estimated contract value is {pricing_model(injection_dates, withdrawal_dates, price_data, 100, 0.1, 100000000000, 50)}")