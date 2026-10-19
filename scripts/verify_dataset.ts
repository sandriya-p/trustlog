
import { network } from "hardhat";

async function main() {
  const { ethers } = await network.connect();

  const contractAddress =
    process.env.TRUSTLOG_DATASET_CONTRACT_ADDRESS;

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
  const expectedHash =
    "10e57315ca3fd0d51784302c08dd6b0b6113e1d9d3649fa0401cd42e2335ecea";
  const expectedCid =
    "QmVrLZtd9tf2aeRoJW8ySHnhwTDixBgotnmGsg7JqpEbmq";

  const dataset = await contract.getDataset(datasetId);

  console.log("\nTrustLog Dataset Verification");
  console.log("Dataset ID:", dataset.datasetId);
  console.log("SHA-256:", dataset.sha256Hash);
  console.log("IPFS CID:", dataset.ipfsCid);
  console.log("Version:", dataset.version);
  console.log("Row count:", dataset.rowCount.toString());
  console.log(
    "Blockchain timestamp:",
    new Date(Number(dataset.timestamp) * 1000).toISOString()
  );
  console.log("Recorder:", dataset.recorder);

  const hashPass = dataset.sha256Hash === expectedHash;
  const cidPass = dataset.ipfsCid === expectedCid;
  const versionPass = dataset.version === "v2";
  const rowsPass = dataset.rowCount === 88865n;

  console.log("\nHash check:", hashPass ? "PASS" : "FAIL");
  console.log("CID check:", cidPass ? "PASS" : "FAIL");
  console.log("Version check:", versionPass ? "PASS" : "FAIL");
  console.log("Row count check:", rowsPass ? "PASS" : "FAIL");

  if (hashPass && cidPass && versionPass && rowsPass) {
    console.log("\nSUCCESS: Dataset metadata verified on blockchain.");
  } else {
    console.error("\nFAILURE: Dataset metadata mismatch detected.");
    process.exitCode = 1;
  }
}

main().catch((error) => {
  console.error("\nERROR:", error.message ?? error);
  process.exitCode = 1;
});
