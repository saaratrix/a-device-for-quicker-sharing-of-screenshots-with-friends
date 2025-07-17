import { ViewingType } from '../viewer/viewer-state.js';

export const viewingItemChangedEvent = 'viewer:itemChanged';
export const viewingFailedToLoadEvent = 'viewer:failedToLoad';

// export type ViewingItemChangedEvent = ViewingType;
export const dispatchViewingItemChangedEvent = (viewingType: ViewingType) => {
  window.dispatchEvent(new CustomEvent<ViewingType>(viewingItemChangedEvent, {
    detail: viewingType,
  }));
}

export const dispatchViewingFailedToLoadEvent = () => {
  window.dispatchEvent(new CustomEvent<void>(viewingFailedToLoadEvent));
}