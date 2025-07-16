import { dispatchViewingItemChangedEvent } from '../events/viewer-events.js';

export enum ViewingType {
  // Really only used initially just to have a value.
  Unknown,
  Download,
  Image,
  Video,
  Audio,
}

class ViewerState {
  private _viewingType: ViewingType = ViewingType.Unknown;
  public get viewingType(): ViewingType {
    return this._viewingType;
  }

  public set viewingType(value: ViewingType) {
    this._viewingType = value;
    dispatchViewingItemChangedEvent(this._viewingType);
  }
}

export const viewerState = new ViewerState();
