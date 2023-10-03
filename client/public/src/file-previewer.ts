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

    if (file.type.startsWith('image')) {
      this.previewImage(file);
    } else if (file.type.startsWith('video')) {
      this.previewVideo(file);
    } else if (file.type.startsWith('audio')) {
      this.previewAudio(file);
    }
  }

  private previewImage(file: File): void {
    // Create a new image element
    const img = document.createElement('img');
    img.style.width = '300px';  // Set width for visualization, adjust as needed
    img.style.height = 'auto';

    img.src = this.currentObjectUrl;
    this.getPreviewElement().appendChild(img);
  }

  private previewVideo(file: File): void {
    const video = document.createElement('video');
    video.controls = true;
    const source = document.createElement('source');
    source.type = file.type;
    source.src = this.currentObjectUrl;
    video.appendChild(source);
    this.getPreviewElement().appendChild(video);
  }

  private previewAudio(file: File): void {
    const audio = document.createElement('audio');
    audio.controls = true;
    audio.innerHTML = `<source src="${this.currentObjectUrl}" type="${file.type}">`

    this.getPreviewElement().appendChild(audio);
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