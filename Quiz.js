import React, { Component } from 'react'
import {QuizData} from './QuizData.js'
import styles from './styles.css'

export class Quiz extends Component {
    constructor(props) {
        super(props)
        this.state = {
            userAnswer: null,
            currentIndex: 0,
            options: [],
            quizEnd: false,
            score: 0,
            disabled: false
        }
    }

loadQuiz = () => {
    const {currentIndex} = this.state;
    this.setState(() => {
        return {
            question: QuizData[currentIndex].question,
            options: QuizData[currentIndex].options,
            answer: QuizData[currentIndex].answer
        }
    })
}

nextQuestionHandler = () => {
    const {userAnswer, realAnswer, score} = this.state

    if(userAnswer === realAnswer) {
        this.setState({
            score: this.state.score + 1
        })
    }

    this.setState({
        currentIndex: this.state.currentIndex + 1,
        userAnswer: null
    })
}

prevQuestionHandler = () => {
    const {userAnswer, realAnswer, score} = this.state

    if(userAnswer === realAnswer) {
        this.setState({
            score: this.state.score + 1
        })
    }

    this.setState({
        currentIndex: this.state.currentIndex - 1,
        userAnswer: null
    })
}

componentDidMount() {
    this.loadQuiz();
}

checkAnswer = answer => {
    this.setState({
        userAnswer: answer,
        disabled: false
    })
}

finishHandler = () => {
    if(this.state.currentIndex === QuizData.length - 1) {
        this.setState({
            quizEnd: true
        })
    }
}

componentDidUpdate(prevProps, prevState) {
    const {currentIndex} = this.state;
    if(this.state.currentIndex != [prevState.currentIndex]) {
        this.setState(() => {
            return {
                disabled: true,
                question: QuizData[currentIndex].question,
                options: QuizData[currentIndex].options,
                answer: QuizData[currentIndex].answer
            }
        });
    }

}

    render() {
        const {question, options, currentIndex, userAnswer, quizEnd} = this.state
        if (quizEnd) {
            return (
                <div>
                    <h1>Good job!</h1>
                    <p>The correct answers were: Fruit, פרי, 水果</p>
                </div>
            )
        }
        return(
            <div>
                <h2>{question}</h2>
                <span>{`Question ${currentIndex + 1} of ${QuizData.length}\n`}</span> {
                    options.map(option => <p 
                        key = {option.id} 
                        className={`options ${userAnswer === option? "selected" : null}`}
                        onClick = {() => this.checkAnswer(option)}>
                            {option}
                    </p>)
                }
                {currentIndex > 0 &&
                <button onClick={this.prevQuestionHandler}>
                    Previous Question
                    </button>}
                {currentIndex < QuizData.length - 1 &&
                <button disabled={this.state.disabled} onClick={this.nextQuestionHandler}>
                    Next Question
                    </button>}
                {currentIndex === QuizData.length - 1 &&
                <button onClick={this.finishHandler} disabled={this.state.disabled}>
                    Finish
                    </button>}
                <p><button onClick={() => alert('Here have some help')}>{'HELP!'}</button></p>
            </div>
        )
    }
}
export default Quiz