import type { HistoryItem } from "../history-handler";

export const historyRemoveItemEvent = 'history:remove-item';

export function dispatchHistoryRemoveItem(element: HTMLElement, item: HistoryItem): void {
  element.dispatchEvent(new CustomEvent<HistoryItem>(historyRemoveItemEvent, {
    detail: item,
  }));
}