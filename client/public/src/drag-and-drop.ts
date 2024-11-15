import { dispatchFileInput } from './events/file-events.js';

export class DragAndDrop {
  initialize() {
    const dragAndDropELement = document.querySelector('.drag-drop-area') as HTMLElement;

    document.addEventListener('dragover', (event) => {
      document.body.classList.add('drag');
      event.preventDefault(); // Prevent default to allow drop
    });

    // Failsafe if the state gets stuck, which has happened a few times.
    dragAndDropELement.addEventListener('click', () => {
      document.body.classList.remove('drag');
    });

    dragAndDropELement.addEventListener('dragleave', (event) => {
        document.body.classList.remove('drag');
    });

    dragAndDropELement.addEventListener('drop', (event) => {
      document.body.classList.remove('drag');
      event.preventDefault(); // Prevent default behavior

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

  }
}