import { TransformActions } from '../editing/transform-actions.js';

export const editTransformChangedEvent = 'edit:changed'

export type EditTransformChangedEvent = keyof TransformActions;
export function dispatchTransformEvent(key: EditTransformChangedEvent) {
  // Might be good to have a safeguard so this event can't be called while updating.
  // Eg you edit something that then edits the state more which causes new events to fire.

  window.dispatchEvent(new CustomEvent<EditTransformChangedEvent>(editTransformChangedEvent, {
    detail: key as EditTransformChangedEvent,
  }));
}