import { dispatchTransformEvent } from '../events/transform-events.js';

export interface Crop {
  x: number,
  y: number,
  width: number,
  height: number,
}

export interface TransformActions {
  rotation: number | undefined;
  crop: Crop | undefined;
}

export const currentTransformActions: TransformActions = {
  rotation: undefined,
  crop: undefined,
}

export function setTransformAction<K extends keyof TransformActions>(key: K, value: TransformActions[K]): void  {
  currentTransformActions[key] = value;
  dispatchTransformEvent(key);
}