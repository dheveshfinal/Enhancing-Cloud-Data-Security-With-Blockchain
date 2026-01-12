// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract UserContract {
    struct Users {
        uint256 id;
        string name;
        string email;
        string password;
        string contact;
        string addresses;
        string status;
    }
    mapping(address => Users[]) public usersStore;
4
    function AddUsers(
        string memory _name,
        string memory _email,
        string memory _password,
        string memory _contact,
        string memory _addresses,
        string memory _status
    ) public returns (bool) {
        uint256 index = usersStore[msg.sender].length + 1;

        usersStore[msg.sender].push(
            Users(
                index,
                _name,
                _email,
                _password,
                _contact,
                _addresses,
                _status
            )
        );
        return (true);
    }

    function checkEmail(string memory _email)
        public
        view
        returns (string memory)
    {
        for (uint256 i = 0; i < usersStore[msg.sender].length; i++) {
            Users memory usersPoint = usersStore[msg.sender][i];
            if (
                keccak256(abi.encode(usersPoint.email)) ==
                keccak256(abi.encode(_email))
            ) {
                return ("email already exists");
            }
        }
        return ("Success");
    }

    function loginFunction(string memory _email, string memory _password)
        public
        view
        returns (
            uint256,
            string memory,
            string memory,
            string memory,
            string memory,
            string memory
        )
    {
        for (uint256 i = 0; i < usersStore[msg.sender].length; i++) {
            Users memory userPoint = usersStore[msg.sender][i];
            bool email = keccak256(abi.encode(userPoint.email)) ==
                keccak256(abi.encode(_email));
            bool password = keccak256(abi.encode(userPoint.password)) ==
                keccak256(abi.encode(_password));

            if (email && password) {
                return (
                    usersStore[msg.sender][i].id,
                    userPoint.name,
                    userPoint.email,
                    userPoint.contact,
                    userPoint.addresses,
                    userPoint.status
                );
            }
        }
        return (
            0,
            "Invalid Users",
            "Invalid Users",
            "Invalid Users",
            "Invalid Users",
            "Invalid Users"
        );
    }

    function getUsersActivated(string memory __status)
        public
        view
        returns (
            uint256[] memory,
            string[] memory,
            string[] memory,
            string[] memory,
            string[] memory,
            string[] memory
        )
    {
        uint256 index = usersStore[msg.sender].length;
        uint256[] memory id = new uint256[](index);
        string[] memory _name = new string[](index);
        string[] memory _email = new string[](index);
        string[] memory _contact = new string[](index);
        string[] memory _addresses = new string[](index);
        string[] memory _status = new string[](index);

        for (uint256 i = 0; i < usersStore[msg.sender].length; i++) {
            Users storage user = usersStore[msg.sender][i];
            if (
                keccak256(abi.encode(__status)) ==
                keccak256(abi.encode(user.status))
            ) {
                id[i] = user.id;
                _name[i] = user.name;
                _email[i] = user.email;
                _contact[i] = user.contact;
                _addresses[i] = user.addresses;
                _status[i] = user.status;
            }
        }
        return (id, _name, _email, _contact, _addresses, _status);
    }
    

    function upldateState(uint256 _id, string memory _status)
        public
    {
        for (uint256 i = 0; i < usersStore[msg.sender].length; i++) {
            Users storage user = usersStore[msg.sender][i];
            if (user.id == _id) {
                user.status = _status;
            }
        }
    }
}
