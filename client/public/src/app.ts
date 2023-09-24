import { DragAndDrop } from './drag-and-drop.js';
import { Paster } from './paster.js';

document.addEventListener('DOMContentLoaded', () => {
  const dropArea = document.querySelector<HTMLElement>('.drag-drop-area');
  if (dropArea) {
    const dragAndDrop = new DragAndDrop();
    dragAndDrop.initialize(dropArea);
  }

  const paster = new Paster();
});