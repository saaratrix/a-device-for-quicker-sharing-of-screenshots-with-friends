import { FileUploadedEvent, fileUploadedEvent } from "./events/file-events.js";
import { FilePreviewer } from "./file-previewer.js";
import { HistoryListHandler } from "./history-list-handler.js";
import { historyRemoveItemEvent } from "./events/history-events.js";
import { DialogHandler } from './dialog-handler.js';

export interface HistoryItem {
  date: Date;
  base64: string;
  url: string;
}

interface RawHistoryItem {
  date: string;
  base64: string;
  url: string;
}

export function canUseLocalStorage() {
  try {
    const key = 'test_localstorage';
    localStorage.setItem(key, 'muumi') ;
    localStorage.removeItem(key);
  } catch {
    return false;
  }

  return true;
}

export class HistoryHandler extends DialogHandler {

  private historyButton: HTMLSpanElement;

  private isEnabled = false;
  private readonly items: HistoryItem[] = [];
  private readonly itemsKey = 'history-items';
  private readonly maxItems = 10;

  private historyListHandler: HistoryListHandler;

  constructor(public filePreviewer: FilePreviewer) {
    const dialogElement = document.querySelector('.history-dialog') as HTMLDialogElement;
    super(dialogElement);

    this.historyListHandler = new HistoryListHandler();
    this.historyButton = document.querySelector('.history') as HTMLSpanElement;

    this.items = this.getItems();
    this.onItemsChanged();

    window.addEventListener(fileUploadedEvent, async (event) => this.onFileUploaded(event as CustomEvent<FileUploadedEvent>));
    document.querySelector('.history-items')?.addEventListener(historyRemoveItemEvent, (event) => this.onItemRemoved(event as CustomEvent<HistoryItem>));

    dialogElement.addEventListener('opened', () => this.historyListHandler.initList(this.items));
  }

  private getItems(): HistoryItem[] {
    let items: RawHistoryItem[];
      items = JSON.parse(localStorage.getItem(this.itemsKey) ?? '[]');

    return items.map(i => ({
      date: new Date(i.date),
      base64: i.base64,
      url: i.url,
    }));
  }

  private addItem(item: HistoryItem): void {
    this.items.push(item);
    this.onItemsChanged();
    this.updateLocalstorage();
  }

  private onItemRemoved(event: CustomEvent<HistoryItem>): void {
    const index = this.items.indexOf(event.detail);
    if (index === -1) {
      return;
    }

    this.items.splice(index, 1);
    this.onItemsChanged();
    this.updateLocalstorage();
  }

  private onItemsChanged(): void {
    if (this.items.length > this.maxItems) {
      this.items.shift();
    }

    const isEnabled = this.items.length > 0;
    if (this.isEnabled != isEnabled) {
      this.isEnabled = isEnabled;
      if (this.isEnabled) {
        this.enable();
      } else {
        this.disable();
      }
    }
  }

  private updateLocalstorage(): void {
    const json = JSON.stringify(this.items);
    localStorage.setItem(this.itemsKey, json);
  }

  private async onFileUploaded(event: CustomEvent<FileUploadedEvent>) {
    const thumbnail = await this.filePreviewer.getThumbnailAsBase64();
    const item: HistoryItem = {
      date: new Date(),
      url: event.detail,
      base64: thumbnail,
    };
    this.addItem(item);
  }

  private enable() {
    this.historyButton.classList.remove('history-disabled');
    this.historyButton.addEventListener('click', this.openDialog);
  }

  private disable() {
    this.historyButton.classList.add('history-disabled');
    this.historyButton.removeEventListener('click', this.openDialog);
  }
}