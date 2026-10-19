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

  const expectedRecords = [
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

  let allPassed = true;

  for (const expected of expectedRecords) {
    console.log(`\nChecking ${expected.id}...`);

    const actual = await contract.getEvidence(expected.id);

    const checks = [
      ["Evidence ID", String(actual[0]), expected.id],
      ["SHA-256", String(actual[1]), expected.hash],
      ["IPFS CID", String(actual[2]), expected.cid],
      ["Risk score", actual[3].toString(), String(expected.score)],
    ] as const;

    for (const [label, actualValue, expectedValue] of checks) {
      const passed = actualValue === expectedValue;
      console.log(
        `${passed ? "PASS" : "FAIL"} - ${label}: ${actualValue}`
      );

      if (!passed) {
        console.log(`  Expected: ${expectedValue}`);
        allPassed = false;
      }
    }

    console.log(
      "Blockchain timestamp:",
      new Date(Number(actual[4]) * 1000).toISOString()
    );
    console.log("Recorder address:", actual[5]);
  }

  if (!allPassed) {
    throw new Error("One or more evidence verification checks failed.");
  }

  console.log("\nSUCCESS: All four blockchain records match expected values.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});