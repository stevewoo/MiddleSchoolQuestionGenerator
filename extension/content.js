// from https://github.com/btahir/summarlight/blob/master/extension_bundle/content.js
alert("Generating questions...");

function unicodeToChar(text) {
	return text.replace(/\\u[\dA-F]{4}/gi,
	      function (match) {
	           return String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16));
	      });
}

// send message To Background
chrome.runtime.sendMessage({name: "fetchQuestions"}, (response) => {

  // wait for Response

    console.log("Response in content.js");
    console.log(response);

//  document.querySelector('h1').innerHTML = response.question;
//  document.querySelector('h2').innerHTML = response.target;
//  document.querySelector('strong').innerHTML = response.sentence_number;

    // for each value

    value = "Kiwi"

    value = unicodeToChar(value).replace(/\\n/g, '');
    document.body.innerHTML = document.body.innerHTML.split(value).join('<span style="background-color: #fff799;">' + value + '</span>');





});



