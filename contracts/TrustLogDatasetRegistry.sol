 // SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TrustLogDatasetRegistry {
    struct Dataset {
        string datasetId;
        string sha256Hash;
        string ipfsCid;
        string version;
        uint256 rowCount;
        uint256 timestamp;
        address recorder;
    }

    mapping(string => Dataset) private datasets;

    event DatasetRegistered(
        string datasetId,
        string sha256Hash,
        string ipfsCid,
        string version,
        uint256 rowCount,
        uint256 timestamp,
        address recorder
    );

    function registerDataset(
        string memory datasetId,
        string memory sha256Hash,
        string memory ipfsCid,
        string memory version,
        uint256 rowCount
    ) public {
        require(bytes(datasetId).length > 0, "Dataset ID required");
        require(bytes(sha256Hash).length > 0, "Hash required");
        require(bytes(ipfsCid).length > 0, "IPFS CID required");
        require(bytes(version).length > 0, "Version required");
        require(rowCount > 0, "Row count must be positive");
        require(
            bytes(datasets[datasetId].datasetId).length == 0,
            "Dataset already exists"
        );

        datasets[datasetId] = Dataset(
            datasetId,
            sha256Hash,
            ipfsCid,
            version,
            rowCount,
            block.timestamp,
            msg.sender
        );

        emit DatasetRegistered(
            datasetId,
            sha256Hash,
            ipfsCid,
            version,
            rowCount,
            block.timestamp,
            msg.sender
        );
    }

    function getDataset(
        string memory datasetId
    ) public view returns (Dataset memory) {
        require(
            bytes(datasets[datasetId].datasetId).length > 0,
            "Dataset not found"
        );

        return datasets[datasetId];
    }
}
