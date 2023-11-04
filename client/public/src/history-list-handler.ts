// Note to self: Components would be nice instead of this. Web components maybe!
import type { HistoryItem } from "./history-handler";
import { dispatchHistoryRemoveItem } from "./events/history-events.js";
import { copyUrlToClipboard } from "./utility/copy-url-to-clipboard.js";

export class HistoryListHandler {
  private listElement: HTMLDivElement;

  private itemsMap = new Map<HistoryItem, HTMLElement>();
  private dateFormatter: Intl.DateTimeFormat

  constructor() {
    this.listElement = document.querySelector('.history-items') as HTMLDivElement;
    this.dateFormatter = new Intl.DateTimeFormat(undefined, {
      month: 'long',
      day: 'numeric',
    });
  }

  initList(items: HistoryItem[]) {
    for (const item of items) {
      this.addItem(item);
    }
  }

  public addItem(item: HistoryItem): void {
    if (this.itemsMap.has(item)) {
      return;
    }

    const element = document.createElement('div');
    const imageHTML = this.getThumbnailHTML(item.base64);
    const copyButton = document.querySelector('.link-copy-btn')!.outerHTML;
    const date = this.dateFormatter.format(item.date);
    element.className = 'history-item';
    element.innerHTML = `
      <div class="thumbnail">${imageHTML}</div>
      <div class="url"><a href="${item.url}">${item.url}</a></div>
      <div class="copy-button">${copyButton}</div>
      <div class="date">${date}</div>
      <div class="remove"><button>Remove</button></div>
    `;

    const copyButtonElement = element.querySelector('.link-copy-btn') as HTMLElement;
    copyButtonElement!.addEventListener('click', () => copyUrlToClipboard(element, '.url'));
    element.querySelector('.remove')!.addEventListener('click', () => this.removeItem(item));
    this.listElement.appendChild(element);

    this.itemsMap.set(item, element);
  }

  private getThumbnailHTML(base64: string): string {
    if (!base64) {
      return '';
    }

    return `<img src="${base64}" alt="" />`;
  }

  public removeItem(item: HistoryItem): void {
    const element = this.itemsMap.get(item);
    if (!element) {
      return;
    }

    element.parentElement?.removeChild(element);
    dispatchHistoryRemoveItem(this.listElement, item);
  }
}