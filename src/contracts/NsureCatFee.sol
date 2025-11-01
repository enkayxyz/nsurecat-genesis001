// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
}

contract NsureCatFee {
    address public treasury;
    address public usdcToken;
    uint256 public feeAmount = 10000;  // 0.01 USDC (assuming 6 decimals)

    constructor(address _treasury, address _usdcToken) {
        treasury = _treasury;
        usdcToken = _usdcToken;
    }

    function payFee() external {
        IERC20(usdcToken).transferFrom(msg.sender, treasury, feeAmount);
    }
}