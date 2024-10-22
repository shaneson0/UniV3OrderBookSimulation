import math

def calculate_price_from_tick(tick):
    return 1.0001 ** tick

def calculate_sqrt_price_x96(price):
    return int(math.sqrt(price) * (2 ** 96))

def caculate_sqrt_price_from_tick(tick):
    # Step 1: Calculate price from tick
    price = calculate_price_from_tick(tick)
    
    # Step 2: Calculate sqrtPriceX96 from price
    calculated_sqrt_price_x96 = calculate_sqrt_price_x96(price)
    
    # Step 3: Compare calculated sqrtPriceX96 with given sqrtPriceX96
    return calculated_sqrt_price_x96

# Example usage
tick0 = -202850
tick1 = -211765
tick2 = -219100

given_sqrt_price_x96 = 1934304298358672824303116

print("tick0 sqrtPrice: ", caculate_sqrt_price_from_tick(tick0))
print("tick1 sqrtPrice: ", caculate_sqrt_price_from_tick(tick1))
print("tick2 sqrtPrice: ", caculate_sqrt_price_from_tick(tick2))

print("tick0 price: ", calculate_price_from_tick(tick0))
print("tick1 price: ", calculate_price_from_tick(tick1))
print("tick2 price: ", calculate_price_from_tick(tick2))


# 计算tick0对比tick1的涨幅
tick1_price = calculate_price_from_tick(tick1)
tick0_price = calculate_price_from_tick(tick0)
increase_percentage = ((tick0_price - tick1_price) / tick1_price) * 100

# 计算tick2对比tick1的跌幅
tick2_price = calculate_price_from_tick(tick2)
decrease_percentage = ((tick1_price - tick2_price) / tick1_price) * 100

print("tick0对比tick1的涨幅: ", increase_percentage, "%")
print("tick2对比tick1的跌幅: ", decrease_percentage, "%")



