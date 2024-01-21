export function copyUrlToClipboard(element: HTMLElement, textClass: '.link-text' | '.url') {
  const linkTextElement = element.querySelector<HTMLSpanElement>(textClass) as HTMLSpanElement;
  const text = linkTextElement.innerHTML;

  if (!text) {
    return;
  }
  navigator.clipboard.writeText(text).then();
}