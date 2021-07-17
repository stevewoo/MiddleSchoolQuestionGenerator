//alert("Generating questions...");

const text = document.querySelectorAll("h1, h2, h3, h4, h5, p, b, em, i, small, strong, sub, sup, mark, span, button");

server = "http://127.0.0.1:5000/";

// from https://stackoverflow.com/questions/1979583/how-can-i-get-the-url-of-the-current-tab-from-a-google-chrome-extension
chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    let url = tabs[0].url;
    // use `url` here inside the callback because it's asynchronous!

    get_questions(url);
});

// from https://stackoverflow.com/questions/247483/http-get-request-in-javascript?rq=1
function httpGetAsync(url, callback)
{
    request = server + "api/test_sentences?" + url;

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", request, true); // true for asynchronous
    xmlHttp.send(null);
}

function callback(responseText){

    questions_json = responseText;

}


// icon from: <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
