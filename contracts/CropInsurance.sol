// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CropInsurance {

    struct InsuranceDetails {
        uint256 areaOfLand;
        uint256 sumInsuredPerAcre;
        uint256 premiumAmount;
        uint256 dispersalAmount;
        uint256 premiumRate;
        address farmer;
    }

    mapping(uint256 => InsuranceDetails) public insuranceData;

    // Function to add insurance details
    function addInsurance(
        uint256 fips,
        uint256 areaOfLand,
        uint256 sumInsuredPerAcre,
        uint256 premiumRate,
        address farmer
    ) public {
        require(farmer != address(0), "Farmer address cannot be zero");
        
        // Calculate premium amount
        uint256 premiumAmount = (areaOfLand * sumInsuredPerAcre * premiumRate) / 100;

        // Calculate dispersal amount (same base formula + 10% buffer if needed)
        uint256 dispersalAmount = (areaOfLand * sumInsuredPerAcre * premiumRate) / 100;

        // Ensure dispersal amount is greater than premium amount (add 10% buffer)
        if (dispersalAmount <= premiumAmount) {
            dispersalAmount = premiumAmount * 110 / 100;
        }

        // Store insurance details
        insuranceData[fips] = InsuranceDetails(
            areaOfLand,
            sumInsuredPerAcre,
            premiumAmount,
            dispersalAmount,
            premiumRate,
            farmer
        );
    }

    // Function to disperse insurance amount
    function disperseInsurance(uint256 fips) public {
        InsuranceDetails storage insurance = insuranceData[fips];
        
        // Ensure contract has enough balance
        require(address(this).balance >= insurance.dispersalAmount, "Insufficient balance in contract");
        
        // Transfer dispersal amount to farmer's address (using payable)
        payable(insurance.farmer).transfer(insurance.dispersalAmount);
    }

    // Function to receive payments to the contract (if needed)
    receive() external payable {}
}
