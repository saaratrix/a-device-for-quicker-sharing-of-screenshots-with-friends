import { FileInputEvent, fileInputEvent } from "./file-events.js";
import { api } from "./environment.js";

export interface UploadInfo {
  extensions: string[];
  maxlengthFile: number;
  maxlengthSecret: number;
}

export interface UploadResponse {
  url: string;
}

export class FileUploader {
  private uploadInfo: UploadInfo | undefined;
  canUpload = false;

  filename: string = '';
  selectedFile: File | undefined;
  selectedSecret: string = '';

  constructor() {
    window.addEventListener(fileInputEvent, (event) => this.onFileInput(event as CustomEvent<FileInputEvent>));
    document.getElementById('upload-btn')?.addEventListener('click', () => this.onUploadClicked());
    document.getElementById('filename')!.addEventListener('input', (event) => this.onFilenameChange(event));

    this.initSecrets();
    this.initLinkSharing();
    this.initUploadingInfo();
  }

  initSecrets(): void {
    const secretsElement = document.getElementById('secret') as HTMLInputElement;
    secretsElement.addEventListener('input', (event) => {
      this.selectedSecret = (event.target as HTMLInputElement).value;
      try {
        localStorage.setItem('secret', this.selectedSecret);
      } catch {
      }
    });

    try {
      this.selectedSecret = localStorage.getItem('secret') ?? '';
      secretsElement.value = this.selectedSecret;
    } catch {
    }
  }

  initLinkSharing(): void {
    const linkShareElement = document.getElementById('link-share') as HTMLElement;
    const copyButton = linkShareElement.querySelector<HTMLElement>('.link-copy-btn') as HTMLElement;
    copyButton.addEventListener('click', () => this.copyLinkToClipboard());
  }

  initUploadingInfo(): void {
    this.getUploadInfo(0).then((uploadInfo) => {
      this.uploadInfo = uploadInfo;
      this.canUpload = true;
      this.setUploadButtonStatus();
      this.setupValidation();
    })
      .catch(() => this.canUpload = false);
  }

  setupValidation(): void {
    const uploadInfo = this.uploadInfo!;
    (document.getElementById('secret') as HTMLInputElement).maxLength = uploadInfo.maxlengthSecret;
    (document.getElementById('filename') as HTMLInputElement).maxLength = uploadInfo.maxlengthFile;
  }

  setUploadButtonStatus(): void {
    const uploadButton = document.getElementById('upload-btn') as HTMLButtonElement;
    if (!this.canUpload || !this.selectedFile) {
      uploadButton.disabled = true;
      return;
    }

    let found = false;
    const lowerFilename = this.filename.toLowerCase();
    for (const extension of this.uploadInfo!.extensions) {
      if (lowerFilename.endsWith(extension)) {
        found = true;
        break;
      }
    }

    if (!found) {
      uploadButton.disabled = true;
      return;
    }

    uploadButton.disabled = false;
  }

  async getUploadInfo(tries: number): Promise<UploadInfo> {
    let promise = new Promise<UploadInfo>(async (res, rej) => {
      await tryFetchUploadInfo(1, res, rej);
    });
    return promise;

    async function tryFetchUploadInfo(tries: number, res: (vaule: (UploadInfo | PromiseLike<UploadInfo>)) => void, rej: (reason: any) => void) {
      const request = fetch(`${api}/upload-info`, {
        method: "GET",
        mode: "cors",
      });
      try {
        const response = await request;
        const json = await response.json();
        res(json);
        return;
      } catch (e) {
        if (tries <= 5) {
          setTimeout(() => tryFetchUploadInfo(tries + 1, res, rej), 1000);
        } else {
          rej(`Failed getting upload info`);
          return;
        }

        console.error('Failed getting upload info, trying again', e);
      }
    }
  }

  private onFilenameChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.setFilename(target.value, false);
  }

  private setFilename(name: string, updateInput: boolean): void {
    this.filename = name;
    if (updateInput) {
      (document.getElementById('filename') as HTMLInputElement).value = name;
    }

    this.setUploadButtonStatus();
    this.onShareLinkChanged('');
  }

  private onShareLinkChanged(link: string): void {
    const linkShareElement = document.getElementById('link-share') as HTMLElement;
    const linkTextElement = linkShareElement.querySelector<HTMLSpanElement>('.link-text') as HTMLSpanElement;

    if (link === linkTextElement.innerHTML) {
      return;
    }

    !link ? linkShareElement.classList.add('invisible') : linkShareElement.classList.remove('invisible');
    linkTextElement.innerHTML = link;
  }

  async onFileInput(event: CustomEvent<FileInputEvent>) {
    const file = event.detail;
    this.selectedFile = file;

    let filename = file.name;
    if (this.uploadInfo) {
      let end = file.name.length;
      let start = file.name.length <= this.uploadInfo.maxlengthFile ? 0 : file.name.length - this.uploadInfo.maxlengthFile;
      filename = file.name.substring(start, end);
    }

    this.setFilename(filename, true);
    this.setUploadButtonStatus();
  }


  private async onUploadClicked() {
    if (!this.selectedFile || !this.canUpload) {
      return;
    }

    const formData = new FormData();
    formData.set('file', this.selectedFile);
    formData.set('filename', this.filename);
    formData.set('secret', this.selectedSecret);

    const uploadButton = document.getElementById('upload-btn') as HTMLButtonElement;
    uploadButton.classList.add('spinner');
    uploadButton.disabled = true;

    const request = fetch(`${api}/upload`, {
      method: 'PUT',
      body: formData,
    });

    try {
      const response = await request;
      const json = await response.json() as UploadResponse;
      let url = getShareUrl(json.url);
      url = encodeURIComponent(url);
      this.onShareLinkChanged(url);
    } finally {
      uploadButton.classList.remove('spinner');
      uploadButton.disabled = false;
    }
  }

  private copyLinkToClipboard() {
    const linkShareElement = document.getElementById('link-share') as HTMLElement;
    const linkTextElement = linkShareElement.querySelector<HTMLSpanElement>('.link-text') as HTMLSpanElement;
    const text = linkTextElement.innerHTML;

    if (!text) {
      return;
    }
    navigator.clipboard.writeText(text)
  }
}

export function getShareUrl(url: string) {
  return `${location.href}#${url}`;
}