async function translate(sourceElem, destElem, targetLang) {
  document.getElementById(destElem).innerHTML = `<img src=${loadingGifUrl}>`;
  const response = await fetch('/translate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json; charset=utf-8'},
    body: JSON.stringify({
      phrase: document.getElementById(sourceElem).innerText,
      target_lang: targetLang
    })
  })
  const data = await response.json();
  document.getElementById(destElem).style = 'color: green;';
  document.getElementById(destElem).innerText = data.text;
}

function initialize_popovers() {
  const popups = Document.getElementsByClassName('user-popups');
  for (let i = 0; i < popups.length; i ++) {
    const popover = new bootstrap.Popover(popups[i], {
      content: 'Loading...',
      trigger: 'hover focus',
      placement: 'right',
      html: true,
      sanitize: false,
      delay: {show: 500, hide: 0},
      container: popups[i],
      customClass: 'd-inline',
    });
  }
}
document.addEventListener('DOMContentLoaded', initialize_popovers);