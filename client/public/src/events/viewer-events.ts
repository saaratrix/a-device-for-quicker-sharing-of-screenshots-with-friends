import { ViewingType } from '../viewer/file-viewer.js';

export const viewingItemChangedEvent = 'viewer:itemChanged';

// export type ViewingItemChangedEvent = ViewingType;
export const dispatchViewingItemChangedEvent = (viewingType: ViewingType) => {
  window.dispatchEvent(new CustomEvent<ViewingType>(viewingItemChangedEvent, {
    detail: viewingType,
  }));
}