export interface Crop {
  x: number,
  y: number,
  width: number,
  height: number,
}

export interface EditingSettings {
  rotation?: number;
  crop?: Crop;
}