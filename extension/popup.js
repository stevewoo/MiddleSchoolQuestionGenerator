// send message To Background
chrome.runtime.sendMessage({name: "fetchQuestions"}, (response) => {

  // wait for Response

  console.log(response);

  document.querySelector('.data') = response.question;
  //document.querySelector('').innerHTML = response.target;


});
