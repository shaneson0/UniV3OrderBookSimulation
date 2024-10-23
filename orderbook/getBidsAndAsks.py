import os

current_dir = os.path.dirname(os.path.abspath(__file__))
abi_path = os.path.join(current_dir, 'abis/uniswapV3.abi.json')

def split_bytes_string(bytes_string):
    # 将bytes string切割成每个bytes32
    bytes32_list = [bytes_string[i:i+64] for i in range(0, len(bytes_string), 64)]
    return bytes32_list

# 示例用法
bytes_string = "fffffffffffffffffffffffffffcc0f2fffffffffffff6611f6a51e0e7cb8645fffffffffffffffffffffffffffcc25000000000000050a42f26d524040a5e92fffffffffffffffffffffffffffcc2b4ffffffffffffaf5bd0d92adbfbf5a16efffffffffffffffffffffffffffcc2e6ffffffffffffc4c6513731e68458f82afffffffffffffffffffffffffffcc37c000000000006f4b79c8e4ff4512d035bfffffffffffffffffffffffffffcc476ffffffffffff993de468255358033e0cfffffffffffffffffffffffffffcc4a8fffffffffffec88ca71f2ad7e2b6b89dfffffffffffffffffffffffffffcc50cfffffffffffff1c6041d37544fc3c66bfffffffffffffffffffffffffffcc570ffffffffffff93cc86d2fd9535283b98fffffffffffffffffffffffffffcc606ffffffffffff19712c443baf36157237fffffffffffffffffffffffffffcc6ceffffffffffff295e8eac9e89b86a7818fffffffffffffffffffffffffffcc732ffffffffffffe9000520c195ccf63817fffffffffffffffffffffffffffcc7c8fffffffffffed71dd9464e22b7e66aa9fffffffffffffffffffffffffffcc7fafffffffffffaa22b9ac2986e10999031fffffffffffffffffffffffffffcc926fffffffffffe2497a6b622e7a4f65589fffffffffffffffffffffffffffccb7e0000000000091daf4349ab167bfb5f9ffffffffffffffffffffffffffffccc14ffffffffffffc0eca1bb13f5118c46f0fffffffffffffffffffffffffffcccaaffffffffffff9f18c51537604eceab28fffffffffffffffffffffffffffcced0fffffffffffff930842f0f8a4721a400fffffffffffffffffffffffffffcd0f6ffffffffffffa362f3fc22ab8bd4ab49fffffffffffffffffffffffffffcd128ffffffffffffd5d0d4175922a315270cfffffffffffffffffffffffffffcd3e4fffffffffffee779b5ec7d98a4184843fffffffffffffffffffffffffffcd4acfffffffffffff97cd9268dfa7baca23cfffffffffffffffffffffffffffcd5d8ffffffffffff7efa1bdf3293052740c5fffffffffffffffffffffffffffcd66effffffffffdb57aabf5166e54eaa2546fffffffffffffffffffffffffffcd9c0fffffffffffff0cb98009bf0bd922347fffffffffffffffffffffffffffcda24fffffffffff90b486371b00baed2fca5fffffffffffffffffffffffffffcdb1effffffffffffe728155a57e2913f4d3dfffffffffffffffffffffffffffcdb82fffffffffffd8c51514613c281b1f23cfffffffffffffffffffffffffffcdce0ffffffffffffc2fb1a7c15ec62abf707fffffffffffffffffffffffffffcdd12ffffffffffff7546f06fb2b2ec230360fffffffffffffffffffffffffffcdea2fffffffffff6e250bcb654e98404a061fffffffffffffffffffffffffffce3b6fffffffffffeefe4add36d7ef7110b6afffffffffffffffffffffffffffce79effffffffffffffef7dabb39edef694a1fffffffffffffffffffffffffffd1c8cfffffffffffffeebe4d8cb59cd79c6fb000000000000000000000000000d89d2ffffffffffbd7911c14c8bb9bfe1590afffffffffffffffffffffffffffcbfc6000000000000dd16b8090c3339a43fbdfffffffffffffffffffffffffffcbf620000000000044821e48ba3b95402bba6fffffffffffffffffffffffffffcbe04000000000001db685949dd185b09aa77fffffffffffffffffffffffffffcbda000000000000006cf7bd0f075b8de5c00fffffffffffffffffffffffffffcbd3c00000000000060a5aba9ac991d8e6c33fffffffffffffffffffffffffffcbcd80000000000000e39fbe2c8abb03c3995fffffffffffffffffffffffffffcbca600000000000128e226b9b1dd48199557fffffffffffffffffffffffffffcbc42000000000000cd11b791eaaf2d808257fffffffffffffffffffffffffffcbc10000000000000099ee095ae1f183479bbfffffffffffffffffffffffffffcbb7a0000000000003b39aec8ce197ba707d6fffffffffffffffffffffffffffcbb16000000000000389bc8a8b7a561bf746cfffffffffffffffffffffffffffcbae4000000000000d6a171536176479587e8fffffffffffffffffffffffffffcbab20000000000003f135e44ec0aee73b910fffffffffffffffffffffffffffcb9ea00000000000016fffadf3e6a3309c7e9fffffffffffffffffffffffffffcb88c0000000000002a2f2be8a6dd5cead8f4fffffffffffffffffffffffffffcb760000000000001101b522c928108eef496fffffffffffffffffffffffffffcb472ffffffffffceb881b7822510d72ef17dfffffffffffffffffffffffffffcb3aa000000000024a85540ae991ab155dabafffffffffffffffffffffffffffcb34600000000000273aeaeb9ec3d7e4e0dc4fffffffffffffffffffffffffffcb2e20000000000000f3467ff640f426ddcb9fffffffffffffffffffffffffffcb1b600000000000118864a1382675be7b7bdfffffffffffffffffffffffffffcaff40000000000003d04e583ea139d5408f9fffffffffffffffffffffffffffcae00000000000000068326d9720584535dc4fffffffffffffffffffffffffffcabda000000000000ecb4402fd2bfa2e17a73fffffffffffffffffffffffffffca824000000000000001082544c6121096b5ffffffffffffffffffffffffffffca7c000000000000018d7eaa5a81d6ec0b2c3fffffffffffffffffffffffffffca6c60000000000008ab90f904d4d13dcfca0fffffffffffffffffffffffffffca3d80000000000008105e420cd6cfad8bf3bfffffffffffffffffffffffffffc9f5afffffffffffffea12e9745ec387749a7fffffffffffffffffffffffffffc9d02000000000001377358e0d5281d494763fffffffffffffffffffffffffffc9aaa0000000000005c9d0c03dd54742b54b7fffffffffffffffffffffffffffc9a14ffffffffffc7855fa9091024694233a3fffffffffffffffffffffffffffc933e000000000000015ed168ba13c788b659fffffffffffffffffffffffffffc701600000000000001141b2734a632863905fffffffffffffffffffffffffffc6bca0000000000387aa056f6efdb96bdcc5dfffffffffffffffffffffffffff2762e000000000073ce6c87314f3568efb579"
result = split_bytes_string(bytes_string)

