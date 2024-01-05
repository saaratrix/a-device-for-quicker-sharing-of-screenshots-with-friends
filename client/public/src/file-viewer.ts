import { api } from './environment.js';
import { getShareUrl } from "./file-uploader.js";
import { Settings } from "./settings.js";

enum ViewingType {
  Download,
  Image,
  Video,
  Audio,
}

export class FileViewer {

  imageExtensions = [
    // Images
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp',
    // Textures
    '.tga',
  ];
  videoExtensions = [
    '.mp4', '.mkv', '.flv', '.webm', '.mov', '.avi', '.m4v',
  ];
  audioExtensions = [
    '.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a',
  ];

  private mimeTypes: Record<string, string> = {
    // Video
    '.mp4': 'video/mp4',
    '.mkv': 'video/x-matroska',
    '.flv': 'video/x-flv',
    '.webm': 'video/webm',
    '.mov': 'video/quicktime',
    '.avi': 'video/x-msvideo',
    '.m4v': 'video/x-m4v',
    // Audio
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.aac': 'audio/aac',
    '.flac': 'audio/flac',
    '.ogg': 'audio/ogg',
    '.m4a': 'audio/x-m4a',
  };


  isViewUrl(): boolean {
    const hashValue = window.location.hash;
    return hashValue.startsWith('#/v/') || hashValue.startsWith('#/d/');
  }

  viewFile(): void {
    const url = window.location.hash.substring(1);
    const [viewingType, extension] = this.getViewingType(url);
    if (viewingType === ViewingType.Download) {
      this.downloadFile(url);
      return;
    }

    document.title = url;

    if (viewingType === ViewingType.Image) {
      this.viewImage(url);
    } else if (viewingType === ViewingType.Video) {
      this.viewVideo(url, extension); // Assuming you have a method viewVideo similar to viewImage
    } else if (viewingType === ViewingType.Audio) {
      this.viewAudio(url, extension); // Assuming you have a method viewAudio
    }
  }

  getViewingType(url: string): [ViewingType, string] {
    if (url.startsWith('/d/')) {
      return [ViewingType.Download, ''];
    }

    // This is to normalize the file extensions.
    const lowerUrl = url.toLowerCase();

    const checks: [string[], ViewingType][] = [
      [this.imageExtensions, ViewingType.Image],
      [this.videoExtensions, ViewingType.Video],
      [this.audioExtensions, ViewingType.Audio],
    ]

    for (const [extensions, viewingType] of checks) {
      for (const extension of extensions) {
        if (lowerUrl.endsWith(extension)) {
          return [viewingType, extension];
        }
      }
    }

    return [ViewingType.Download, ''];
  }

  downloadFile(url: string): void {
    window.location.href = api + url;
  }

  private getViewerItem(): HTMLElement {
    return document.getElementById('view-item')!;
  }

  private viewImage(url: string): void {
    const image = new Image();
    image.src = api + url;

    this.setMaxDimensions(image);
    this.getViewerItem().appendChild(image);
  }

  private viewVideo(url: string, extension: string) {
    const mimeType = this.mimeTypes[extension];
    const fileUrl = api + url;
    this.getViewerItem().innerHTML = `<video controls autoplay>
        <source src="${ fileUrl }" type="${ mimeType }">
      </video>`;

    const videoElement = this.getViewerItem().querySelector('video') as HTMLVideoElement;
    this.setMaxDimensions(videoElement);

    this.getViewerItem().querySelector<HTMLSourceElement>('source')!.onerror = () => this.handleMediaError(url);
  }

  private viewAudio(url: string, extension: string) {
    const mimeType = this.mimeTypes[extension];
    const fileUrl = api + url;
    this.getViewerItem().innerHTML = `<audio controls>
        <source src="${ fileUrl }" type="${ mimeType }">
      </audio>`;

    this.getViewerItem().querySelector<HTMLSourceElement>('source')!.onerror = () => this.handleMediaError(url);
  }

  private setMaxDimensions(element: HTMLElement): void {
    const container = document.querySelector('.container') as HTMLElement;
    const maxHeight = window.innerHeight - this.getOccupiedHeight();

    element.style.maxWidth = `${ container.clientWidth }px`;

    if (Settings.getSettings().automaticallyAdjustHeight) {
      element.style.maxHeight = `${maxHeight}px`;
    }
  }

  private getOccupiedHeight(): number {
    const viewer = document.getElementById('viewer')!;
    const viewerStyle = getComputedStyle(viewer);

    const viewerPadding = parseInt(viewerStyle.paddingTop) + parseInt(viewerStyle.paddingBottom);
    return viewerPadding;
  }

  private handleMediaError(url: string) {
    url = url.replace('/v/', '/d/');
    const downloadUrl = getShareUrl(url);

    const errorMessage = "Failed to load, here is download link: ";
    this.getViewerItem().innerHTML += `<p style="color: #a42929">${ errorMessage } <a href="${ downloadUrl }">${ downloadUrl }</a></p>`;
  }

}