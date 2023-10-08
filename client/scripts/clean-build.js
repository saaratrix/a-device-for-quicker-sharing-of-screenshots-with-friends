import { rm } from 'fs/promises';
try {
  await rm('./build', { recursive: true });
  console.log('successfully removed build and the content.')
} catch(e) {
  if (e.code !== 'ENOENT') {
    console.error('Error removing build directory:', e.message);
  } else {
    console.log('Build directory does not exist, no need to clean directory.');
  }
}

