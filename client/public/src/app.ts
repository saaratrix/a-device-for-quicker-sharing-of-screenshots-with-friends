import { DragAndDrop } from './drag-and-drop.js';
import { Paster } from './paster.js';

document.addEventListener('DOMContentLoaded', async () => {
  const dropArea = document.querySelector<HTMLElement>('.drag-drop-area');
  if (dropArea) {
    const dragAndDrop = new DragAndDrop();
    dragAndDrop.initialize(dropArea);
  }

  const paster = new Paster();

  const request = fetch('http://localhost:5001/view/small.png')
  try {
     const response = await request;
     console.log('response', response);
  } catch(e) {
    console.log('error', e);
  }

});