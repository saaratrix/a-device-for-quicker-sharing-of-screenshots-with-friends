import { FileInputEvent, fileInputEvent } from "./file-events.js";

export interface UploadInfo {
  extensions: string[];
  maxlengthFile: number;
  maxlengthUser: number;
}

export interface UploadResponse {
  url: string;
}

export class FileUploader {
    private uploadInfo: UploadInfo | undefined;
    canUpload = false;

    selectedFile: File | undefined;
    selectedKey: string = '';

  constructor() {
    window.addEventListener(fileInputEvent, (event) => this.onFileInput(event as CustomEvent<FileInputEvent>));

    document.getElementById('upload-btn')?.addEventListener('click', () => this.onSubmit());
    const secretsElement = document.getElementById('secret') as HTMLInputElement;
    secretsElement.addEventListener('input', (event) => {
      this.selectedKey = (event.target as HTMLInputElement).value;
      try {
        localStorage.setItem('key', this.selectedKey);
      } catch {}
    });

    try {
      this.selectedKey = localStorage.getItem('key') ?? '';
      secretsElement.value = this.selectedKey;
    } catch { }

    this.getUploadInfo(0).then((uploadInfo) => {
        this.uploadInfo = uploadInfo;
        this.canUpload = true;
        console.log('can now upload!');
        this.setUploadButtonStatus();
    })
    .catch(() => this.canUpload = false);
  }

  setUploadButtonStatus() {
    const uploadButton = document.getElementById('upload-btn') as HTMLButtonElement;
    if (!this.canUpload || !this.selectedFile ) {
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
      const request = fetch('http://localhost:5001/upload-info', {
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


  async onFileInput(event: CustomEvent<FileInputEvent>) {
    const file = event.detail;
    this.selectedFile = file;

    this.setUploadButtonStatus();
  }


  private async onSubmit() {
    if (!this.selectedFile || !this.canUpload) {
      return;
    }

    const formData = new FormData();
    formData.set('file', this.selectedFile);
    formData.set('key', this.selectedKey);

    const request = fetch('http://localhost:5001/upload', {
      method: 'PUT',
      body: formData,
    });
    const response = await request;
    const json = await response.json() as UploadResponse;
    console.log(json);
  }
}