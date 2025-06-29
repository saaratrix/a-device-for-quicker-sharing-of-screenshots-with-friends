import { FileInputEvent, fileInputEvent } from "./events/file-events.js";
import { EditRotationEvent, editRotationEvent } from './events/editing-events.js';

export const PreviewType = {
  Unknown: 'unknown',
  Image: 'image',
  Video: 'video',
  Audio: 'audio',
} as const;

/**
 * Updates the preview when a file is selected.
 */
export class FilePreviewer {
  private currentObjectUrl: string = '';
  private previewElement: HTMLDivElement | undefined;

  constructor() {
    window.addEventListener(fileInputEvent, (event) => this.onFileInput(event as CustomEvent<FileInputEvent>));
    window.addEventListener(editRotationEvent, (event) => this.onRotationChanged(event as CustomEvent<EditRotationEvent>));
  }

  static getPreviewType(file: File | undefined): typeof PreviewType[keyof typeof PreviewType] {
    if (!file) {
      return PreviewType.Unknown;
    }

    if (file.type.startsWith('image')) {
      return PreviewType.Image;
    } else if (file.type.startsWith('video')) {
      return PreviewType.Video
    } else if (file.type.startsWith('audio')) {
      return PreviewType.Audio;
    }

    return PreviewType.Unknown;
  }

  onFileInput(event: CustomEvent<FileInputEvent>): void {
    const file = event.detail;

    if (this.currentObjectUrl) {
      URL.revokeObjectURL(this.currentObjectUrl);
    }

    if (!file) {
      // This is bad to do here, then you can't see what you uploaded anymore.
      // this.clearPreview();
      return;
    }

    this.currentObjectUrl = URL.createObjectURL(file);

    const previewElement = this.getPreviewElement();
    previewElement.innerHTML = '';

    const previewType = FilePreviewer.getPreviewType(file);
    switch (previewType) {
      case PreviewType.Image:
        this.previewImage(file);
        break;
      case PreviewType.Video:
        this.previewVideo(file);
        break;
      case PreviewType.Audio:
        this.previewAudio(file);
        break;
      default:
        break;
    }
  }

  public clearPreview(): void {
    const previewElement = this.getPreviewElement();
    previewElement.innerHTML = '';
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

  private previewImage(_: File): void {
    // Create a new image element
    const img = document.createElement('img');
    img.style.width = '300px';  // Set width for visualization, adjust as needed
    img.style.height = 'auto';
    img.style.transition = `transform 100ms ease-in`;
    img.style.position = 'relative';

    img.addEventListener('load', () => {
      const previewElement = this.getPreviewElement();
      const previewWidth = previewElement.offsetWidth;
      const imgWidth = img.offsetWidth;

      const heightDifference = (previewWidth - imgWidth) / 2;
      img.style.top = `-${heightDifference}px`;
    }, { once: true });

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

  private onRotationChanged(event: CustomEvent<EditRotationEvent>) {
    const img = this.getPreviewElement().querySelector('img') as HTMLImageElement;
    if (!img) {
      return;
    }

    img.style.transform = `rotate(${event.detail}deg)`;
  }
}