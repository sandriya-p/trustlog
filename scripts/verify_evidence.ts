import { network } from "hardhat";

async function main() {
  const { ethers } = await network.connect();

  const contractAddress = "0x6993D79625EC77BC3d81807d957A336D9B9f6eEC";

  const contract = await ethers.getContractAt(
    "TrustLogRegistry",
    contractAddress
  );

  const evidenceId = "TRUSTLOG-HIGH-RISK-001";

  console.log("Reading evidence from blockchain...\n");

  const evidence = await contract.getEvidence(evidenceId);

  console.log("Evidence ID:", evidence[0]);
  console.log("SHA-256 Hash:", evidence[1]);
  console.log("IPFS CID:", evidence[2]);
  console.log("Risk Score:", evidence[3].toString());
  console.log(
    "Blockchain Timestamp:",
    new Date(Number(evidence[4]) * 1000).toISOString()
  );
  console.log("Recorder Address:", evidence[5]);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});