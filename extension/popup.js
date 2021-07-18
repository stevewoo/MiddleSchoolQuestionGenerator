// send message To Background
chrome.runtime.sendMessage({name: "fetchQuestions"}, (response) => {

  // wait for Response

  console.log(response);

  document.querySelector('h1').innerHTML = response.question;
  document.querySelector('h2').innerHTML = response.target;
  document.querySelector('strong').innerHTML = response.sentence_number;

  chrome.tabs.executeScript(null, { file: "content.js" });


});
