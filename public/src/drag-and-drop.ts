import { dispatchFileInpit } from './file-events.js';

export class DragAndDrop {
  initialize(dropAreaElement: HTMLElement) {
    // Add dragover event listener
    dropAreaElement?.addEventListener('dragover', (event) => {
      event.preventDefault(); // Prevent default to allow drop
      dropAreaElement.classList.add('dragging'); // Add a class for visual feedback
      console.log('dragover');
    });

    // Add dragleave event listener
    dropAreaElement?.addEventListener('dragleave', () => {
      dropAreaElement.classList.remove('dragging'); // Remove the visual feedback class
      console.log('dragleave');
    });


    window.addEventListener("dragover",function(e){
      e.preventDefault();
    });
    // Prevent file drops everywhere.
    window.addEventListener('drop', (event) => {
      event.preventDefault();
    });

    // Add drop event listener
    dropAreaElement?.addEventListener('drop', (event) => {
      event.preventDefault(); // Prevent default behavior
      dropAreaElement.classList.remove('dragging'); // Remove the visual feedback class
      console.log('drop');

      // Handle the files here
      const files = event.dataTransfer?.files;
      if (!files || files.length === 0) {
        return;
      }

      const file = files[0];
      const blob = new Blob([file], { type: file.type });
      dispatchFileInpit(blob);
    });
  }
}