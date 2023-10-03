import { dispatchFileInput, fileInputEvent } from './file-events.js';

export class Paster {
  private currentObjectUrl: string = '';

  constructor() {
    // Add paste event listener to the document
    document.addEventListener('paste', (event) => this.onPaste(event));
  }

  onPaste(event: ClipboardEvent): void {
    const items = (event.clipboardData || (window as any).clipboardData).items;

    for (let index in items) {
      const item = items[index];

      // Check if the item is an image file
      if (item.kind === 'file' && item.type.indexOf('image') !== -1) {
        const file = item.getAsFile();

        if (!file) {
          break;  // For simplicity, handling only the first image found
        }
        dispatchFileInput(file);
      }
    }
  }

}
