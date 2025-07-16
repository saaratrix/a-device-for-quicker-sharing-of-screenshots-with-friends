import { viewerState, ViewingType } from './viewer-state.js';
import { viewingItemChangedEvent } from '../events/viewer-events.js';

type Feature = 'video:audio' | 'video:progress' | 'video:fullscreen' | 'rotate';

class ViewerControls extends HTMLElement {
  shadow: ShadowRoot;
  viewerControlsElement!: HTMLElement;
  activeFeatures: Set<Feature> = new Set();

  constructor() {
      super();
      this.shadow = this.attachShadow({ mode: 'open' });
      this.shadow.innerHTML = `
        <style>
          .viewer-controls {
            position: absolute;
            top: 0.5rem;
            left: 0.5rem;
            height: 40px;
            width: calc(100% - 2rem);
            
            display: flex;
            align-items: center;
            padding: 0 0.5rem;
          }
        </style>
        <div class="viewer-controls">
        </div>
      `;
    }

    private updateView(): void {
      // Conditionally add each feature.
      this.viewerControlsElement.innerHTML = `
        ${this.activeFeatures.has('video:audio') ? `<viewer-controls-audio />` : ''}
        ${this.activeFeatures.has('video:progress') ? `<viewer-controls-progress />` : ''}
        ${this.activeFeatures.has('video:fullscreen') ? `<viewer-controls-fullscreen />` : ''}
        ${this.activeFeatures.has('rotate') ? `<viewer-controls-rotate />` : ''}
      `;
    }

    connectedCallback () {
       this.viewerControlsElement = this.shadow.querySelector('.viewer-controls') as HTMLElement;
       if (!this.viewerControlsElement) {
         throw new Error("Viewer Controls failed to initialize, bad bad!");
       }

      window.addEventListener(viewingItemChangedEvent, this.onViewingItemChanged);

      this.setFeatures();
      this.updateView();
    }

    disconnectedCallback () {
      window.removeEventListener(viewingItemChangedEvent, this.onViewingItemChanged);
    }

    private onViewingItemChanged = (_: Event) => {
      this.setFeatures();
      this.updateView();
    };

  private setFeatures() {
    const features: Feature[] = [];
    switch (viewerState.viewingType) {
        case ViewingType.Video:
          features.push('video:audio', 'video:fullscreen', 'video:progress');
          features.push('rotate');
          break;
        case ViewingType.Image:
          features.push('rotate');
          break;
        default:
          break;
      }

    this.activeFeatures = new Set<Feature>(features);
  }
}

customElements.define('viewer-controls', ViewerControls);