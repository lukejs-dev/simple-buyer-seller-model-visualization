import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import streamlit as st
import random

import src.classes as classes

st.title("Simple Buyer-Seller Model Visualization")

n_buyers = st.sidebar.slider("Number of Buyers", 10, 500, 100)
n_sellers = st.sidebar.slider("Number of Sellers", 10, 500, 100)
buyer_minimum_price = st.sidebar.slider("Buyer Lowest Price", 50, 100, 50)
buyer_maximum_price = st.sidebar.slider("Buyer Maximum Price", 50, 100, 100)
seller_minimum_price = st.sidebar.slider("Seller Lowest Price", 60, 110, 60)
seller_maximum_price = st.sidebar.slider("Seller Maximum Price", 60, 110, 110)
n_iterations = st.sidebar.number_input("Number of Days (Iterations)", 50)

# Create market!1!!
market = classes.Market(n_buyers, n_sellers, buyer_minimum_price, buyer_maximum_price, seller_minimum_price, seller_maximum_price)

# Keep track of average prices per day
avg_prices_over_time = []

plt.figure(figsize=(8, 4))
plt.xlabel("Day")
plt.ylabel("Average Transaction Price")
plt.xlim([0, n_iterations])
plt.ylim([max(buyer_minimum_price, seller_minimum_price), max(buyer_maximum_price, seller_maximum_price)])
plt.title("Average Transaction Price Over Time")
# plt.text(1, 0.95, "Average Price: %.4f" % (sum(avg_prices_over_time) / min(len(avg_prices_over_time), 1)), fontsize=10)

chartplot = st.pyplot(plt)

progress_bar = st.progress(0)

if st.sidebar.button("Run Simulation"):
    # List is inside button click, resets each time a new simulation
    avg_prices_over_time = []

    for i in range(n_iterations):
        # Replenish market for new day to create new agents in an iteration
        market = classes.Market(n_buyers, n_sellers, buyer_minimum_price, buyer_maximum_price, seller_minimum_price, seller_maximum_price)

        # Run one day of market
        market.run_simulation_step()

        # Calculate average price for days transactions
        if market.transaction_history:
            avg_price_today = sum(market.transaction_history) / len(market.transaction_history)
            avg_prices_over_time.append(avg_price_today)

        plt.figure(figsize=(8, 4))
        plt.xlabel("Day")
        plt.ylabel("Average Transaction Price")
        plt.xlim([0, n_iterations])

        # Set y-limits
        price_range = (min(buyer_minimum_price, seller_minimum_price), max(buyer_maximum_price, seller_maximum_price))
        plt.ylim(price_range)
        plt.title("Market Price Convergence")

        plt.plot(avg_prices_over_time)

        if avg_prices_over_time:
            current_avg = avg_prices_over_time[-1]
            plt.text(1, price_range[1] * 0.95, f"Last Avg Price: ${current_avg:.2f}", fontsize=10)
        
        chartplot.pyplot(plt)
        plt.close("all")

        progress_bar.progress((i + 1.0) / n_iterations)
