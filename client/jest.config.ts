import type {Config} from 'jest';

const config: Config = {
  verbose: true,
  preset: 'ts-jest/presets/default-esm',
  // Need to change the order because if the build script has generated any .js files then tests won't run.
  // It complains on import & export not working.
  moduleFileExtensions: ['ts', 'js'],
  transform: {
    '^.+\\.ts$': ['ts-jest', {
      tsconfig: 'tsconfig.test.json',
    }],
  },
};

export default config;

