export function dispatchFileInpit(blob: Blob) {
  document.dispatchEvent(new CustomEvent<Blob>('file:input', {
    detail: blob,
  }));
}