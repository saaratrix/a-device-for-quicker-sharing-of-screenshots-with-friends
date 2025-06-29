export const fileInputEvent = 'file:input';
export const fileUploadedEvent = 'file:uploaded';

export type FileInputEvent = File | undefined;
export function dispatchFileInput(file: FileInputEvent ) {
  window.dispatchEvent(new CustomEvent<FileInputEvent>(fileInputEvent, {
    detail: file,
  }));
}

export type FileUploadedEvent = string;
export function dispatchFileUploaded(event: FileUploadedEvent) {
  window.dispatchEvent(new CustomEvent<FileUploadedEvent>(fileUploadedEvent, {
    detail: event,
  }));
}