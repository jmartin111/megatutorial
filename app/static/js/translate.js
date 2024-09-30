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