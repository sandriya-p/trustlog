import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { network } from "hardhat";

async function main() {
  const contractAddress = process.env.TRUSTLOG_CONTRACT_ADDRESS;

  if (!contractAddress) {
    throw new Error("TRUSTLOG_CONTRACT_ADDRESS is not set.");
  }

  const evidenceId = process.env.TRUSTLOG_EVIDENCE_ID;
  const filePath = process.env.TRUSTLOG_EVIDENCE_FILE;

  if (!evidenceId || !filePath) {
    throw new Error(
      'Usage: npx hardhat run scripts/check_tampering.ts --network ganache -- "EVIDENCE-ID" "FILE-PATH"'
    );
  }

  const { ethers } = await network.connect();
  const contract = await ethers.getContractAt(
    "TrustLogRegistry",
    contractAddress
  );

  console.log("\nTrustLog Blockchain Tampering Check");
  console.log("Evidence ID:", evidenceId);
  console.log("File:", filePath);

  const evidence = await contract.getEvidence(evidenceId);
  const trustedHash = String(evidence[1]).toLowerCase();

  const fileBytes = readFileSync(filePath);
  const actualHash = createHash("sha256")
    .update(fileBytes)
    .digest("hex")
    .toLowerCase();

  console.log("\nBlockchain SHA-256:", trustedHash);
  console.log("File SHA-256:      ", actualHash);

  if (actualHash === trustedHash) {
    console.log("\nRESULT: NOT TAMPERED - Hashes match.");
  } else {
    console.log("\nRESULT: TAMPERED - Hash mismatch detected!");
    process.exitCode = 1;
  }
}

main().catch((error) => {
  console.error("\nERROR:", error.message ?? error);
  process.exitCode = 1;
});