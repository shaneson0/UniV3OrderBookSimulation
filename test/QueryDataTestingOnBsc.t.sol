// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;
pragma experimental ABIEncoderV2;

import {Test, console} from "forge-std/Test.sol";
import {TickMath} from "../src/libraries/TickMath.sol";

import {QueryActiveLiquidity} from "../src/QueryActiveLiquidity.sol";

import '../src/interfaces/IUniswapV3PoolState.sol';
import '../src/interfaces/IUniswapV3PoolImmutables.sol';


interface IQueryData {
    function queryUniv3TicksSuperCompact(address pool, uint256 len) external view returns (bytes memory);
}

interface IUniswapV3Pool is IUniswapV3PoolImmutables {
    function slot0()
        external
        view
        returns (
            uint160 sqrtPriceX96,
            int24 tick,
            uint16 observationIndex,
            uint16 observationCardinality,
            uint16 observationCardinalityNext,
            uint32 feeProtocol,
            bool unlocked
        );
    function liquidity() external view returns (uint128);
}

contract QueryDataTesting is Test {
    QueryActiveLiquidity public queryLiquidity;

    address public V3Pool = 0x38231d4ef9d33EBea944C75a21301ff6986499C3;
    address public V2Pool = 0xaf0Eb8F2f114917ef0026105c070Cf08423F488E;
    address public queryDataAddress = 0xD0B2a7c5f9321e038eEC9D9d9e0623923c1c02a7;
    
    function setUp() public {
        vm.createSelectFork("https://bsc.meowrpc.com");
        queryLiquidity = new QueryActiveLiquidity();
    }

    function test0() public {
        (
            uint160 currentPriceSqrtPriceX96,
            int24 tick,
            uint16 observationIndex,
            uint16 observationCardinality,
            uint16 observationCardinalityNext,
            uint32 feeProtocol,
            bool unlocked
        ) = IUniswapV3Pool(V3Pool).slot0();
        uint256 currentPrice = uint256(currentPriceSqrtPriceX96);

        // 计算对应的tick数
        int24 downTick = tick - 10;
        int24 upTick = tick + 10;

        console.log("downTick", downTick);
        console.log("tick: ", tick);
        console.log("upTick", upTick);

        // tick0 price:  2.4842149800124597e-10
        // tick1 price:  5.879746384524717e-10
        // tick2 price:  9.936227245421387e-10

        require( downTick < tick && tick < upTick, "check ticks" );

        bytes memory infos = queryLiquidity.queryUniv3TicksSuperCompact(V3Pool, 100);
        console.logBytes(infos);

        for (uint256 i = 0; i < infos.length; i += 32) {
            bytes32 tickInfo;
            assembly {
                tickInfo := mload(add(infos, add(32, i)))
            }
            int24 _tick = int24(int256(uint256(tickInfo) >> 128));
            int128 liquidityNet = int128(uint128(uint256(tickInfo)));

            console.log("liquidityNet: ", liquidityNet);
        }
        console.log(infos.length / 32);
        console.log("current tick", tick);

        console.log(IUniswapV3Pool(V3Pool).tickSpacing());

        uint128 liquidity = IUniswapV3Pool(V3Pool).liquidity();
        console.log("liquidity: ", liquidity);

    }


}