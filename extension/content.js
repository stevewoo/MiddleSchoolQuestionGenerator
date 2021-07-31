// from https://github.com/btahir/summarlight/blob/master/extension_bundle/content.js

// send message To background.js
chrome.runtime.sendMessage({name: "fetchQuestions"}, (response) => {

  // wait for Response
    console.log("Response in content.js");
    console.log(response);

    var previously_targetted = []

    for (var i = 0; i < response.questions.length; i++) {

        var question_object = response.questions[i];

        var question = question_object.question;
        var sentence_number = question_object.sentence_number;
        var target = question_object.target;//.replace(/^["'](.+(?=["']$))["']$/, '$1');

        // try not to double up in the same area
        if (previously_targetted.includes(target)){
            continue;
        }

        previously_targetted.push(target);

        console.log(question);

        var split_on_colon = question.split(":");

        // get the bloom level and question out
        var bloom_level = split_on_colon[0];
        question = split_on_colon[1];

        var el = document.body; // getElementById('mytext');
        text = document.querySelectorAll("section, p, article"); // tags with the main text
        tooltip_text = "<div><strong>"+ bloom_level +"</strong></div>" + question;

        for (let j = 0; j < text.length; j++) {

            let tag = text[j].tagName;
            p_text = text[j].innerText;
            p_text = p_text.replace(/[[0-9]+]+/g, ""); // remove wiki references
            // console.log(p_text); // after reference removal

            if (p_text.toLowerCase().includes(target.toLowerCase())){

                // add the question as a tooltip
                text[j].innerHTML = text[j].innerHTML.replace(target, "<span class='tooltip'><mark>"
                + target + "</mark><span class='right'><span class='text-content'>"
                + tooltip_text + "</span><i></i></span></span>");


            }

        }
    }
});



