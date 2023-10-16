import { mkdir, copyFile } from 'fs/promises';
import { join } from 'path';

const moveFile = async (sourcePath, destPath) => {
  try {
    await mkdir(join(destPath, '..'), { recursive: true });
    await copyFile(sourcePath, destPath);
    console.log(`Copied: ${sourcePath} to ${destPath}`);
  } catch (err) {
    console.error(`Error copying file: ${err}`);
  }
};

const assets = [
  ['./public/index.html', "./build/index.html"],
  ['./public/error_pages/400.html', "./build/400.html"],
  ['./public/error_pages/404.html', "./build/404.html"],
  ['./public/error_pages/500.html', "./build/500.html"],
];


for (const [source, destination] of assets) {
  await moveFile(source, destination);
}
