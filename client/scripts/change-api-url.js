import { writeFile } from 'fs/promises';

if (!process.env.API_URL) {
    console.error('API_URL environment variable is not set.');
    process.exit(1);
}

const apiUrl = process.env.API_URL;

try {
  const content = `
export const api = '${apiUrl}';
`;

  await writeFile('./build/src/environment.js', content);
  console.log('created new /build/src/environment.js');
} catch (e) {
  console.log('Failed to generate /build/src/environment.js', e.message, e);
}