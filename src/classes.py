import random

class Agent:
    def __init__(self, agent_type, reservation_price):
        self.agent_type = agent_type
        self.price = reservation_price

class Market:
    def __init__(self, n_buyers, n_sellers, low_buy, high_buy, low_sell, high_sell):
        self.buyers = [Agent('buyer', random.uniform(low_buy, high_buy)) for _ in range(n_buyers)]
        self.sellers = [Agent('seller', random.uniform(low_sell, high_sell)) for _ in range(n_sellers)]
        self.transaction_history = []

    def run_simulation_step(self):
        if not self.buyers or not self.sellers:
            return
        
        # Shuffle agents for random matching
        random.shuffle(self.buyers)
        random.shuffle(self.sellers)

        successful_buyers = []
        successful_sellers = []

        # Match buyers and sellers for 1 on 1
        num_pairs = min(len(self.buyers), len(self.sellers))
        for i in range(num_pairs):
            buyer = self.buyers[i]
            seller = self.sellers[i]

            # Check if transaction is possible
            if buyer.price >= seller.price:
                # Make deal
                transaction_price = (buyer.price + seller.price) / 2
                self.transaction_history.append(transaction_price)

                # Mark agents for removal
                successful_buyers.append(buyer)
                successful_sellers.append(seller)

        # Remove agents who made deal so they dont trade again in step
        self.buyers = [b for b in self.buyers if b not in successful_buyers]
        self.sellers = [s for s in self.sellers if s not in successful_sellers]
