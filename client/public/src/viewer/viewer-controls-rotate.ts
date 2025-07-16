import { uploadSharedCSS } from '../editing/styles/upload-shared.js';
import { viewingItemChangedEvent } from '../events/viewer-events.js';

export class ViewerControlsRotate extends HTMLElement {
  shadow: ShadowRoot;

  private _rotation: number = 0;

  viewItem!: HTMLElement;
  rotateLeft: HTMLButtonElement | null = null;
  rotateRight: HTMLButtonElement | null = null;

  viewContainerSize: { width: number, height: number } | undefined = undefined;

  // Bit excessive typing, was just curious if it works, and it does :P
  translatePart: ` translate(${number}px, ${number}px)` | '' = '';

  get rotation(): number {
    return this._rotation;
  }

  set rotation(value: number) {
    this._rotation = value;
  };

  constructor() {
    super();
    this.shadow = this.attachShadow({ mode: 'open' });

    this.shadow.adoptedStyleSheets = [uploadSharedCSS]
      this.shadow.innerHTML = `
        <style>
            .viewer-controls-rotate {
                display: inline-flex;
                gap: 0.5rem;
            }
            
            .icon-action {
            
            }
        </style>
        <div class="viewer-controls-rotate">
            <button class="rotate-left icon-action" title="Rotate 90° left.">⟲ 90°</button>
            <button class="rotate-right icon-action" title="Rotate 90° right.">⟳ 90°</button>
        </div>
      `;
  }

  connectedCallback () {

    window.addEventListener(viewingItemChangedEvent, this.onViewingItemChanged)

    this.rotateLeft = this.shadow.querySelector('.rotate-left') as HTMLButtonElement;
    this.rotateRight = this.shadow.querySelector('.rotate-right') as HTMLButtonElement;
    this.viewItem = document.getElementById('view-item') as HTMLElement;

    if (!this.rotateLeft || !this.rotateRight || !this.viewItem) {
      return;
    }

    this.rotateLeft.addEventListener('click', this.onRotateLeft);
    this.rotateRight.addEventListener('click', this.onRotateRight);
  }

  disconnectedCallback () {
    window.removeEventListener(viewingItemChangedEvent, this.onViewingItemChanged)

    if (!this.rotateLeft || !this.rotateRight) {
      return;
    }

    this.rotateLeft.removeEventListener('click', this.onRotateLeft);
    this.rotateRight.removeEventListener('click', this.onRotateRight);
  }

  private onViewingItemChanged = () => {
    this.rotation = 0;
    this.viewContainerSize = undefined;
    this.translatePart = '';
  };

  private onRotateLeft = () => {
    this.rotation -= 90;
    // Need to blur or the :active state gets stuck.
    this.rotateLeft!.blur();
    this.calculateTranslation();
    this.viewItem.style.transform = `rotate(${this.rotation}deg)${this.translatePart}`;
  };

  private onRotateRight = () => {
    this.rotation += 90;
    // Need to blur or the :active state gets stuck.
    this.rotateRight!.blur();
    this.calculateTranslation();
    this.viewItem.style.transform = `rotate(${this.rotation}deg)${this.translatePart}`;
  };

  private calculateTranslation(): void {
    if (!this.viewContainerSize) {
      // For example a too wide image will be pushed too far up so you can't see the full picture.
      const viewItemContainer = this.viewItem.parentElement as HTMLElement;
      this.viewContainerSize = {
        width: viewItemContainer.offsetWidth,
        height: viewItemContainer.offsetHeight,
      }
    }

    const rotation = Math.abs((this.rotation % 360) + 360) % 360;
    if (this.viewContainerSize.width === this.viewContainerSize.height || rotation === 0 || rotation === 180) {
      this.translatePart = '';
      return;
    }

    const direction = rotation === 90 ? 1 : -1;
    if (this.viewContainerSize.width > this.viewContainerSize.height) {
      const difference = (this.viewItem.offsetWidth - this.viewContainerSize.height) / 2;
      this.translatePart = ` translate(${difference * direction}px, 0px)`;
    }
    else {
      // I'm not exactly sure why 32 but seems to be related to padding, and a tall image is already capped in some ways width wise.
      const difference = 32;
      this.translatePart = ` translate(0px, ${32 * -direction}px)`;
    }
  }
}

customElements.define('viewer-controls-rotate', ViewerControlsRotate);