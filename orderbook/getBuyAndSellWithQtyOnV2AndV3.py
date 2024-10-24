import json
from web3 import Web3
import os
import math

def get_bids_and_asks(rpc_url, v2_pool_address, v3_pool_address, query_data_address, v2_abi_path, v3_abi_path, query_data_abi_path):
    # 连接到BSC节点
    web3 = Web3(Web3.HTTPProvider(rpc_url))

    # 检查连接是否成功
    if not web3.is_connected():
        raise Exception("connect error")
    current_dir = os.path.dirname(os.path.abspath(__file__))

    with open(v3_abi_path, 'r') as abi_file:
        abi = json.load(abi_file)

    with open(query_data_abi_path, 'r') as queryData_abi_file:
        queryData_abi = json.load(queryData_abi_file)

    with open(v2_abi_path, 'r') as uniswapv2_abi_file:
        uniswapV2_abi = json.load(uniswapv2_abi_file)

    # 创建合约实例
    v2Pool = web3.eth.contract(address=v2_pool_address, abi=uniswapV2_abi)
    v3Pool = web3.eth.contract(address=v3_pool_address, abi=abi)
    queryDataContract = web3.eth.contract(address=query_data_address, abi=queryData_abi)

    # 调用合约的slot0函数获取当前价格和tick等信息
    slot0 = v3Pool.functions.slot0().call()

    currentPriceSqrtPriceX96 = slot0[0]
    currentTick = slot0[1]
    observationIndex = slot0[2]
    observationCardinality = slot0[3]
    observationCardinalityNext = slot0[4]
    feeProtocol = slot0[5]
    unlocked = slot0[6]

    # 调用合约的tickSpacing函数获取tick间距
    tick_spacing = v3Pool.functions.tickSpacing().call()
    # print("Tick Spacing: ", tick_spacing)

    activeTicksInOneLength = queryDataContract.functions.queryUniv3TicksSuperCompact(v3_pool_address, 2).call()

    # 将bytes数组转码并切割
    tick_liquidity_list = []
    for i in range(0, len(activeTicksInOneLength), 32):
        tickInfo = activeTicksInOneLength[i:i+32]
        tick = int.from_bytes(tickInfo[:16], byteorder='big', signed=True)
        liquidityNet = int.from_bytes(tickInfo[16:], byteorder='big', signed=True)
        tick_liquidity_list.append({'tick': tick, 'liquidityNet': liquidityNet})

    # for item in tick_liquidity_list:
    #     print(f"Tick: {item['tick']}, LiquidityNet: {item['liquidityNet']}")

    # BandWidth = tick_liquidity_list[0]['tick'] - tick_liquidity_list[1]['tick']
    # print("Current Tick: ", currentTick)
    # print("BandWidth: ", BandWidth)

    liquidity = v3Pool.functions.liquidity().call()
    # print("liquidity: ", liquidity)

    reserves = v2Pool.functions.getReserves().call()
    UniswapV2K = reserves[0] * reserves[1]

    sqrt_price = math.sqrt(1.0001 ** currentTick)
    token0 = liquidity / sqrt_price
    token1 = liquidity * sqrt_price

    # WBNB(v2_token1)/Cheems(v2_token0) => price
    # v2_token1 * v2_token0 = k
    # v2_token1^2 = price * k
    # v2_token1 = sqrt(price * k)
    # v2_token0 = K / v2_token1

    v2_token1 = math.sqrt(UniswapV2K * (1.0001 ** currentTick))
    v2_token0 = UniswapV2K / v2_token1

    upper_bound = (currentTick + 5) if (currentTick + 5 < tick_liquidity_list[0]['tick'] - 1) else (tick_liquidity_list[0]['tick'] - 1)
    lower_bound = (currentTick - 5) if (currentTick - 5 > tick_liquidity_list[1]['tick'] + 1) else (tick_liquidity_list[1]['tick'] + 1)

    bids = []
    asks = []

    prev_tick_token1 = token1
    v2_prev_tick_token1 = v2_token1
    for tick in range(currentTick - 1, lower_bound -1, -1):
        price = 1.0001 ** tick

        token11 = liquidity * math.sqrt(price)
        v2_token11 = math.sqrt(UniswapV2K * price)

        # print("v3: ", (prev_tick_token1 - token11))
        # print("v2: ", (v2_prev_tick_token1 - v2_token11))

        bids.append((price, (prev_tick_token1 - token11) + (v2_prev_tick_token1 - v2_token11)))
        prev_tick_token1 = token11
        v2_prev_tick_token1 = v2_token11

    bids.sort(key=lambda x: x[0])

    prev_tick_token0 = token0
    v2_prev_tick_token0 = v2_token0
    for tick in range(currentTick + 1, upper_bound):
        price = 1.0001 ** tick

        token00 = liquidity / math.sqrt(price)
        v2_token11 = math.sqrt(UniswapV2K * price)
        v2_token00 = UniswapV2K / v2_token11

        # print("v3: ", (prev_tick_token0 - token00))
        # print("v2: ", (v2_prev_tick_token0 - v2_token00))

        asks.append((price, (prev_tick_token0 - token00) + (v2_prev_tick_token0 - v2_token00)))
        prev_tick_token0 = token00
        v2_prev_tick_token0 = v2_token00

    bids_and_asks = (tuple(bids), tuple(asks))
    return bids_and_asks

def get_ToB_price(rpc_url,v3_pool_address, v3_abi_path):
    # 连接到BSC节点
    web3 = Web3(Web3.HTTPProvider(rpc_url))

    # 检查连接是否成功
    if not web3.is_connected():
        raise Exception("connect error")
    current_dir = os.path.dirname(os.path.abspath(__file__))

    with open(v3_abi_path, 'r') as abi_file:
        abi = json.load(abi_file)

    v3Pool = web3.eth.contract(address=v3_pool_address, abi=abi)
    # 调用合约的slot0函数获取当前价格和tick等信息
    slot0 = v3Pool.functions.slot0().call()
    currentTick = slot0[1]  

    return (1.0001 ** (currentTick-1), 1.0001 ** (currentTick+1))


if __name__ == "__main__":
    rpc_url = "https://bsc-dataseed.binance.org/"
    v2_pool_address = "0xaf0Eb8F2f114917ef0026105c070Cf08423F488E"
    v3_pool_address = "0x38231d4ef9d33EBea944C75a21301ff6986499C3"
    query_data_address = "0xD0B2a7c5f9321e038eEC9D9d9e0623923c1c02a7"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    v2_abi_path = os.path.join(current_dir, 'abis/uniswapV2.abi.json')
    v3_abi_path = os.path.join(current_dir, 'abis/uniswapV3.abi.json')
    query_data_abi_path = os.path.join(current_dir, 'abis/querydata.abi.json')

    # bids_and_asks = get_bids_and_asks(rpc_url, v2_pool_address, v3_pool_address, query_data_address, v2_abi_path, v3_abi_path, query_data_abi_path)
    # print("Generated Bids and Asks:", bids_and_asks)


    (bid1_price, ask1_price) = get_ToB_price(rpc_url, v3_pool_address, v3_abi_path)
    print("bid1_price: ", bid1_price, ", ask1_price: ", ask1_price)

