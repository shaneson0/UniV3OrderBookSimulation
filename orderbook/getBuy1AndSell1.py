import json
from web3 import Web3
import os

# 连接到BSC节点
bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

# 检查连接是否成功
if not web3.is_connected():
    raise Exception("connect error")

# 合约地址和ABI
poolAddress = "0x38231d4ef9d33EBea944C75a21301ff6986499C3"

# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
abi_path = os.path.join(current_dir, 'abis/uniswapV3.abi.json')

with open(abi_path, 'r') as abi_file:
    abi = json.load(abi_file)

# 创建合约实例
v3Pool = web3.eth.contract(address=poolAddress, abi=abi)


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
print("Tick Spacing: ", tick_spacing)


from UniswapV3PoolUtil import UniswapV3PoolUtil

# 初始化UniswapV3PoolUtil实例
pool_util = UniswapV3PoolUtil(tick_spacing)

# 获取买一和卖一价格及数量
buy1_and_sell1 = pool_util.get_buy1_and_sell1_without_quantity(currentTick)

print("Buy1 - Price: {}".format(buy1_and_sell1['buy1']['price']))
print("Sell1 - Price: {}".format(buy1_and_sell1['sell1']['price']))



