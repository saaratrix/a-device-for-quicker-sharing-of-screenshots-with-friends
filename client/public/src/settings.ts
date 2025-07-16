export type ViewerControlsPlacement = 'page:left' | 'page:right' | 'item:left' | 'item:right';

export interface SettingsConfig {
  automaticallyAdjustHeight?: boolean;
  viewerControlsPlacement?: ViewerControlsPlacement;
}

export class Settings {
  private static _settings: Settings;
  public static readonly settingsStorageKey = 'settings';

  private readonly config: SettingsConfig;

  constructor() {
    this.config = this.loadSettings();
  }

  private loadSettings(): SettingsConfig {
    try {
      const json = localStorage.getItem(Settings.settingsStorageKey) ?? '{}';
      return JSON.parse(json) as SettingsConfig;
    } catch {
      return {};
    }
  }

  public static saveSettings(settings?: SettingsConfig): void {
    settings ??= this.getSettings();
    const json = JSON.stringify(settings);
    localStorage.setItem(Settings.settingsStorageKey, json);
  }

   public static getSettings(): SettingsConfig {
    if (!this._settings) {
      this._settings = new Settings();
    }

    return this._settings.config;
  }
}