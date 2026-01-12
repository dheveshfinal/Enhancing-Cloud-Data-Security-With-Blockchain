// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract AccessRequest {
    struct Request {
        uint256 id;
        string fileid;
        string useremail;
        string textcontent;
        string receiveremail;
        string filekey;
        string datetime;
        string status;
    }

    mapping(address => Request[]) public request;

    function addRequest(
        string memory __fileid,
        string memory __useremail,
        string memory __textcontent,
        string memory __receiveremail,
        string memory __filekey,
        string memory __datetime,
        string memory __status
    ) public {
        uint256 index = request[msg.sender].length + 1;
        request[msg.sender].push(
            Request(
                index,
                __fileid,
                __useremail,
                __textcontent,
                __receiveremail,
                __filekey,
                __datetime,
                __status
            )
        );
    }

    function getRequestsFromOther(
        string memory _email,
        string memory __status
    )
        public
        view
        returns (
            uint256[] memory,
            string[] memory,
            string[] memory,
            string[] memory,
            string[] memory,
            string[] memory,
            string[] memory,
            string[] memory
        )
    {
        uint256 count = request[msg.sender].length;

        uint256[] memory _id = new uint256[](count);
        string[] memory _fileid = new string[](count);
        string[] memory _useremail = new string[](count);
        string[] memory _textcontent = new string[](count);
        string[] memory _receiveremail = new string[](count);
        string[] memory _filekey = new string[](count);
        string[] memory _datetime = new string[](count);
        string[] memory _status = new string[](count);

        for (uint256 i = 0; i < request[msg.sender].length; i++) {
            Request storage requests3 = request[msg.sender][i];

            bool emailCheck = keccak256(abi.encode(_email)) ==
                keccak256(abi.encode(requests3.useremail));

            bool statusCheck = keccak256(abi.encode(__status)) ==
                keccak256(abi.encode(requests3.status));

            if (emailCheck && statusCheck) {
                _id[count] = requests3.id;
                _fileid[count] = requests3.fileid;
                _useremail[count] = requests3.useremail;
                _textcontent[count] = requests3.textcontent;
                _receiveremail[count] = requests3.receiveremail;
                _filekey[count] = requests3.filekey;
                _datetime[count] = requests3.datetime;
                _status[count] = requests3.status;
            }
        }

        return (
            _id,
            _fileid,
            _useremail,
            _textcontent,
            _receiveremail,
            _filekey,
            _datetime,
            _status
        );
    }
}
