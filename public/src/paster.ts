import { dispatchFileInpit } from './file-events.js';

export class Paster {
  private currentObjectUrl: string = '';

  constructor() {
    // Add paste event listener to the document
    document.addEventListener('paste', (event) => this.onPaste(event));
    document.addEventListener('file:input', (event) => this.onFileInput(event as CustomEvent<Blob>));
  }

  onPaste(event: ClipboardEvent): void {
    const items = (event.clipboardData || (window as any).clipboardData).items;

    console.log('paste items', items);
    for (let index in items) {
      const item = items[index];

      // Check if the item is an image file
      if (item.kind === 'file' && item.type.indexOf('image') !== -1) {
        const blob = item.getAsFile();

        if (!blob) {
          break;  // For simplicity, handling only the first image found
        }
        console.log(blob);
        dispatchFileInpit(blob);
      }
    }
  }

  onFileInput(event: CustomEvent<Blob>): void {
      const blob = event.detail;

      if (this.currentObjectUrl) {
        URL.revokeObjectURL(this.currentObjectUrl);
      }

      this.currentObjectUrl = URL.createObjectURL(blob);

      // Create a new image element
      const img = document.createElement('img');
      img.style.width = '300px';  // Set width for visualization, adjust as needed
      img.style.height = 'auto';

      img.src = this.currentObjectUrl;

      // Append the image to the document or a specific container
      document.body.appendChild(img);
  }
}