# 定义一个数组，记录从-887250 ～ 887250的一个DeltaL累加值
deltaL_accumulated = [0] * (887250 - (-887250) + 1)

currenctTick = -212780

liquidity = 148723491823002002625347566

tick_spacing = 50

# 将结果存储在一个列表中
deltaL_datas = []
for item in result:
    tick_number = int(item[:32], 16)
    deltaL = int(item[32:], 16)
    if tick_number >= 2**127:
        tick_number -= 2**128
    if deltaL >= 2**127:
        deltaL -= 2**128
    deltaL_datas.append((tick_number, deltaL, 0))

# 按照tick_number排序
deltaL_datas.sort(key=lambda x: x[0])

currentIndex = 0
for i, data in enumerate(deltaL_datas):
    tick_number, deltaL, _ = data
    if tick_number > currenctTick:
        currentIndex = i;
        break

lowerLiquidity = liquidity
for i in range(currentIndex - 1, -1, -1):
    tick_number, deltaL, _ = deltaL_datas[i]
    lowerLiquidity -= deltaL
    deltaL_datas[i] = (tick_number, deltaL, lowerLiquidity)

upperLiquidity = liquidity
for i in range(currentIndex, len(deltaL_datas)):
    tick_number, deltaL, _ = deltaL_datas[i]
    upperLiquidity += deltaL
    deltaL_datas[i] = (tick_number, deltaL, upperLiquidity)

# # 输出deltaL_datas
for data in deltaL_datas:
    print(f"tick_number: {data[0]}, deltaL: {data[1]}, value: {data[2]}")

print(f"currentTick : {currenctTick} , currentIndex: {currentIndex}")

from UniswapV3PoolUtil import UniswapV3PoolUtil

# 定义Bid和Ask的数组
bids = []
asks = []

# 初始化UniswapV3PoolUtil实例
pool_util = UniswapV3PoolUtil(tick_spacing)

# 遍历deltaL_datas，生成Bid和Ask
for i, data in enumerate(deltaL_datas):
    upperTick, deltaL, liquidity = data
    (lowerTick, _, _) = deltaL_datas[i-1]

    if liquidity == 0:
         continue;

    buy1_and_sell1 = pool_util.get_buy_and_sell_with_quantity_duringTicks(lowerTick, upperTick, liquidity)

    if i < currentIndex:
        # 生成Bid
        bids.append({'price': buy1_and_sell1['buy1']['lower_price'], 'quantity': buy1_and_sell1['buy1']['quantity']})
    elif i == currentIndex:
        buy2_and_sell2 = pool_util.get_buy_and_sell_with_quantity_duringTicks(lowerTick, currenctTick, liquidity)

        bidsTimes = int((currenctTick - lowerTick) / tick_spacing);
        for j in range(bidsTimes):
            bids.append({'price': pool_util.get_price_at_tick(lowerTick + j * tick_spacing), 'quantity': buy2_and_sell2['buy1']['quantity'] / tick_spacing})

        asksTimes = int((upperTick - currenctTick) / tick_spacing);
        buy3_and_sell3 = pool_util.get_buy_and_sell_with_quantity_duringTicks(currenctTick, upperTick, liquidity)

        for j in range(asksTimes):
            asks.append({'price': pool_util.get_price_at_tick(currenctTick + j * tick_spacing), 'quantity': buy3_and_sell3['sell1']['quantity'] / tick_spacing})
        
        print( "upperTick: ", upperTick, "currenctTick: ", currenctTick, ",bidsTimes: ", bidsTimes, ", asksTimes: ", asksTimes)
    else:
        # 生成Ask
        asks.append({'price': buy1_and_sell1['sell1']['upper_price'], 'quantity': buy1_and_sell1['sell1']['quantity']})

# 输出Bid和Ask数组
print("Bids:")
for bid in bids:
    print(f"Bid Price: {bid['price']}, Quantity: {bid['quantity']}")

print("Asks:")
for ask in asks:
    print(f"Ask Price: {ask['price']}, Quantity: {ask['quantity']}")



