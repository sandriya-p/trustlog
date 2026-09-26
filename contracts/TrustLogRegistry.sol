// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TrustLogRegistry {
    struct Evidence {
        string evidenceId;
        string sha256Hash;
        string ipfsCid;
        uint256 riskScore;
        uint256 timestamp;
        address recorder;
    }

    mapping(string => Evidence) private evidenceRecords;

    event EvidenceRegistered(
        string evidenceId,
        string sha256Hash,
        string ipfsCid,
        uint256 riskScore,
        uint256 timestamp,
        address recorder
    );

    function registerEvidence(
        string memory evidenceId,
        string memory sha256Hash,
        string memory ipfsCid,
        uint256 riskScore
    ) public {
        require(bytes(evidenceId).length > 0, "Evidence ID required");
        require(bytes(sha256Hash).length > 0, "Hash required");
        require(bytes(ipfsCid).length > 0, "IPFS CID required");
        require(riskScore <= 100, "Risk score must be 0-100");
        require(
            bytes(evidenceRecords[evidenceId].evidenceId).length == 0,
            "Evidence already exists"
        );

        evidenceRecords[evidenceId] = Evidence(
            evidenceId,
            sha256Hash,
            ipfsCid,
            riskScore,
            block.timestamp,
            msg.sender
        );

        emit EvidenceRegistered(
            evidenceId,
            sha256Hash,
            ipfsCid,
            riskScore,
            block.timestamp,
            msg.sender
        );
    }

    function getEvidence(
        string memory evidenceId
    ) public view returns (Evidence memory) {
        require(
            bytes(evidenceRecords[evidenceId].evidenceId).length > 0,
            "Evidence not found"
        );

        return evidenceRecords[evidenceId];
    }
}