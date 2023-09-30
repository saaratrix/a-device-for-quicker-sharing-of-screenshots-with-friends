import { dispatchFileInput } from './file-events.js';

export class DragAndDrop {
  initialize() {
    // Add dragover event listener
    document.addEventListener('dragover', (event) => {
      event.preventDefault(); // Prevent default to allow drop
      // dropAreaElement.classList.add('dragging'); // Add a class for visual feedback
      console.log('dragover');
    });

    // Add dragleave event listener
    document.addEventListener('dragleave', () => {
      // dropAreaElement.classList.remove('dragging'); // Remove the visual feedback class
      console.log('dragleave');
    });

    document.addEventListener('drop', (event) => {
      event.preventDefault(); // Prevent default behavior
      // dropAreaElement.classList.remove('dragging'); // Remove the visual feedback class
      console.log('drop');

      // Handle the files here
      const files = event.dataTransfer?.files;
      if (!files || files.length === 0) {
        return;
      }

      dispatchFileInput(files[0]);
    });

    window.addEventListener("dragover",function(e){
      e.preventDefault();
    });
    // Prevent file drops everywhere.
    window.addEventListener('drop', (event) => {
      event.preventDefault();
    });

    // Add drop event listener

  }
}