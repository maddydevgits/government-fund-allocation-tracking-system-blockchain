// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract funds {

  address[] _senders;
  address[] _receivers;
  uint[] _amounts;

  function createfund(address sender,address receiver,uint amount) public{

    _senders.push(sender);
    _receivers.push(receiver);
    _amounts.push(amount);

  }

  function viewfunds() public view returns(address[] memory,address[] memory,uint[] memory){

    return(_senders,_receivers,_amounts);

  }
}
