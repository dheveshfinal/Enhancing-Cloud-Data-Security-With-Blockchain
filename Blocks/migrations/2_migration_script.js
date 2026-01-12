const FileData=artifacts.require("FileRequest")

module.exports = function(deployer){
    deployer.deploy(FileData)   
}