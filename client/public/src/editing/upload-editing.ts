import { type FileInputEvent, fileInputEvent } from '../events/file-events.js';
import { uploadSharedCSS } from './styles/upload-shared.js';
import { dispatchEditRotationEvent, getEditingSettingsEvent, GetEditSettingsEvent } from '../events/editing-events.js';
import { EditingSettings } from './editing-settings.js';
import { FilePreviewer, PreviewType } from '../file-previewer.js';

class UploadEditing extends HTMLElement {
  shadow: ShadowRoot;

  private _rotation: number = 0;
  get rotation(): number {
    return this._rotation;
  }

  set rotation(value: number) {
    this._rotation = value;
  };

  rotateLeft: HTMLButtonElement | null = null;
  rotateRight: HTMLButtonElement | null = null;

  constructor() {
      super();
      this.shadow = this.attachShadow({ mode: 'open' });
      this.shadow.adoptedStyleSheets = [uploadSharedCSS]

      // Styles and layout
      this.shadow.innerHTML = `
        <style>
          .upload-editing {
          }
          p {
            text-align: left;
            margin: 0;
          }
          .editor-buttons {
            display: flex;
            gap: 10px;
          }         
    
        </style>
        <div class="upload-editing">
          <div class="editor-buttons">
            <button class="icon-action" id="rotateLeft" title="Rotate 90° left." disabled>⟲ 90°</button>
            <button class="icon-action" id="rotateRight" title="Rotate 90° right." disabled>⟳ 90°</button>
          </div>
        </div>
        
      `;
    }

    connectedCallback () {
      window.addEventListener(fileInputEvent, this.onFileInput);
      window.addEventListener(getEditingSettingsEvent, this.onGetEditSettingsEvent)

      this.rotateLeft = this.shadow.getElementById('rotateLeft') as HTMLButtonElement;
      this.rotateRight = this.shadow.getElementById('rotateRight') as HTMLButtonElement;

      if (!this.rotateLeft || !this.rotateRight) {
        return;
      }

      this.rotateLeft.addEventListener('click', this.onRotateLeft);
      this.rotateRight.addEventListener('click', this.onRotateRight);
    }

    disconnectedCallback () {
      window.removeEventListener(fileInputEvent, this.onFileInput);
      window.removeEventListener(getEditingSettingsEvent, this.onGetEditSettingsEvent);

      if (!this.rotateLeft || !this.rotateRight) {
        return;
      }

      this.rotateLeft.removeEventListener('click', this.onRotateLeft);
      this.rotateRight.removeEventListener('click', this.onRotateRight);
    }

    private onGetEditSettingsEvent = (e: Event): void => {
      const event = e as CustomEvent<GetEditSettingsEvent>;

      const settings: EditingSettings = event.detail.settings ?? {};
      if (this.rotation !== 0) {
        settings.rotation = this.rotation % 360;
      }

      if (event.detail && Object.keys(settings).length > 0) {
        event.detail.settings = settings;
      }
    }

    private onRotateLeft = () => {
      this.rotation -= 90;
      dispatchEditRotationEvent(this.rotation);
      // Need to blur or the :active state gets stuck.
      this.rotateLeft!.blur();
    };

    private onRotateRight = () => {
      this.rotation += 90;
      dispatchEditRotationEvent(this.rotation);
      // Need to blur or the :active state gets stuck.
      this.rotateRight!.blur();
    };

    private onFileInput = (e: Event) => {
      const event = e as CustomEvent<FileInputEvent>;

      const hasFile = !!event.detail;
      const previewType = FilePreviewer.getPreviewType(event.detail);

      const supportsRotation = hasFile && previewType === PreviewType.Image;

      this.rotateRight && (this.rotateRight.disabled = !supportsRotation);
      this.rotateLeft && (this.rotateLeft.disabled = !supportsRotation);
      this.rotation = 0;
    }


}

 customElements.define('upload-editing', UploadEditing);