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

    def calculate_tokens(self, L, P_low, P_high):
        token0 = L * (1 / (P_low ** 0.5) - 1 / (P_high ** 0.5))
        token1 = L * (P_high ** 0.5 - P_low ** 0.5)
        return token0, token1

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

        (buy1_quantity, sell1_quantity) = self.calculate_tokens(liquidity, buy1_price, sell1_price)
        return {'buy1': {'price': buy1_price, 'quantity': buy1_quantity}, 'sell1': {'price': sell1_price, 'quantity': sell1_quantity}}

    def get_buy_and_sell_with_quantity_duringTicks(self, lowerTick, upperTick, liquidity):
        lower_price = self.get_price_at_tick(lowerTick)
        upper_price = self.get_price_at_tick(upperTick)
        (buy1_quantity, sell1_quantity) = self.calculate_tokens(liquidity, lower_price, upper_price)
        return {'buy1': {'lower_price': lower_price, 'quantity': buy1_quantity}, 'sell1': {'upper_price': upper_price, 'quantity': sell1_quantity}}

