pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
// contracts/src/v0.8/interfaces/AggregatorV3Interface.sol
contract FundMe{
    mapping (address => uint) public addressToAmountFunded;
    
    address private owner;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public{
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }
    function fund() public payable{
        uint minimumValue = 50 * 10 ** 18;
        require((getConversionRate(msg.value)) >= minimumValue);
        
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns(uint){
        
        return priceFeed.version();
    }

    function getLatestPrice() public view returns(uint){
        
        (, int answer, , , ) = priceFeed.latestRoundData();
        return uint(answer * 10000000000);
    }

    function getConversionRate(uint ethAmount) public view returns(uint){
        uint ethPrice = getLatestPrice();
        uint ethPriceInUSD = ethPrice * ethAmount / 1000000000000000000;
        return ethPriceInUSD;
    }

    modifier onlyOwner() {
       require(msg.sender == owner, "You are not the owner!");
        _;
    }

    function withdraw() public onlyOwner{
       address to = msg.sender;
       payable(to).transfer(address(this).balance);

       for(uint index; index<funders.length; index++){
           address funder = funders[index];
           addressToAmountFunded[funder] = 0;

       }
       funders = new address[](0);
    }


    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getLatestPrice();
        uint256 precision = 1 * 10**18;
        // return (minimumUSD * precision) / price;
        // We fixed a rounding error found in the video by adding one!
        return ((minimumUSD * precision) / price) + 1;
    }
}