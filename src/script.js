document.addEventListener('DOMContentLoaded', _ => {
  document.onmouseup = _ => {
    if (window.getSelection) {
      fuzzyWrapText(window.getSelection())
    }
  }

});

const fuzzyWrapText = sel => {
  const selectedText = getSelectionText(sel)
  const fuzzyWrap = document.createElement('span')
  const range = sel.getRangeAt(0).cloneRange()

  fuzzyWrap.classList.add('glitch')
  fuzzyWrap.setAttribute('data-text', selectedText)

  range.surroundContents(fuzzyWrap)
  sel.removeAllRanges()
  sel.addRange(range)
  
}

const getSelectionText = sel => document.selection && document.selection.type != "Control" ? document.selection.createRange().text : sel.toString();