import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { network } from "hardhat";

const IPFS_EXE =
  "D:\\Downloads\\kubo_v0.43.1_windows-amd64\\kubo\\ipfs.exe";

const EXPECTED = [
  {
    id: "TRUSTLOG-HIGH-RISK-001",
    hash: "1882fae6c2ba99ec459c7d0ae613b986c641c8f2b4fb9ad1c8a49be0b7f16fc1",
    cid: "QmfJXJyPpK1AGiMy2jwvdt3dsomtpxSw79SUtizfzYYR46",
    score: 100,
  },
  {
    id: "TRUSTLOG-LOW-001",
    hash: "2b0589bf8934d931f5ef20a546989864fd6c83f935f038eed7addb01f50af04e",
    cid: "QmUEoe3QvhYP8q6LCoRFiCd5rZC32G4kY6vSUtUxPdrX4D",
    score: 21,
  },
  {
    id: "TRUSTLOG-MEDIUM-001",
    hash: "b73f635494d320cae7a782f86a35d7f12c7388d757b3e022544ce4c306b1cd1f",
    cid: "QmVrj6YCjffg7txLSbmLn3m1CRdDZbMigBNBLiyo5T8ZeC",
    score: 54,
  },
  {
    id: "TRUSTLOG-HIGH-001",
    hash: "e55fb81d02c404d1e4f0708953bf9c97e9b5ece8428cf9253f37a98be4e4dbe4",
    cid: "QmRCAYXviS5DcqQRPwcdB4EVp3jeUgpaLbgcCM542R7eAR",
    score: 80,
  },
];

function check(label: string, passed: boolean): boolean {
  console.log(`${passed ? "PASS" : "FAIL"} - ${label}`);
  return passed;
}

async function main() {
  const contractAddress = process.env.TRUSTLOG_CONTRACT_ADDRESS;

  if (!contractAddress) {
    throw new Error("TRUSTLOG_CONTRACT_ADDRESS is not set.");
  }

  const { ethers } = await network.connect();
  const contract = await ethers.getContractAt(
    "TrustLogRegistry",
    contractAddress
  );

  let totalPassed = 0;
  let totalFailed = 0;

  for (const expected of EXPECTED) {
    console.log(`\n===== ${expected.id} =====`);

    let recordPassed = true;

    try {
      const actual = await contract.getEvidence(expected.id);

      const metadataChecks = [
        check("Evidence ID", String(actual[0]) === expected.id),
        check("Blockchain SHA-256", String(actual[1]) === expected.hash),
        check("Blockchain IPFS CID", String(actual[2]) === expected.cid),
        check(
          "Blockchain risk score",
          actual[3].toString() === String(expected.score)
        ),
      ];

      const content = execFileSync(
        IPFS_EXE,
        ["cat", String(actual[2])],
        { maxBuffer: 10 * 1024 * 1024 }
      );

      const actualHash = createHash("sha256")
        .update(content)
        .digest("hex");

      console.log("Retrieved content SHA-256:", actualHash);

      const contentPassed = check(
        "IPFS content hash matches blockchain hash",
        actualHash === String(actual[1])
      );

      recordPassed =
        metadataChecks.every(Boolean) && contentPassed;
    } catch (error) {
      console.log("FAIL - Could not complete verification:", error);
      recordPassed = false;
    }

    if (recordPassed) {
      totalPassed++;
      console.log(`RESULT: PASS - ${expected.id}`);
    } else {
      totalFailed++;
      console.log(`RESULT: FAIL - ${expected.id}`);
    }
  }

  console.log("\n========== FINAL SUMMARY ==========");
  console.log("Records passed:", totalPassed);
  console.log("Records failed:", totalFailed);

  if (totalFailed > 0) {
    throw new Error("End-to-end evidence verification failed.");
  }

  console.log("SUCCESS: All four records passed end-to-end verification.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
