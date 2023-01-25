const register=artifacts.require("register");

module.exports=function(deployer){
    deployer.deploy(register);
    
}