import { FileInputEvent, fileInputEvent } from "./file-events.js";


/**
 * Updates the preview when a file is selected.
 */
export class FilePreviewer {
  private currentObjectUrl: string = '';
  private previewElement: HTMLDivElement | undefined;

  constructor() {
    window.addEventListener(fileInputEvent, (event) => this.onFileInput(event as CustomEvent<FileInputEvent>));
  }

  onFileInput(event: CustomEvent<FileInputEvent>) {
    const file = event.detail;

    if (this.currentObjectUrl) {
      URL.revokeObjectURL(this.currentObjectUrl);
    }

    this.currentObjectUrl = URL.createObjectURL(file);

    const previewElement = this.getPreviewElement();
    previewElement.innerHTML = '';

    // Create a new image element
    const img = document.createElement('img');
    img.style.width = '300px';  // Set width for visualization, adjust as needed
    img.style.height = 'auto';

    img.src = this.currentObjectUrl;
    previewElement.appendChild(img);

  }

  private getPreviewElement(): HTMLElement {
    if (this.previewElement) {
      return this.previewElement;
    }

    const previewElement = document.createElement('div');
    previewElement.classList.add('preview');
    this.previewElement = previewElement;
    document.body.appendChild(previewElement);
    return this.previewElement;
  }
}