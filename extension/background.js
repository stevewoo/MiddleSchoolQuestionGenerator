// from https://www.youtube.com/watch?v=Aw3G2jR-5IM

const server = "https://questionv2-yk4rgxamaa-ts.a.run.app/";

var clicked = false;

// toggle icon on and off
chrome.action.onClicked.addListener(function (tab) {
    clicked = !clicked;

    if(clicked){
        chrome.action.setIcon({path: "imgs/icon16_on.png", tabId:tab.id});
        chrome.scripting.executeScript({
                target: {tabId: tab.id},
                files: ['content.js'],
        });
    }
    else{
        chrome.action.setIcon({path: "imgs/icon16_off.png", tabId:tab.id});
    }
});

// listen for messages
chrome.runtime.onMessage.addListener((msg, sender, response) => {

    if(msg.name == "fetchQuestions"){

        // get url. from https://stackoverflow.com/questions/1979583/how-can-i-get-the-url-of-the-current-tab-from-a-google-chrome-extension
        chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {

            let url = tabs[0].url; // use `url` here inside the callback because it's asynchronous!
            const apiCall = server + "api/get_sentences?url=" + url;
            console.log(apiCall);

            // call api
            fetch(apiCall).then(function(res){

                if  (res.status !== 200){
                    response({question: 'Error - no question', target: "Error - no target", sentence_number: "Error - no sentence number"});
                    return;
                }
                res.json().then(function(data){

                    response(data);
                    console.log(data);
                });
            }).catch(function(err) {
                response({question: 'Error - no question', target: "Error - no target", sentence_number: "Error - no sentence number"});
            });
        });
    }
    return true;
});
