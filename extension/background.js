// from https://www.youtube.com/watch?v=Aw3G2jR-5IM

// listen for messages
chrome.runtime.onMessage.addListener((msg, sender, response) => {

  if(msg.name == "fetchQuestions"){


    //const apiKey = 'OUR-API-KEY';
    //const dateStr = new Date().toISOString().slice(0, 10); //2020-01-01
    //const apiCall = 'https://api.wordnik.com/v4/words.json/wordOfTheDay?date='+dateStr+'&api_key='+apiKey;
    //We call api..
    //wait for response..
    //send the response...

    //fetch(..).await...


    const questions = [
      "A kind of Japanese woodblock print, privately commissioned for special occasions such as the New Year.",
      "In <em>fencing</em>, the ninth and last thrust, usually aimed at the side.",
      "The point in a solar orbit where the orbiting body is closest to the sun.",
      "A typewriter used to emboss paper with braille cells to be read by the visually impaired instead of using a manual stylus.",
      "A fire produced by the friction of one piece of wood upon another, or of a rope upon a stake of wood."
    ];

    const targets = [
      "surimono",
      "flanconade",
      "perihelion",
      "brailler",
      "needfire"
    ];

    const sentenceNumbers = [
        5,
        3,
        5,
        23,
        1
    ]

    var number = 3

    //Send response
    response({question: questions[number], target: targets[number], senNum: sentenceNumbers[number]});

  }

});
