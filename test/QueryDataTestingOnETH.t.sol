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
}

contract QueryDataTestingOnETH is Test {
    QueryActiveLiquidity public queryLiquidity;

    address public V3Pool = 0xCBCdF9626bC03E24f779434178A73a0B4bad62eD;
    
    function setUp() public {
        vm.createSelectFork("https://eth.meowrpc.com");
        queryLiquidity = new QueryActiveLiquidity();
    }

    function test0OnETH() public {
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

        bytes memory infos = queryLiquidity.queryUniv3TicksSuperCompact(V3Pool, 50);
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
        console.log("current tick:", tick);

    }


}