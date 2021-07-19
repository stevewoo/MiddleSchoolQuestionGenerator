// from https://github.com/btahir/summarlight/blob/master/extension_bundle/content.js
//alert("Generating questions...");


// send message To Background
chrome.runtime.sendMessage({name: "fetchQuestions"}, (response) => {

  // wait for Response

    console.log("Response in content.js");
    console.log(response);

//  document.querySelector('h1').innerHTML = response.question;
//  document.querySelector('h2').innerHTML = response.target;
//  document.querySelector('strong').innerHTML = response.sentence_number;

    // for each value

    for (var i = 0; i < response.questions.length; i++) {

        var question_object = response.questions[i];

        var question = question_object.question;
        var sentence_number = question_object.sentence_number;
        var target = question_object.target.replace(/['"]+/g, ''));;

        console.log(question);

        //value = target;

        //highlight(value);

        //value = unicodeToChar(value).replace(/\\n/g, '');
        //document.body.innerHTML = document.body.innerHTML.split(value).join('<span style="background-color: #fff799;">' + value + '</span>');

        var el = document.body; // getElementById('mytext');

        // text = el.innerHTML;

        text = document.querySelectorAll("p");

        for (let j = 0; j < text.length; j++) {
            let tag = text[j].tagName;
            if (text[j].innerHTML.match(target) && !(tag == "BUTTON" || tag == "SPAN")){
                text[j].innerHTML = text[j].innerHTML.replace(new RegExp(target, 'g'),"<mark>"+target+"</mark>");
            }

        }


        //console.log(el.innerText);

        //keyword = value; //document.getElementById('input').value;

        //marked = text.replace(new RegExp(keyword, 'g'),"<mark>"+keyword+"</mark>");

        //el.innerHTML = marked;


    }


});



