import { DragAndDrop } from './drag-and-drop.js';
import { Paster } from './paster.js';
import { FileUploader } from "./file-uploader.js";
import { FileViewer } from "./file-viewer.js";
import { FilePreviewer } from "./file-previewer.js";
import { dispatchFileInput } from "./events/file-events.js";
import { canUseLocalStorage, HistoryHandler } from "./history-handler.js";

document.addEventListener('DOMContentLoaded', async () => {
  const uploaderElement = document.getElementById('uploader');
  const viewerElement = document.getElementById('viewer');
  // Reason for this example is if we're on index.html and you paste the shared url it would not change the url.
  // As we're dealing with #.
  initItemChange();

  const fileViewer = new FileViewer();
  if (fileViewer.isViewUrl()) {
    initViewer(viewerElement!, fileViewer);
  } else {
    initUploader(uploaderElement!);
  }
});

function initItemChange(): void {
  window.addEventListener('hashchange', function() {
    const hash = window.location.hash.substring(1); // Get hash, remove the '#'
    if (hash.startsWith('/v/') || hash.startsWith('/d/')) {
      location.reload();
    }
  });
}

function initViewer(viewerElement: HTMLElement, fileViewer: FileViewer): void {
  viewerElement.hidden = false;

  fileViewer.viewFile();
}

function initUploader(uploaderElement: HTMLElement): void {
  uploaderElement.hidden = false;

  document.title = 'upload a file';

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
  if (canUseLocalStorage()) {
    const historyHandler = new HistoryHandler(filePreviewer);
  }
}


