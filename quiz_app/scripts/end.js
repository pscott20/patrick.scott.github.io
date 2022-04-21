const username = document.getElementById('username');
const saveScoreBtn = document.getElementById('saveScoreBtn');
const finalScore = document.getElementById('finalScore');
const mostRecentScore = localStorage.getItem('mostRecentScore');

//Local Storage only stores key-value pairs with the value being strings. In order to work with arrays we need to convert them into JSON strings first.
const highScores = JSON.parse(localStorage.getItem('highScores')) || []; //Converts the JSON string into an object or returns an empty array

const MAX_HIGH_SCORES = 5; 
finalScore.innerText = mostRecentScore; 

username.addEventListener("keyup", () => {
    saveScoreBtn.disabled = !username.value; //Set the save button to disabled if the username input is falsey
});

saveHighScore = (e) => {
    e.preventDefault(); //This prevents the form from submitting to a new page with the form properties as query parameters.

    const score = {
        score: Math.floor(Math.random() * 100),
        name: username.value
    };
    highScores.push(score);

    highScores.sort( (a,b) => b.score - a.score) //If b score is higher than a score then place b before a in array. The return is implicit.
    
    highScores.splice(5);

    localStorage.setItem('highScores', JSON.stringify(highScores));
    window.location.assign("/");
};

