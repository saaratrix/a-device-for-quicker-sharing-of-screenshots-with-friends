export class PersistentPositionOnZoom {
  private mouseX: number;
  private mouseY: number;

  private currentWidth: number;
  private currentHeight: number;

  constructor() {
    this.mouseX = 0;
    this.mouseY = 0;

    const scrollingElement = document.scrollingElement as HTMLElement;

    this.currentWidth = scrollingElement.clientWidth;
    this.currentHeight = scrollingElement.clientHeight;

    window.addEventListener('mousemove', this.handleMouseMove);
    window.addEventListener('mouseleave', this.handleMouseLeave);
    window.addEventListener('resize', this.handleResize);
  }

  dispose(): void {
    window.removeEventListener('mousemove', this.handleMouseMove);
    window.removeEventListener('mouseleave', this.handleMouseLeave);
    window.removeEventListener('resize', this.handleResize);
  }

  private handleMouseMove = (event: MouseEvent): void => {
    this.mouseX = event.clientX;
    this.mouseY = event.clientY;
  };

  /**
   * This works because if a user wants to resize the browser they have to leave it to select a corner.
   * Which will unset the mouse positions.
   */
  private handleMouseLeave = (): void => {
    this.mouseX = -1;
    this.mouseY = -1;
  };

  private handleResize = (): void => {
    const oldWidth = this.currentWidth;
    const oldHeight = this.currentHeight;
    const scrollingElement = document.scrollingElement as HTMLElement;
    this.currentWidth = scrollingElement.clientWidth;
    this.currentHeight = scrollingElement.clientHeight;

    if (this.currentWidth === -1 || this.currentHeight === -1 || oldWidth === -1 || oldHeight === -1) {
      return;
    }
    if (this.currentWidth === oldWidth && this.currentHeight === oldHeight) {
      return;
    }
    if (this.mouseX === -1 || this.mouseY === -1) {
      return;
    }

    // To calculate how much we zoomed in %.
    // oldWidth = 1000x1000,  currentWidth = 500x500
    const zoomRatioWidth = this.currentWidth / oldWidth;
    const zoomRatioHeight = this.currentHeight / oldHeight;

    // scrollingElement.scrollLeft is always the same value when you zoom in and out.
    const deltaSizeX = this.currentWidth - oldWidth;
    const deltaSizeY = this.currentHeight - oldHeight;

    // Since no mouse event has happened we need to adjust the mouse position to the new zoom ratio
    this.mouseX *= zoomRatioWidth;
    this.mouseY *= zoomRatioHeight;

    // How much to multiply the deltas as we want to go towards cursor.
    const scrollRatioX = this.mouseX / this.currentWidth;
    const scrollRatioY = this.mouseY / this.currentHeight;

    const left = scrollingElement.scrollLeft - deltaSizeX * scrollRatioX;
    const top = scrollingElement.scrollTop - deltaSizeY * scrollRatioY;

    requestAnimationFrame(() => {
      scrollingElement.scrollTo({
        left,
        top,
      });
    });
  };
}