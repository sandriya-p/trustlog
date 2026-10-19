import { network } from "hardhat";

async function main() {
  const { ethers } = await network.connect();

  const contractAddress = process.env.TRUSTLOG_DATASET_CONTRACT_ADDRESS;

  if (!contractAddress) {
    throw new Error(
      "Please set TRUSTLOG_DATASET_CONTRACT_ADDRESS first."
    );
  }

  const contract = await ethers.getContractAt(
    "TrustLogDatasetRegistry",
    contractAddress
  );

  const datasetId = "TRUSTLOG-DATASET-V2-001";
  const sha256Hash =
    "10e57315ca3fd0d51784302c08dd6b0b6113e1d9d3649fa0401cd42e2335ecea";
  const ipfsCid =
    "QmVrLZtd9tf2aeRoJW8ySHnhwTDixBgotnmGsg7JqpEbmq";
  const version = "v2";
  const rowCount = 88865;

  console.log("Registering TrustLog dataset metadata...");
  console.log("Dataset ID:", datasetId);
  console.log("SHA-256:", sha256Hash);
  console.log("IPFS CID:", ipfsCid);
  console.log("Version:", version);
  console.log("Rows:", rowCount);

  const tx = await contract.registerDataset(
    datasetId,
    sha256Hash,
    ipfsCid,
    version,
    rowCount
  );

  console.log("Transaction submitted:", tx.hash);
  await tx.wait();

  console.log("Dataset metadata registered successfully.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
