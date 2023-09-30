export class FileViewer {
  isViewUrl(): boolean {
    return false;
  }

  viewFile(): void {

  }

  async fetchImage(): Promise<void> {
    const request = fetch('http://localhost:5001/v/23/09/30/abcd/test/test.jpg', {
      method: "GET",
      mode: "cors",
    })
    try {
      const response = await request;
      console.log('response', response);
    } catch (e) {
      console.log('error', e);
    }
  }
}