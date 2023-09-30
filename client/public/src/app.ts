import { DragAndDrop } from './drag-and-drop.js';
import { Paster } from './paster.js';
import { FileUploader } from "./file-uploader.js";
import { FileViewer } from "./file-viewer.js";
import { FilePreviewer } from "./file-previewer.js";
import { dispatchFileInput } from "./file-events.js";

document.addEventListener('DOMContentLoaded', async () => {
  const uploaderElement = document.getElementById('uploader');
  const viewerElement = document.getElementById('viewer');

  const fileViewer = new FileViewer();
  if (fileViewer.isViewUrl()) {
    initViewer(viewerElement!);
  } else {
    initUploader(uploaderElement!);
  }
});

function initViewer(viewerElement: HTMLElement): void {
  viewerElement.hidden = false;
}

function initUploader(uploaderElement: HTMLElement): void {
  uploaderElement.hidden = false;

  const dragAndDrop = new DragAndDrop();
  dragAndDrop.initialize();

  document.getElementById('fileInput')?.addEventListener('change', (event) => {
    const target = event.target as HTMLInputElement;
    const file = target.files?.[0];
    if (file) {
      dispatchFileInput(file);
    }
  })

  const paster = new Paster();
  // When uploading or pasting files the file uploader listens for those events.
  const fileUploader = new FileUploader();
  const filePreviewer = new FilePreviewer();
}


