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

  const evidenceId = "TRUSTLOG-HIGH-RISK-001";

  const sha256Hash =
  "1882fae6c2ba99ec459c7d0ae613b986c641c8f2b4fb9ad1c8a49be0b7f16fc1";

  const ipfsCid =
    "QmfJXJyPpK1AGiMy2jwvdt3dsomtpxSw79SUtizfzYYR46";

  const riskScore = 100;

  console.log("Registering TrustLog evidence...");

  const tx = await contract.registerEvidence(
    evidenceId,
    sha256Hash,
    ipfsCid,
    riskScore
  );

  console.log("Transaction submitted:", tx.hash);

  await tx.wait();

  console.log("Evidence registered successfully.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});