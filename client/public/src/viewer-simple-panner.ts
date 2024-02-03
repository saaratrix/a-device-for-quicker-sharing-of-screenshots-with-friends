export class ViewerSimplePanner {
  private isPanning: boolean = false;
  private currentX: number = -1;
  private currentY: number = -1;

  private hasMoved: boolean = false;
  private hasMovedAmount: number = 0;
  private readonly moveThreshold: number = 15;

  constructor() {
    this.handleMouseDown = this.handleMouseDown.bind(this);
    this.handleMouseUp = this.handleMouseUp.bind(this);
    this.handleMouseLeave = this.handleMouseLeave.bind(this);
    this.handleMouseMove = this.handleMouseMove.bind(this);
    this.handleClick = this.handleClick.bind(this);

    window.addEventListener('mousedown', this.handleMouseDown);
    window.addEventListener('mouseup', this.handleMouseUp);
    window.addEventListener('mouseleave', this.handleMouseLeave);
    window.addEventListener('mousemove', this.handleMouseMove);
    window.addEventListener('click', this.handleClick, true);

    this.isPanning = false;
    this.currentX = 0;
    this.currentY = 0;
  }

  handleMouseDown(event: MouseEvent): void {
    // 0 = left mouse button
    // 1 = middle mouse button
    if (event.button !== 0 && event.button !== 1) {
      return;
    }

    this.isPanning = true;
    this.hasMoved = false;
    this.hasMovedAmount = 0;
    this.currentX = event.clientX;
    this.currentY = event.clientY;
    // This prevents the middle mouse button scroll toggle.
    // Also needed for mouseUp.
    if (event.button === 1) {
      event.preventDefault();
    }
  }

  handleMouseUp(event: MouseEvent): void {
    if (!this.isPanning) {
      return;
    }

    // Using set timeout so we let click() process too as we might want to cancel the click event.
    setTimeout(() => {
      this.isPanning = false;
    }, 0);

    // Middle mouse button
    if (event.button === 1) {
      event.preventDefault();
    }
  }

  handleClick(event: PointerEvent): void {
    if (!this.isPanning || !this.hasMoved) {
      return;
    }

    const target = event.target as HTMLElement;
    // So we don't do this if we click on video buttons etc.  
    if (target?.matches('video')) {
      event.preventDefault();
    }
  }

  handleMouseLeave(event: MouseEvent): void {
    this.isPanning = false;
  }

  handleMouseMove(event: MouseEvent): void {
    if (!this.isPanning) {
      return;
    }

    const dx = event.clientX - this.currentX;
    const dy = event.clientY - this.currentY;

    if (!this.hasMoved) {
      this.hasMovedAmount += Math.abs(dx) + Math.abs(dy);
      if (this.hasMovedAmount > this.moveThreshold) {
        this.hasMoved = true;
      }
    }

    this.currentX = event.clientX;
    this.currentY = event.clientY;
    document.scrollingElement?.scrollTo({
      left: window.scrollX - dx,
      top: window.scrollY - dy,
    });
  }

  dispose(): void {
    // Remove event listeners
    window.removeEventListener('mousedown', this.handleMouseDown);
    window.removeEventListener('mouseup', this.handleMouseUp);
    window.removeEventListener('mouseleave', this.handleMouseLeave);
    window.removeEventListener('mousemove', this.handleMouseMove);
    window.removeEventListener('click', this.handleClick);
  }
}