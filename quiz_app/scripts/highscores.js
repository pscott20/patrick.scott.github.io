const highScoresList = document.getElementById('highScoresList');
const highScores = JSON.parse(localStorage.getItem('highScores')) || [];

//Map takes an incoming array (highscores) and allows me to convert each of the elements into something new in a new array.
//The function converts the score object into a string object <li>.
//highScoresList is an unordered list set to the mapped joined string. 
highScoresList.innerHTML = highScores
    .map(score => {
        return `<li class="high-score">${score.name} - ${score.score}</li>`;
    })
    .join("");