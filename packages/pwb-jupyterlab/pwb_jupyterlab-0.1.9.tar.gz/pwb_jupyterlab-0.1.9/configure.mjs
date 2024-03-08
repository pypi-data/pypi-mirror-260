import { promises as fsp } from 'fs';


const EXT_VERSION = process.env.EXT_VERSION || '0.99.99';

if (process.env.EXT_VERSION) {
  console.log(`using version "${EXT_VERSION}"`);
} else {
  console.log(`no version specified, resetting to default "${EXT_VERSION}"`);
}

async function updatePackageFile() {
  const packageFile = await fsp.readFile('./package.json');
  
  try {
    const packageJson = JSON.parse(packageFile);
    packageJson.version = EXT_VERSION;
  
    await fsp.writeFile('./package.json', JSON.stringify(packageJson, null, 2));
    console.log(`\x1B[;32mconfigured package file with version "${EXT_VERSION}"\x1B[;m`);
  } catch (err) {
    console.error(err);
  }
}

updatePackageFile();
