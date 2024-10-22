import numpy as np

class UniswapV3PoolUtil:
    def __init__(self, tick_spacing):
        self.tick_spacing = tick_spacing

    @staticmethod
    def get_price_at_tick(tick):
        return 1.0001 ** tick

    def simulate_order_book(self, current_tick, liquidity, depth=10):
        order_book = {'bids': [], 'asks': []}
        
        # Simulate bids
        for i in range(1, depth + 1):
            tick = current_tick - i * self.tick_spacing
            price = self.get_price_at_tick(tick)
            quantity = liquidity / price
            order_book['bids'].append({'price': price, 'quantity': quantity})

        # Simulate asks
        for i in range(1, depth + 1):
            tick = current_tick + i * self.tick_spacing
            price = self.get_price_at_tick(tick)
            quantity = liquidity * price
            order_book['asks'].append({'price': price, 'quantity': quantity})

        return order_book

    def get_buy1_and_sell1_without_quantity(self, current_tick):
        buy1_tick = current_tick - self.tick_spacing
        sell1_tick = current_tick + self.tick_spacing
        buy1_price = self.get_price_at_tick(buy1_tick)
        sell1_price = self.get_price_at_tick(sell1_tick)
        return {'buy1': {'price': buy1_price}, 'sell1': {'price': sell1_price}}

    def get_buy1_and_sell1_with_quantity(self, current_tick, liquidity):
        buy1_tick = current_tick - self.tick_spacing
        sell1_tick = current_tick + self.tick_spacing
        buy1_price = self.get_price_at_tick(buy1_tick)
        sell1_price = self.get_price_at_tick(sell1_tick)
        buy1_quantity = liquidity / buy1_price
        sell1_quantity = liquidity * sell1_price
        return {'buy1': {'price': buy1_price, 'quantity': buy1_quantity}, 'sell1': {'price': sell1_price, 'quantity': sell1_quantity}}




# # Example usage
# liquidity = 146397912183698051832063671
# tick_spacing = 50
# current_tick = -212792

# pool = UniswapV3Pool(tick_spacing)
# order_book = pool.simulate_order_book(current_tick, liquidity)
# buy1_and_sell1 = pool.get_buy1_and_sell1(current_tick, liquidity)

# print("Order Book:")
# print("Bids:")
# for bid in order_book['bids']:
#     print(f"Price: {bid['price']}, Quantity: {bid['quantity']}")

# print("\nAsks:")
# for ask in order_book['asks']:
#     print(f"Price: {ask['price']}, Quantity: {ask['quantity']}")

# print("\nBuy1 and Sell1:")
# print(f"Buy1 - Price: {buy1_and_sell1['buy1']['price']}, Quantity: {buy1_and_sell1['buy1']['quantity']}")
# print(f"Sell1 - Price: {buy1_and_sell1['sell1']['price']}, Quantity: {buy1_and_sell1['sell1']['quantity']}")

