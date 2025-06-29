import { EditingSettings } from '../editing/editing-settings.js';

export const getEditingSettingsEvent = 'edit:settings';
export const editRotationEvent = 'edit:rotate';


export type GetEditSettingsEvent = { settings?: EditingSettings };
export function dispatchGetEditSettingsEvent(target: GetEditSettingsEvent) {
  window.dispatchEvent(new CustomEvent<GetEditSettingsEvent>(getEditingSettingsEvent, {
    detail: target,
  }));
}

export type EditRotationEvent = number;
export function dispatchEditRotationEvent(rotation: EditRotationEvent) {
  window.dispatchEvent(new CustomEvent<EditRotationEvent>(editRotationEvent, {
    detail: rotation
  }));
}