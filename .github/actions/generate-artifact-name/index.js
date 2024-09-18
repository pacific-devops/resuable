const core = require('@actions/core');
const github = require('@actions/github');

try {
  // Input: prefix for artifact name
  const prefix = core.getInput('prefix');
  
  // Generate short SHA (first 7 characters)
  const shortSha = github.context.sha.substring(0, 7);
  
  // Get the GitHub run number
  const runNumber = github.context.runNumber;
  
  // Generate artifact name
  const artifactName = `${prefix}-${shortSha}-${runNumber}`;
  
  // Set the artifact name as an output
  core.setOutput('artifact_name', artifactName);
  
  console.log(`Generated artifact name: ${artifactName}`);
} catch (error) {
  core.setFailed(`Action failed with error: ${error.message}`);
}
