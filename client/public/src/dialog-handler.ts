export class DialogHandler {
  protected backdropElement: HTMLDivElement;
  protected dialogElement: HTMLDialogElement;

  constructor(dialogElement: HTMLDialogElement) {
    this.backdropElement = document.querySelector('.dialog-backdrop') as HTMLDivElement;
    this.dialogElement = dialogElement;

    this.backdropElement.addEventListener('click', () => this.closeDialog());
  }

  openDialog = () => {
    this.backdropElement.classList.add('open');
    this.dialogElement.open = true;
    this.dialogElement.dispatchEvent(new CustomEvent('opened'));
  }

  closeDialog() {
    if (!this.dialogElement.open) {
      return;
    }

    this.backdropElement.classList.remove('open');
    this.dialogElement.open = false;
  }
}