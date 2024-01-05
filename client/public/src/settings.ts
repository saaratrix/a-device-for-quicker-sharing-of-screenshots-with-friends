export interface SettingsConfig {
  automaticallyAdjustHeight?: boolean;
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

  public static saveSettings(): void {
    const json = JSON.stringify(this.getSettings());
    localStorage.setItem(Settings.settingsStorageKey, json);
  }

   public static getSettings(): SettingsConfig {
    if (!this._settings) {
      this._settings = new Settings();
    }

    return this._settings.config;
  }
}