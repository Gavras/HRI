import React, {Component} from 'react';
import {QuizData} from './QuizData.js';
import "bootstrap/dist/css/bootstrap.css";
import Alert from "react-bootstrap/Alert";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Image from "react-bootstrap/Image";
import Form from 'react-bootstrap/Form';
import Card from "react-bootstrap/Card";
import "./index.css";
import Button from "react-bootstrap/Button";

class Quiz extends Component {

    constructor(props) {
        super(props);
        this.state = {
            userAnswer: null,
            currentIndex: 0,
            question: QuizData[0].question,
            options: QuizData[0].options,
            answer: QuizData[0].answer,
            quizEnd: false,
            score: 0,
            disabled: false,
            started: false
        };
    }

    render() {
        return (
            <Card bg="light" className="vh-100">
                <Card.Body bg="light" className="h-100">
                    <Container className="h-100">
                        {this.renderMainContent()}
                        {this.renderFooter()}
                    </Container>
                </Card.Body>
            </Card>
        );
    }

    renderMainContent() {
        const column = this.state.started ? this.renderQuizContent() : this.renderLandingPage();
        return (
            <Row className="h-90 align-items-center justify-content-center">
                {column}
            </Row>
        );
    }

    renderLandingPage() {
        return (
            <Col xs={6} sm={6} className="h-fc w-fc">
                {this.renderStartButton()}
            </Col>
        );
    }

    renderQuizContent() {
        return (
            <>
                <Col xs={{offset:3}} ms={{offset:3}} className="h-fc">
                    {this.renderQuestion()}
                </Col>
                <Col className="h-fc">
                    {this.renderNao()}
                </Col>
            </>
        );
    }

    renderQuestion() {
        if (this.state.quizEnd) {
            return (
                <Alert variant="success">
                    Good job!
                </Alert>
            );
        }

        return (
            <Card bg="light" className="h-100 w-questions-card">
                <Card.Header>
                    {this.state.question}
                </Card.Header>
                <Card.Body>
                    <Form>
                        {this.renderAnswerOptions()}
                        {this.renderActionButtons()}
                    </Form>
                </Card.Body>
            </Card>
        );
    }

    renderAnswerOptions() {
        return this.state.options.map(option =>
            <Form.Check
                type="radio"
                id={option}
                label={option}
                name="radioAnswerOption"
                onClick={() => this.onAnswerOptionClick(option)}
            />,
        );
    }

    renderActionButtons() {
        const {currentIndex} = this.state;

        const prevButton = currentIndex > 0 ?
            <Button onClick={this.OnPrevButtonClick}>
                Previous Question
            </Button> : null;

        const nextButton = currentIndex < QuizData.length - 1 ?
            <Button disabled={this.state.disabled} onClick={this.OnNextButtonClick}>
                Next Question
            </Button> : null;

        const finishButton = currentIndex === QuizData.length - 1 ?
            <Button onClick={this.onFinishButtonClick} disabled={this.state.disabled}>
                Finish
            </Button> : null;

        const askNaoButton =
            <Button
                variant="info" className="mt-2"
                onClick={this.onAskNaoButtonClick}
            >
                {'Ask Nao'}
            </Button>;

        return (
            <div className="mt-2">
                {prevButton}
                {nextButton}
                {finishButton}
                <br/>
                {askNaoButton}
            </div>
        );
    }

    renderNao() {
        const nao_img = require('./images/nao_picture.png').default;
        return (
            <Image src={nao_img} alt="nao_img" fluid className="h-100 max-vh-50"/>
        );
    }

    renderStartButton() {
        const start_button_img = require('./images/start_picture.png').default;
        return (
            <Image src={start_button_img} alt="start_button_img" fluid className="h-100 max-vh-50"
                   onClick={() => this.onStartButtonClick()}/>
        );
    }

    renderFooter() {
        return (
            <Row className="h-10">
                <Col xs={2} sm={2} className="h-100">
                    {this.renderTechnionImage()}
                </Col>
                <Col className="h-100">
                    {this.renderMindfulLabImage()}
                </Col>
            </Row>
        );
    }

    renderTechnionImage() {
        const technion_img = require('./images/technion.png').default;
        return (
            <Image src={technion_img} alt="technion_img" fluid className="h-100"/>
        );
    }

    renderMindfulLabImage() {
        const mindful_lab_img = require('./images/mindful_lab.png').default;
        return (
            <Image src={mindful_lab_img} alt="mindful_lab_img" fluid className="h-100"/>
        );
    }

    onAnswerOptionClick = answer => {
        this.setState({
            userAnswer: answer,
            disabled: false,
        });
    };

    OnPrevButtonClick = () => {
        const {userAnswer, realAnswer} = this.state;

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

    OnNextButtonClick = () => {
        const {userAnswer, realAnswer} = this.state;

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

    onFinishButtonClick = () => {
        if (this.state.currentIndex === QuizData.length - 1) {
            this.setState({
                quizEnd: true,
            });
        }
    };

    onAskNaoButtonClick = () => {
        alert("apples grow on trees");
    };

    onStartButtonClick = () => {
        this.setState({
            started: true,
        });
    };
}

export default Quiz;
