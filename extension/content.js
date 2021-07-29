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


    var previously_targetted = []

    for (var i = 0; i < response.questions.length; i++) {

        var question_object = response.questions[i];

        var question = question_object.question;
        var sentence_number = question_object.sentence_number;
        var target = question_object.target;//.replace(/^["'](.+(?=["']$))["']$/, '$1');

        if (previously_targetted.includes(target)){
            continue;
        }

        previously_targetted.push(target);



        console.log(question);

        var split_on_colon = question.split(":");

        var bloom_level = split_on_colon[0];
        question = split_on_colon[1];

        //value = target;

        //highlight(value);

        //value = unicodeToChar(value).replace(/\\n/g, '');
        //document.body.innerHTML = document.body.innerHTML.split(value).join('<span style="background-color: #fff799;">' + value + '</span>');

        var el = document.body; // getElementById('mytext');

        // text = el.innerHTML;

        text = document.querySelectorAll("p");

        tooltip_text = "<h3>"+ bloom_level +"</h3>" + question;

        /*
        <div class="tooltip">
            Right
            <div class="right">
                <img src="cssttp/tooltip-head.jpg" />
                <div class="text-content">
                    <h3>Fade in Effect</h3>
                    <ul>
                        <li>This demo has fade in/out effect.</li>
                        <li>It is using CSS opacity, visibility, and transition property to toggle the tooltip.</li>
                        <li>Other demos are using display property<em>(none or block)</em> for the toggle.</li>
                    </ul>
                </div>
                <i></i>
            </div>
        </div>
        */

        // tooltip_text = question;



        for (let j = 0; j < text.length; j++) {
            let tag = text[j].tagName;

            p_text = text[j].innerText;
            // console.log(p_text);

            p_text = p_text.replace(/[[0-9]+]+/g, ""); // remove wiki references
            //p_text = p_text.lower();

            // console.log(p_text); // after reference removal

            if (p_text.toLowerCase().includes(target.toLowerCase())){



                //var pattern = new RegExp(target, 'gi')
                text[j].innerHTML = text[j].innerHTML.replace(target, "<span class='tooltip'><mark>"
                + target + "</mark><span class='right'><span class='text-content'>"
                + tooltip_text + "</span><i></i></span></span>");
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



