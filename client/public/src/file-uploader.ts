import { dispatchFileUploaded, FileInputEvent, fileInputEvent, FileUploadedEvent, fileUploadedEvent } from "./events/file-events.js";
import { api } from "./environment.js";
import { copyUrlToClipboard } from "./utility/copy-url-to-clipboard.js";
import { currentTransformActions } from './editing/transform-actions.js';

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

  canClearShareLinkTime = -1;

  constructor() {
    window.addEventListener(fileInputEvent, (event) => this.onFileInput(event as CustomEvent<FileInputEvent>));
    window.addEventListener(fileUploadedEvent, (event) => this.onFileUpload(event as CustomEvent<FileUploadedEvent>));
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
    this.getUploadInfo().then((uploadInfo) => {
      this.uploadInfo = uploadInfo;
      this.canUpload = true;
      this.setUploadButtonStatus();
      this.setupValidation();
    })
      .catch(() => {
        this.canUpload = false;
        this.showOrHideError('Can\'t connect to server. Please try again or some other time.');
      });
  }

  showOrHideError(error: string | false) {
    const errorElement = document.getElementById('upload-error') as HTMLParagraphElement;
    if (!errorElement) {
      return;
    }

    errorElement.hidden = !error;
    errorElement.innerText = error;
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
      console.log('upload button disabled');
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
      console.log('upload button disabled');
      uploadButton.disabled = true;
      return;
    }

    console.log('upload button enabled');
    uploadButton.disabled = false;
  }

  async getUploadInfo(): Promise<UploadInfo> {
    let promise = new Promise<UploadInfo>(async (res, rej) => {
      await tryFetchUploadInfo(1, res, rej);
    });
    return promise;

    async function tryFetchUploadInfo(tries: number, res: (value: (UploadInfo | PromiseLike<UploadInfo>)) => void, rej: (reason: any) => void) {
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
    // This is so that when the uploaded file is cleared we don't clear the shared link, timings ^.^
    if (performance.now() > this.canClearShareLinkTime) {
      this.onShareLinkChanged('');
    }
  }

  private onShareLinkChanged(link: string): void {
    const linkShareElement = document.getElementById('link-share') as HTMLElement;
    const linkTextElement = linkShareElement.querySelector('.link-text') as HTMLAnchorElement;

    if (link === linkTextElement.innerHTML) {
      return;
    }

    !link ? linkShareElement.classList.add('invisible') : linkShareElement.classList.remove('invisible');
    linkTextElement.innerHTML = link;
    linkTextElement.href = link || '#';
  }

  async onFileInput(event: CustomEvent<FileInputEvent>) {
    const file = event.detail;
    this.selectedFile = file;

    let filename = '';
    if (file) {
      filename = file.name;
      if (this.uploadInfo) {
        let end = file.name.length;
        let start = file.name.length <= this.uploadInfo.maxlengthFile ? 0 : file.name.length - this.uploadInfo.maxlengthFile;
        filename = file.name.substring(start, end);
      }
    }
    this.setFilename(filename, true);
    this.showOrHideError(false);
  }


  private async onUploadClicked() {
    if (!this.selectedFile || !this.canUpload) {
      return;
    }

    const formData = new FormData();
    formData.set('file', this.selectedFile);
    formData.set('filename', this.filename);
    formData.set('secret', this.selectedSecret);


    const transformActions = this.getTransformActionsJson();
    if (transformActions) {
      formData.set('transformActions', transformActions);
    }

    const uploadButton = document.getElementById('upload-btn') as HTMLButtonElement;
    uploadButton.classList.add('spinner');
    uploadButton.disabled = true;

    this.showOrHideError(false);

    const request = fetch(`${api}/upload`, {
      method: 'PUT',
      body: formData,
    });

    try {
      const response = await request;
      if (response.status !== 200) {
        const text = await response.text();
        this.showOrHideError(text);
        return;
      } else {
        const json = await response.json() as UploadResponse;
        const url = getShareUrl(json.url);
        this.onShareLinkChanged(url);
      }
      dispatchFileUploaded(url);
    } catch (e) {
      this.showOrHideError(e);
    } finally {
      uploadButton.classList.remove('spinner');
      uploadButton.disabled = false;
    }
  }

  private getTransformActionsJson() {
    const transformActions = { ...currentTransformActions };
    const hasRotation = transformActions.rotation !== undefined && transformActions.rotation !== 0;
    const shouldTransformFile = hasRotation;

    if (!shouldTransformFile) {
      return '';
    }

    if (hasRotation) {
      transformActions.rotation = transformActions.rotation! % 360;
    }

    return JSON.stringify(transformActions);
  }

  private copyLinkToClipboard() {
    const linkShareElement = document.getElementById('link-share') as HTMLElement;
    copyUrlToClipboard(linkShareElement, '.link-text');
  }

  private onFileUpload(_: CustomEvent<FileUploadedEvent>) {
    this.canClearShareLinkTime = performance.now() + 100;
  }
}

export function getShareUrl(url: string) {
  const baseUrl = window.location.origin + window.location.pathname;
  const components = url.split('/');
  const encodedUrl = components.map(c => encodeURIComponent(c)).join('/');

  // If we use window.location.href and we already have a #, well we end up with 2 :) 
  return `${baseUrl}#${encodedUrl}`;
}