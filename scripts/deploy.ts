import { network } from "hardhat";

async function main() {
  const { ethers } = await network.connect();

  console.log("Deploying TrustLogRegistry...");

  const TrustLogRegistry =
    await ethers.getContractFactory("TrustLogRegistry");

  const contract = await TrustLogRegistry.deploy();

  await contract.waitForDeployment();

  console.log(
    "TrustLogRegistry deployed to:",
    await contract.getAddress()
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});