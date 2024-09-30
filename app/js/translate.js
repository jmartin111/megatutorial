async function translate(sourceElem, destElem, sourceLang, targetLang) {
    document.getElementById(destElem).innerHTML =
      '<img src="{{ url_for('static', filename='loading.gif') }}">';
    const response = await fetch('/translate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json; charset=utf-8'},
      body: JSON.stringify({
        phrase: document.getElementById(sourceElem).innerText,
        source_lang: sourceLang,
        target_lang: destLang
      })
    })
    const data = await response.json();
    document.getElementById(destElem).innerText = data.text;
  }