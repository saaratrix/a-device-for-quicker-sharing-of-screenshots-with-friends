import { viewerState, ViewingType } from './viewer-state.js';
import { viewingItemChangedEvent } from '../events/viewer-events.js';
import { Settings } from '../settings.js';

type Feature = 'video:audio' | 'video:progress' | 'video:fullscreen' | 'rotate';

class ViewerControls extends HTMLElement {
  shadow: ShadowRoot;
  featuresElement!: HTMLElement;
  activeFeatures: Set<Feature> = new Set();

  constructor() {
      super();
      this.shadow = this.attachShadow({ mode: 'open' });

      const [controlsCSS, featuresCSS] = this.getPositionCSS();

      this.shadow.innerHTML = `
        <style>
          .viewer-controls {
            ${controlsCSS}            
            left: 0.5rem;
            height: 55px;
            width: calc(100% - 2rem);
            
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 0 0.5rem;
            
            opacity: 0;
            transition: opacity 100ms ease-in;
          }
          
          .viewer-controls:hover {
            opacity: 0.7
          }
          
          .features {
            display: flex;
            ${featuresCSS}
          }
          
          .extra-space {
            width: 100%;
            height: 15px;
          }
          
        </style>
        <div class="viewer-controls">
            <div class="features"></div>
            <div class="extra-space"></div>
        </div>
      `;
    }

    private getPositionCSS(): [controlCSS: string, featuresCSS: string | '']  {
      const settings = Settings.getSettings();
      const placement = settings.viewerControlsPlacement ?? 'page:left';

      let position: string;
      let side: string;

      switch (placement) {
        case 'page:left':
        case 'page:right':
          position = `position: fixed; top: 0;`;
          break;
        default:
          position = 'position: absolute; top: 0.25rem;';
      }

      switch (placement) {
        case 'item:right':
        case 'page:right':
          side = 'justify-content: flex-end;';
          break;
        // No need to do anything if left align as it's default.
        default:
          side = '';
          break;
      }

      return [position, side];
    }

    private get

    private updateView(): void {
      // Conditionally add each feature.
      this.featuresElement.innerHTML = `
        ${this.activeFeatures.has('video:audio') ? `<viewer-controls-audio />` : ''}
        ${this.activeFeatures.has('video:progress') ? `<viewer-controls-progress />` : ''}
        ${this.activeFeatures.has('video:fullscreen') ? `<viewer-controls-fullscreen />` : ''}
        ${this.activeFeatures.has('rotate') ? `<viewer-controls-rotate />` : ''}
      `;
    }

    connectedCallback () {
       this.featuresElement = this.shadow.querySelector('.features') as HTMLElement;
       if (!this.featuresElement) {
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