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
    const keys: (keyof SettingsConfig)[] = ['automaticallyAdjustHeight'];

    for (const key of keys) {
      const value = this.settings[key] ?? false;
      const element = document.getElementById(key) as HTMLInputElement;
      element.checked = value;
      element.addEventListener('input', () => {
        this.settings[key] = element.checked;
        Settings.saveSettings();
      });
    }
  }
}