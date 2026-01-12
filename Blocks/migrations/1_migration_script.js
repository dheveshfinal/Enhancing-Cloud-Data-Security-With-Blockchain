const UserData = artifacts.require("UserContract")

module.exports = function (deployer) {
    deployer.deploy(UserData)
}