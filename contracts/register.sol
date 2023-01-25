// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract register {

  address[] _usernames;
  string[] _emails;
  string[] _names;
  string[] _mobiles;
  string[] _depts;
  uint[] _roles;
  uint[] _passwords;

  mapping(address=>bool) users;

  function registeruser(address username,string memory email,string memory name,string memory mobile,string memory dept,uint role,uint password) public {
    
    require(!users[username]);

    users[username]=true;
    _usernames.push(username);
    _emails.push(email);
    _names.push(name);
    _mobiles.push(mobile);
    _depts.push(dept);
    _roles.push(role);
    _passwords.push(password);
    
  }

  function viewusers() public view returns(address[] memory,string[] memory,string[] memory,string[] memory,string[] memory,uint[] memory,uint[] memory){

    return(_usernames,_emails,_names,_mobiles,_depts,_roles,_passwords);
  }

  function loginuser(address username,uint password) public view returns(bool){

    uint i=0;
    require(users[username]);

    for(i=0;i<_usernames.length;i++){

      if(_usernames[i]==username && _passwords[i]==password){

        return true;
      }
    }
    return false;


  }
}
