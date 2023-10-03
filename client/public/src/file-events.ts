export const fileInputEvent = 'file:input';
export type FileInputEvent = File;
export function dispatchFileInput(file: File) {
  window.dispatchEvent(new CustomEvent<FileInputEvent>(fileInputEvent, {
    detail: file,
  }));
}