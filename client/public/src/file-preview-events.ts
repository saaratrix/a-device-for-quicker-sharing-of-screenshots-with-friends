import type { SingleFilePicker } from './vendor/nui/file-picker/single-file-picker';
import { EditTransformChangedEvent, editTransformChangedEvent } from './events/transform-events.js';
import { currentTransformActions } from './editing/transform-actions.js';

export function initializeFilePreviewEvents(filePicker: SingleFilePicker) {
  window.addEventListener(editTransformChangedEvent, (e: Event) => {
    const event = e as CustomEvent<EditTransformChangedEvent>;
    if (event.detail !== 'rotation') {
      return;
    }

    const item = filePicker.pickerPreview.previewItem;
    if (!item || !('nodeName' in item) || item.nodeName !== 'IMG') {
      return;
    }

    // item.style.transform = `translateY(-50%) rotate(${currentTransformActions.rotation}deg)`;
    item.style.transform = `rotate(${currentTransformActions.rotation}deg)`;
  });
}