import { network } from "hardhat";

async function main() {
  const { ethers } = await network.connect();

  const contractAddress = "0x6993D79625EC77BC3d81807d957A336D9B9f6eEC";

  const contract = await ethers.getContractAt(
    "TrustLogRegistry",
    contractAddress
  );

  const evidenceId = "TRUSTLOG-HIGH-RISK-001";

  const sha256Hash =
    "c98d94b7550413f592835ab2c376c1646a0b56b8360a7723ef3247e94c196b0e";

  const ipfsCid =
    "QmfFguXXn3sefUzkfJKcFBDEeLURo5NgbA2cjS3DpuzaVM";

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