import React, {Component} from 'react';
import {QuizData} from './QuizData.js';
import "bootstrap/dist/css/bootstrap.css";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Image from "react-bootstrap/Image";

class Quiz extends Component {

    constructor(props) {
        super(props);
        this.state = {
            userAnswer: null,
            currentIndex: 0,
            options: [],
            quizEnd: false,
            score: 0,
            disabled: false,
        };
    }

    loadQuiz = () => {
        const {currentIndex} = this.state;
        this.setState(() => {
            return {
                question: QuizData[currentIndex].question,
                options: QuizData[currentIndex].options,
                answer: QuizData[currentIndex].answer,
            };
        });
    };

    nextQuestionHandler = () => {
        const {userAnswer, realAnswer, score} = this.state;

        if (userAnswer === realAnswer) {
            this.setState({
                score: this.state.score + 1,
            });
        }

        this.setState({
            currentIndex: this.state.currentIndex + 1,
            userAnswer: null,
        });
    };

    prevQuestionHandler = () => {
        const {userAnswer, realAnswer, score} = this.state;

        if (userAnswer === realAnswer) {
            this.setState({
                score: this.state.score + 1,
            });
        }

        this.setState({
            currentIndex: this.state.currentIndex - 1,
            userAnswer: null,
        });
    };

    componentDidMount() {
        this.loadQuiz();
    }

    checkAnswer = answer => {
        this.setState({
            userAnswer: answer,
            disabled: false,
        });
    };

    finishHandler = () => {
        if (this.state.currentIndex === QuizData.length - 1) {
            this.setState({
                quizEnd: true,
            });
        }
    };

    componentDidUpdate(prevProps, prevState) {
        const {currentIndex} = this.state;
        if (this.state.currentIndex != [prevState.currentIndex]) {
            this.setState(() => {
                return {
                    disabled: true,
                    question: QuizData[currentIndex].question,
                    options: QuizData[currentIndex].options,
                    answer: QuizData[currentIndex].answer,
                };
            });
        }
    }

    render() {
        return (
            <Container>
                <Row xm={3} sm={3} className="align-items-center">
                    <Col xs={2} sm={2}>
                        {this.renderTechnionImage()}
                    </Col>
                    <Col className="d-flex justify-content-center">
                        {this.renderQuestions()}
                    </Col>
                    <Col>
                        {this.renderNaoPicture()}
                    </Col>
                </Row>
                <Row className="mt-5">
                    <Col xs={10} sm={10}>
                        {this.renderFooter()}
                    </Col>
                </Row>
            </Container>
        );
    }

    renderTechnionImage() {
        const technion_img = require('./images/technion.png').default;
        return (
            <Image src={technion_img} alt="technion_img" fluid/>
        );
    }

    renderQuestions() {
        const {question, options, currentIndex, userAnswer, quizEnd} = this.state;
        if (quizEnd) {
            return (
                <div>
                    <h1>Good job!</h1>
                    <p>The correct answers were: Fruit, פרי, 水果</p>
                </div>
            );
        }

        return (
            <div>
                <h2>{question}</h2>
                <span>{`Question ${currentIndex + 1} of ${QuizData.length}\n`}</span> {
                options.map(option =>
                    <Form.Check
                        type="radio"
                        id={option}
                        label={option}
                        name="radioAnswer"
                        onClick={() => this.checkAnswer(option)}
                    />,
                )
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
                <p>
                    <button onClick={() => alert('Here have some help')}>{'HELP!'}</button>
                </p>
            </div>
        );
    }

    renderNaoPicture() {
        const nao_img = require('./images/nao_picture.png').default;
        return (
            <Image src={nao_img} alt="nao_img" fluid/>
        );
    }

    renderFooter() {
        const mindful_lab_img = require('./images/mindful_lab.png').default;
        return (
            <Image src={mindful_lab_img} alt="mindful_lab_img" fluid/>
        );
    }
}

export default Quiz;
