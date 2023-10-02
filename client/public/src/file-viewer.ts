import { api } from './environment.js';

enum ViewingType {
  Download,
  Image,
  Video,
  Audio,
}

export class FileViewer {
  /**
   * # Images
   *         '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp',
   *         # Videos
   *         '.mp4', '.mkv', '.flv', '.webm', '.mov', '.avi', '.m4v',
   *         # Audio
   *         '.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a',
   */
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


  isViewUrl(): boolean {
    const hashValue = window.location.hash;
    return hashValue.startsWith('#/v/') || hashValue.startsWith('#/d/');
  }

  viewFile(): void {
    const url  = window.location.hash.substring(1);
    const viewingType = this.getViewingType(url);
    if (viewingType === ViewingType.Download) {
      this.downloadFile(url);
      return;
    }

    if (viewingType === ViewingType.Image) {
      this.viewImage(url);
    } else if (viewingType === ViewingType.Video) {
      this.viewVideo(url); // Assuming you have a method viewVideo similar to viewImage
    } else if (viewingType === ViewingType.Audio) {
      this.viewAudio(url); // Assuming you have a method viewAudio
    }


  }

  getViewingType(url: string): ViewingType {
    if (url.startsWith('/d/')) {
      return ViewingType.Download;
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
          return viewingType
        }
      }
    }

    return ViewingType.Download;
  }

  downloadFile(url: string): void {
    window.location.href = api + url;
  }

  private viewImage(url: string): void {
    const image = new Image();
    image.src = api + url;

    const viewerItem = document.getElementById('view-item')!;
    viewerItem.appendChild(image);
  }

  private viewVideo(url: string) {

  }

  private viewAudio(url: string) {

  }
}