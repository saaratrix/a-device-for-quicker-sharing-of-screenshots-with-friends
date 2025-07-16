import { DialogHandler } from './dialog-handler.js';
import { Settings, SettingsConfig } from "./settings.js";

export class SettingsHandler extends DialogHandler {
  private readonly settings: SettingsConfig;

  constructor() {
    const dialogElement = document.querySelector('.settings-dialog') as HTMLDialogElement;
    super(dialogElement);

    this.settings = Settings.getSettings();
    this.initSettings();

    const button = document.querySelector('.settings') as SVGElement;
    button.addEventListener('click', this.openDialog);
  }

  private initSettings(): void {
    const checkboxKeys = ['automaticallyAdjustHeight'] as const;

    for (const key of checkboxKeys) {
      const value = this.settings[key] ?? false;
      const element = document.getElementById(key) as HTMLInputElement;
      element.checked = value;
      element.addEventListener('input', () => {
        this.settings[key] = element.checked;
        Settings.saveSettings(this.settings);
      });
    }

    const dropdownKeys = [{ key: 'viewerControlsPlacement', defaultValue: 'page:left'}] as const;
    for (const { key, defaultValue } of dropdownKeys) {
      const value = this.settings[key] ?? defaultValue;
      const element = document.getElementById(key) as HTMLSelectElement
      element.value = value;
      for (let i = 0; i < element.options.length; i++) {
        const option = element.options.item(i);
        if (option?.value === value) {
          element.selectedIndex = i;
          break;
        }
      }
      element.addEventListener('change', (event) => {
        this.settings[key] = element.value as any;
        Settings.saveSettings(this.settings);
      });
    }
  }
}