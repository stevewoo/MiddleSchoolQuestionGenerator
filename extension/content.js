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

//    var el = document.body;
//    text = document.querySelectorAll("p");
//    console.log(text);

//    for (let k = 0; k < text.length; k++) {
//
//            console.log(k + text[k]);
//    }


    for (var i = 0; i < response.questions.length; i++) {

        var question_object = response.questions[i];

        var question = question_object.question;
        var sentence_number = question_object.sentence_number;
        var target = question_object.target;//.replace(/^["'](.+(?=["']$))["']$/, '$1');

        console.log(question);

        //value = target;

        //highlight(value);

        //value = unicodeToChar(value).replace(/\\n/g, '');
        //document.body.innerHTML = document.body.innerHTML.split(value).join('<span style="background-color: #fff799;">' + value + '</span>');

        var el = document.body; // getElementById('mytext');

        // text = el.innerHTML;

        text = document.querySelectorAll("p");



        tooltip_text = question;

        for (let j = 0; j < text.length; j++) {
            let tag = text[j].tagName;

            p_text = text[j].innerText;
            // console.log(p_text);

            p_text = p_text.replace(/[[0-9]+]+/g, "");

            // console.log(p_text); // after reference removal

            if (text[j].innerText.includes(target)){



                //var pattern = new RegExp(target, 'gi')
                text[j].innerHTML = text[j].innerHTML.replace(target, "<mark><div class='tooltip'>"
                + target + "<span class='tooltiptext'>"
                + tooltip_text + "</span></div></mark>");
            }


            // working ok for small phrases
//            if (text[j].innerHTML.match(target) && !(tag == "BUTTON" || tag == "SPAN")){
//                text[j].innerHTML = text[j].innerHTML.replace(new RegExp(target, 'g'),"<mark><div class=\"tooltip\">"+target+"<span class=\"tooltiptext\">" + tooltip_text + "</span></div></mark>");
//            }

        }

        /*

        <div class="tooltip">Hover over me
            <span class="tooltiptext">Tooltip text</span>
         </div>

        */


        //console.log(el.innerText);

        //keyword = value; //document.getElementById('input').value;

        //marked = text.replace(new RegExp(keyword, 'g'),"<mark>"+keyword+"</mark>");

        //el.innerHTML = marked;


    }


});



