import { FileInputEvent, fileInputEvent } from "./events/file-events.js";


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

  public async getThumbnailAsBase64(): Promise<string> {
    const previewElement = this.getPreviewElement();
    const image = previewElement.querySelector('img');
    if (image) {
      return this.getThumbnailAsBase64FromImage(image);
    }
    const video = previewElement.querySelector('video');
    if (video) {
      return this.getThumbnailAsBase64FromVideo(video);
    }

    return '';
  }

  private getThumbnailAsBase64FromImage(image: HTMLImageElement) {
    let  thumbnailSize = Math.min(64, Math.max(image.naturalWidth, image.naturalHeight));

    const widthRatio = thumbnailSize / image.width;
    const heightRatio = thumbnailSize / image.height;
    const scale = Math.min(widthRatio, heightRatio);

    const canvasWidth = scale * image.width;
    const canvasHeight = scale * image.height;

    const canvas = document.createElement('canvas');
    canvas.width = canvasWidth;
    canvas.height = canvasHeight;
    const ctx = canvas.getContext('2d') as CanvasRenderingContext2D;
    ctx.drawImage(image, 0, 0, canvasWidth, canvasHeight);

    const dataUrl = canvas.toDataURL();
    return dataUrl;
  }

  /**
   * Get thumbnail from video as base 64, currently doesn't seek or anything so whatever the user has the frame as, we'll use that.
   * @param video
   * @private
   */
  private getThumbnailAsBase64FromVideo(video: HTMLVideoElement): Promise<string> {
    const currentTime = video.currentTime;
    video.currentTime = 0;

    return new Promise<string>(res => {
      video.addEventListener('seeked', () => {
        const thumbnailSize = Math.min(64, Math.max(video.videoWidth, video.videoHeight));
        const canvas = document.createElement('canvas');
        const scale = Math.min(thumbnailSize / video.videoWidth, thumbnailSize / video.videoHeight);

        canvas.width = video.videoWidth * scale;
        canvas.height = video.videoHeight * scale;
        const ctx = canvas.getContext('2d') as CanvasRenderingContext2D;

        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataUrl = canvas.toDataURL();

        video.currentTime = currentTime;
        res(dataUrl);
      }, { once: true });
    });
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