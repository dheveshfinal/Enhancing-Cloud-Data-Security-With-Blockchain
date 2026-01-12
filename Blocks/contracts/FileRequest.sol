// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract FileRequest {
    struct FileUpload {
        uint256 id;
        string useremail;
        string textcontent;
        string filekey;
        string datetime;
        string encfilepath;
        string decfilepath;
    }
    mapping(address => FileUpload[]) public fileStore;

    function addFiles(
        string memory _useremail,
        string memory _textcontent,
        string memory _filekey,
        string memory _datetime,
        string memory _encfilepath,
        string memory _decfilepath
    ) public {
        uint256 index = fileStore[msg.sender].length + 1;
        FileUpload memory _newFile = FileUpload(
            index,
            _useremail,
            _textcontent,
            _filekey,
            _datetime,
            _encfilepath,
            _decfilepath
        );
        fileStore[msg.sender].push(_newFile);
    }

    function viewFiles(string memory _email)
        public
        view
        returns (
            uint256[] memory,
            string[] memory,
            string[] memory,
            string[] memory,
            string[] memory,
            string[] memory,
            string[] memory
        )
    {
        uint256 count = 0;
        for (uint256 i = 0; i < fileStore[msg.sender].length; i++) {
            FileUpload storage file = fileStore[msg.sender][i];
            if (
                keccak256(abi.encode(_email)) !=
                keccak256(abi.encode(file.useremail))
            ) {
                count++;
            }
        }

        uint256[] memory __id = new uint256[](count);
        string[] memory _useremail = new string[](count);
        string[] memory _textcontent = new string[](count);
        string[] memory _filekey = new string[](count);
        string[] memory _datetime = new string[](count);
        string[] memory _encfilepath = new string[](count);
        string[] memory _decfilepath = new string[](count);


        for (uint256 i = 0; i < fileStore[msg.sender].length; i++) {
            FileUpload storage file = fileStore[msg.sender][i];
            if (
                keccak256(abi.encode(_email)) !=
                keccak256(abi.encode(file.useremail))
            ) {
                __id[i] = file.id;
                _useremail[i] = file.useremail;
                _textcontent[i] = file.textcontent;
                _filekey[i] = file.filekey;
                _datetime[i] = file.datetime;
                _encfilepath[i] = file.encfilepath;
                _decfilepath[i] = file.decfilepath;
            }
        }
        return (
            __id,
            _useremail,
            _textcontent,
            _filekey,
            _datetime,
            _encfilepath,
            _decfilepath
        );
    }

    
}
