const question = document.getElementById("question") //DOM query to reference to the question 
const choices = Array.from(document.getElementsByClassName( 'choice-text')); //Convert the html collection to an array
const progressText = document.getElementById('progressText');
const scoreText = document.getElementById('scoreText');
const progressBarFull = document.getElementById('progressBarFull');
const loader = document.getElementById('loader');
const game = document.getElementById('game');
let currentQuestion = {};
let acceptingAnswers = false; //This is to prevent answering before the page is loaded and ready
let score = 0;
let questionCounter = 0;
let availableQuestion = [];
let questions = [];

//Fetch is used to pull from an open source api 
fetch("https://opentdb.com/api.php?amount=10&difficulty=easy&type=multiple")
    .then(res => {
        return res.json();
    })
    .then(loadedQuestions => {
        questions = loadedQuestions.results.map ( loadedQuestions => {
            const formattedQuestion = {
                question: loadedQuestions.question
            };

            const answerChoices = [... loadedQuestions.incorrect_answers]; 
            formattedQuestion.answer = Math.floor(Math.random() * 3) + 1; //Moves the answer to one of the choices (A, B, C, D) randomly
            answerChoices.splice(formattedQuestion.answer -1, 0, 
            loadedQuestions.correct_answer);

            answerChoices.forEach((choice, index) => { //Iterate through each of the answer choices created at line 25.  
                formattedQuestion["choice" + (index+1)] = choice; //Put them as choice 1-4.
            })

            return formattedQuestion;
        })
        startGame();
    })
    .catch(err => { //Anytime fetch is used catch should be used for the error scenario.
        console.log(err);
    }); 

//Constants
const CORRECT_BONUS = 10;
const MAX_QUESTIONS = 3;

startGame = () => {
    questionCounter = 0;
    score = 0;
    availableQuestions = [...questions] //Used the spread operator to copy in all of the questions from the array
    getNewQuestion();
    game.classList.remove('hidden');
    loader.classList.add('hidden');
};

getNewQuestion = () => { //Arrow syntax for more concise functions
    if(availableQuestions.length === 0 || questionCounter >= MAX_QUESTIONS){
        localStorage.setItem('mostRecentScore', score);
        //Go to end page
        return window.location.assign("end.html");
    }
    questionCounter++;
    progressText.innerText = `Question ${questionCounter}/${MAX_QUESTIONS}`;
    //Update the progress bar each time the question is updated
    progressBarFull.style.width = `${(questionCounter / MAX_QUESTIONS) * 100}%`;

    const questionIndex = Math.floor(Math.random() * availableQuestion.length); //Math.random gives a random number between 0 and 1. Multiplying by 3 gives a number between 0 and 3. Math.floor rounds down to integer*/
    currentQuestion = availableQuestions[questionIndex];
    question.innerText = currentQuestion.question;

    choices.forEach( choice => {
        const number = choice.dataset['number']; //Gets the number property from the data-set property 
        choice.innerText = currentQuestion['choice' + number]; //Out of the current question we get the choice out of it
    });
    availableQuestions.splice(questionIndex, 1); //Take the available question array and get rid of the question we just used.
    acceptingAnswers = true;
};

choices.forEach(choice => {
    choice.addEventListener('click', e => {
        if(!acceptingAnswers) return;

        acceptingAnswers = false;
        const selectedChoice = e.target;
        const selectedAnswer = selectedChoice.dataset['number'];

        const classToApply = selectedAnswer == currentQuestion.answer ? 'correct' : 'incorrect';

        if(classToApply === 'correct') {
            incrementScore(CORRECT_BONUS);
        }
        
        selectedChoice.parentElement.classList.add(classToApply);

        setTimeout( () => {
            selectedChoice.parentElement.classList.remove(classToApply);
            getNewQuestion();
        }, 500);
    });
});

incrementScore = num => {
    score += num;
    scoreText.innerText = score;
};