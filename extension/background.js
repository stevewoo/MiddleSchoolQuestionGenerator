// from https://www.youtube.com/watch?v=Aw3G2jR-5IM

const server = "http://127.0.0.1:5000/";

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

//                   result = JSON.parse(data)
//                    console.log(result);

                    response({question: data.question, target: data.target, sentence_number: data.sentence_number});
                });
            }).catch(function(err) {
                response({question: 'Error - no question', target: "Error - no target", sentence_number: "Error - no sentence number"});
            });

        });

    }

    return true;

});

//
//    const questions = [
//      "A kind of Japanese woodblock print, privately commissioned for special occasions such as the New Year.",
//      "In <em>fencing</em>, the ninth and last thrust, usually aimed at the side.",
//      "The point in a solar orbit where the orbiting body is closest to the sun.",
//      "A typewriter used to emboss paper with braille cells to be read by the visually impaired instead of using a manual stylus.",
//      "A fire produced by the friction of one piece of wood upon another, or of a rope upon a stake of wood."
//    ];
//
//    const targets = [
//      "surimono",
//      "flanconade",
//      "perihelion",
//      "brailler",
//      "needfire"
//    ];
//
//    const sentenceNumbers = [
//        5,
//        3,
//        5,
//        23,
//        1
//    ]
//
//    var number = 3
//
//    // send response
//    response({question: questions[number], target: targets[number], senNum: sentenceNumbers[number]});
//
//  }
//
//});
