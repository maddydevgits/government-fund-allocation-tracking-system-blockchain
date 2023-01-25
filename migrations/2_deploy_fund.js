const funds=artifacts.require("funds");

module.exports=function(deployer){
    deployer.deploy(funds);
    
}