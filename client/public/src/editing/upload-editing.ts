import { type FileInputEvent, fileInputEvent } from '../events/file-events.js';
import { uploadSharedCSS } from './styles/upload-shared.js';
import { setTransformAction } from './transform-actions.js';
import { FilePickerPreview, PreviewType } from '../vendor/nui/file-picker/file-picker-preview.js';

class UploadEditing extends HTMLElement {
  shadow: ShadowRoot;

  private _rotation: number = 0;
  get rotation(): number {
    return this._rotation;
  }

  set rotation(value: number) {
    this._rotation = value;
  };

  rotateLabel: HTMLElement | null = null;
  rotateLeft: HTMLButtonElement | null = null;
  rotateRight: HTMLButtonElement | null = null;

  constructor() {
      super();
      this.shadow = this.attachShadow({ mode: 'open' });
      this.shadow.adoptedStyleSheets = [uploadSharedCSS]
      // language=HTML
    this.shadow.innerHTML = `
        <style>
            .upload-editing {
                color: var(--color-text);
                display: flex;
                /* Temporary until there are 2 actions. */
                flex-direction: row-reverse;
            }

            .editor-row {
                display: inline-flex;
                flex-direction: column;
                align-items: center;
                gap: 0.25em;
                /*color: var(--muted);*/
            }

            .editor-row label {
                display: block;
                width: 100%;
                font-size: 0.85em;
                /*text-align: right;*/
            }

            .editor-buttons {
                display: flex;
                gap: 10px;
            }
            
            .disabled {
                color: var(--color-text-disabled);
            }

            .editor-buttons button {
                padding: 0.33em 0.66em;
                border: 1px solid rgba(124, 135, 174, .45);
                border-radius: 10px;
                background: var(--button-base-bg-muted);
                color: var(--color-text-disabled);
                cursor: pointer;
            }
            
            .editor-buttons button[disabled] {
                cursor: default;
            }

            .editor-buttons button:hover:not([disabled]) {
                background: var(--button-base-bg);
                color: var(--color-text);
            }

        </style>
        <div class="upload-editing">
            <div class="editor-row">
                <label class="rotation-label disabled">Rotation</label>
                <div class="editor-buttons">
                    <button class="button-base" id="rotateLeft" title="Rotate 90° left." disabled>↶ 90°</button>
                    <button class="button-base" id="rotateRight" title="Rotate 90° right." disabled>↷ 90°</button>
                </div>
            </div>

        </div>
    `;
    }

    connectedCallback () {
      window.addEventListener(fileInputEvent, this.onFileInput);

      this.rotateLeft = this.shadow.getElementById('rotateLeft') as HTMLButtonElement;
      this.rotateRight = this.shadow.getElementById('rotateRight') as HTMLButtonElement;
      this.rotateLabel = this.shadow.querySelector('.rotation-label') as HTMLElement;

      if (!this.rotateLeft || !this.rotateRight) {
        return;
      }

      this.rotateLeft.addEventListener('click', this.onRotateLeft);
      this.rotateRight.addEventListener('click', this.onRotateRight);
    }

    disconnectedCallback () {
      window.removeEventListener(fileInputEvent, this.onFileInput);

      if (!this.rotateLeft || !this.rotateRight) {
        return;
      }

      this.rotateLeft.removeEventListener('click', this.onRotateLeft);
      this.rotateRight.removeEventListener('click', this.onRotateRight);
    }

    private onRotateLeft = () => {
      this.rotation -= 90;
      setTransformAction('rotation', this.rotation);
      // Need to blur or the :active state gets stuck.
      this.rotateLeft!.blur();
    };

    private onRotateRight = () => {
      this.rotation += 90;
      setTransformAction('rotation', this.rotation);
      // Need to blur or the :active state gets stuck.
      this.rotateRight!.blur();
    };

    private onFileInput = (e: Event) => {
      const event = e as CustomEvent<FileInputEvent>;

      const hasFile = !!event.detail;
      const previewType = FilePickerPreview.getPreviewType(event.detail);

      const supportsRotation = hasFile && previewType === PreviewType.Image;

      this.rotateRight && (this.rotateRight.disabled = !supportsRotation);
      this.rotateLeft && (this.rotateLeft.disabled = !supportsRotation);
      this.rotateLabel?.classList.toggle('disabled', !supportsRotation);
      this.rotation = 0;
    }


}

 customElements.define('upload-editing', UploadEditing);