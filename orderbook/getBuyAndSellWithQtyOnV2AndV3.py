import json
from web3 import Web3
import os
import math

def get_bids_and_asks():
    # 连接到BSC节点
    bsc = "https://bsc-dataseed.binance.org/"
    web3 = Web3(Web3.HTTPProvider(bsc))

    # 检查连接是否成功
    if not web3.is_connected():
        raise Exception("connect error")
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 先处理V2的结果
    V2PoolAddress = "0xaf0Eb8F2f114917ef0026105c070Cf08423F488E"
    uniswapv2_abi_path = os.path.join(current_dir, 'abis/uniswapV2.abi.json')

    # 合约地址和ABI
    # BSC
    poolAddress = "0x38231d4ef9d33EBea944C75a21301ff6986499C3"
    queryDataAddress = "0xD0B2a7c5f9321e038eEC9D9d9e0623923c1c02a7"

    # 获取当前脚本的目录
    abi_path = os.path.join(current_dir, 'abis/uniswapV3.abi.json')
    queryData_abi_path = os.path.join(current_dir, 'abis/querydata.abi.json')

    with open(abi_path, 'r') as abi_file:
        abi = json.load(abi_file)

    with open(queryData_abi_path, 'r') as queryData_abi_file:
        queryData_abi = json.load(queryData_abi_file)

    with open(uniswapv2_abi_path, 'r') as uniswapv2_abi_file:
        uniswapV2_abi = json.load(uniswapv2_abi_file)

    # 创建合约实例
    v2Pool = web3.eth.contract(address=V2PoolAddress, abi=uniswapV2_abi)
    v3Pool = web3.eth.contract(address=poolAddress, abi=abi)
    queryDataContract = web3.eth.contract(address=queryDataAddress, abi=queryData_abi)

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

    activeTicksInOneLength = queryDataContract.functions.queryUniv3TicksSuperCompact(poolAddress, 2).call()

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

    v2_token1 = math.sqrt(UniswapV2K * 1.0001 ** currentTick)
    v2_token0 = math.sqrt(UniswapV2K / (1.0001 ** currentTick))

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

        bids.append((price, (prev_tick_token1 - token11) + (v2_prev_tick_token1 - v2_token11)))
        prev_tick_token1 = token11
        v2_prev_tick_token1 = v2_token11

    bids.sort(key=lambda x: x[0])

    prev_tick_token0 = token0
    v2_prev_tick_token0 = v2_token0
    for tick in range(currentTick + 1, upper_bound):
        price = 1.0001 ** tick

        token00 = liquidity / math.sqrt(price)
        v2_token00 = math.sqrt(UniswapV2K / price)

        asks.append((price, (prev_tick_token0 - token00) + (v2_prev_tick_token0 - v2_token00)))
        prev_tick_token0 = token00
        v2_prev_tick_token0 = v2_token00

    bids_and_asks = (tuple(bids), tuple(asks))
    return bids_and_asks


if __name__ == "__main__":
    bids_and_asks = get_bids_and_asks()
    print("Generated Bids and Asks:", bids_and_asks)
