import { mkdir, copyFile } from 'fs/promises';
import { join } from 'path';

const moveFile = async (sourcePath, destPath) => {
  try {
    await mkdir(join(destPath, '..'), { recursive: true });
    await copyFile(sourcePath, destPath);
    console.log(`Moved: ${sourcePath} to ${destPath}`);
  } catch (err) {
    console.error(`Error moving file: ${err}`);
  }
};

// Define your file paths
const source = './public/index.html';
const destination = './build/index.html';

// Execute the move
await moveFile(source, destination);