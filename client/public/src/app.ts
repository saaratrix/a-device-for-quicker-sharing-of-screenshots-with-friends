import { DragAndDrop } from './drag-and-drop.js';
import { Paster } from './paster.js';
import { FileUploader } from "./file-uploader.js";
import { FileViewer } from "./file-viewer.js";
import { FilePreviewer } from "./file-previewer.js";
import { dispatchFileInput, dispatchFileUploaded, fileUploadedEvent } from "./events/file-events.js";
import { canUseLocalStorage, HistoryHandler } from "./history-handler.js";
import { SettingsHandler } from "./settings-handler.js";
import { ViewerSimplePanner } from "./viewer-simple-panner.js";
import { PersistentPositionOnZoom } from "./persistent-position-on-zoom.js";

import './custom-components.js';

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
  let currentHash = getHash();

  window.addEventListener('hashchange', function() {
    const hash = getHash();
    if (isHashForItem(hash) || isHashForItem(currentHash)) {
      location.reload();
      return;
    }

    currentHash = hash;
  });
}

function getHash(): string {
  // Remove the '#'
  return window.location.hash.substring(1);
}

function isHashForItem(hash: string): boolean {
  return hash.startsWith('/v/') || hash.startsWith('/d/');
}

function initViewer(viewerElement: HTMLElement, fileViewer: FileViewer): void {
  viewerElement.hidden = false;
  document.body.classList.add('viewer-root');
  fileViewer.viewFile();

  const panner = new ViewerSimplePanner();
  const persistentPositionOnZoom = new PersistentPositionOnZoom();
}

function initUploader(uploaderElement: HTMLElement): void {
  uploaderElement.hidden = false;

  document.title = 'upload a file';

  const dragAndDrop = new DragAndDrop();
  dragAndDrop.initialize();

  const fileInput = document.getElementById('fileInput') as HTMLInputElement;
  if (fileInput) {
    fileInput.addEventListener('change', (event) => {
      const target = event.target as HTMLInputElement;
      const file = target.files?.[0];
      if (file) {
        dispatchFileInput(file);
      }
    });

    // Clear the file input after upload.
    window.addEventListener(fileUploadedEvent, () => {
      fileInput.value = '';
      // This is to let others process fileUploadedEvent first.
      setTimeout(() => dispatchFileInput(undefined));
    });
  }


  document.body.classList.add('uploader-root');

  const paster = new Paster();
  // When uploading or pasting files the file uploader listens for those events.
  const fileUploader = new FileUploader();
  const filePreviewer = new FilePreviewer();
  const settingsHandler = new SettingsHandler();
  if (canUseLocalStorage()) {
    const historyHandler = new HistoryHandler(filePreviewer);
  }
}


