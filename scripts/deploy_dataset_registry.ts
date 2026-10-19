import { network } from "hardhat";

async function main() {
  const { ethers } = await network.connect();

  console.log("Deploying TrustLogDatasetRegistry...");

  const DatasetRegistry = await ethers.getContractFactory(
    "TrustLogDatasetRegistry"
  );

  const contract = await DatasetRegistry.deploy();

  await contract.waitForDeployment();

  const address = await contract.getAddress();

  console.log("TrustLogDatasetRegistry deployed to:", address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
