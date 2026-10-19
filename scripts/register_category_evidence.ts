import { network } from "hardhat";

async function main() {
  const { ethers } = await network.connect();

  const contractAddress = process.env.TRUSTLOG_CONTRACT_ADDRESS;

  if (!contractAddress) {
    throw new Error("Please set TRUSTLOG_CONTRACT_ADDRESS first.");
  }

  const contract = await ethers.getContractAt(
    "TrustLogRegistry",
    contractAddress
  );

  const records = [
    {
      evidenceId: "TRUSTLOG-LOW-001",
      sha256Hash:
        "2b0589bf8934d931f5ef20a546989864fd6c83f935f038eed7addb01f50af04e",
      ipfsCid: "QmUEoe3QvhYP8q6LCoRFiCd5rZC32G4kY6vSUtUxPdrX4D",
      riskScore: 21,
    },
    {
      evidenceId: "TRUSTLOG-MEDIUM-001",
      sha256Hash:
        "b73f635494d320cae7a782f86a35d7f12c7388d757b3e022544ce4c306b1cd1f",
      ipfsCid: "QmVrj6YCjffg7txLSbmLn3m1CRdDZbMigBNBLiyo5T8ZeC",
      riskScore: 54,
    },
    {
      evidenceId: "TRUSTLOG-HIGH-001",
      sha256Hash:
        "e55fb81d02c404d1e4f0708953bf9c97e9b5ece8428cf9253f37a98be4e4dbe4",
      ipfsCid: "QmRCAYXviS5DcqQRPwcdB4EVp3jeUgpaLbgcCM542R7eAR",
      riskScore: 80,
    },
  ];

  for (const record of records) {
    console.log(`\nRegistering ${record.evidenceId}...`);

    const tx = await contract.registerEvidence(
      record.evidenceId,
      record.sha256Hash,
      record.ipfsCid,
      record.riskScore
    );

    console.log("Transaction submitted:", tx.hash);
    await tx.wait();

    console.log(`${record.evidenceId} registered successfully.`);
  }

  console.log("\nAll category evidence records registered.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
