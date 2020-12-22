import React, {Component} from 'react';
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

const Phase = Object.freeze({
    "started": 1,
    "quiz": 2,
    "ended": 3,
});

class Quiz extends Component {

    BACKEND_URL = 'http://localhost:8002/';

    constructor(props) {
        super(props);
        this.state = {
            question: null,
            userAnswer: null,
            serverSubmitAnswer: null,
            hint: null,
            phase: Phase.started,
        };
    }

    getQuestion(first = false) {
        const xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function () {
            if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
                for (const [ref, object] of Object.entries(this.refs)) {
                    if (ref.startsWith('radioAnswerOption')) {
                        object.checked = false;
                    }
                }
                const question = JSON.parse(xmlHttp.responseText);
                let phase = Phase.quiz;
                if (question.question === "No More Questions!") {
                    phase = Phase.ended;
                }
                this.setState({
                    question: question,
                    userAnswer: null,
                    serverSubmitAnswer: null,
                    hint: null,
                    phase: phase,
                });
            }
        }.bind(this);
        const url_suffix = first ? '?idx=0' : '';
        const url = this.BACKEND_URL + 'get_question' + url_suffix;
        xmlHttp.open('GET', url, true);
        xmlHttp.send(null);
    }

    getServerSubmitAnswer() {
        const xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function () {
            if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
                this.setState({
                    serverSubmitAnswer: JSON.parse(xmlHttp.responseText),
                });
            }
        }.bind(this);
        const url = this.BACKEND_URL + 'submit_answer?answer=' + this.state.userAnswer;
        xmlHttp.open('GET', url, true);
        xmlHttp.send(null);
    }

    getHint() {
        const xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function () {
            if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
                this.setState({
                    hint: xmlHttp.responseText,
                });
            }
        }.bind(this);
        xmlHttp.open('GET', this.BACKEND_URL + 'get_hint', true);
        xmlHttp.send(null);
    }

    render() {
        return (
            <Card bg="light" className="vh-100 vw-100 justify-content-center">
                <Card.Body bg="light" className="h-100 w-100 justify-content-center">
                    <Container className="h-100 w-100 justify-content-center">
                        {this.renderMainContent()}
                        {this.renderFooter()}
                    </Container>
                </Card.Body>
            </Card>
        );
    }

    renderMainContent() {
        let column = null;
        switch (this.state.phase) {
            case Phase.started:
                column = this.renderLandingPage();
                break;
            case Phase.quiz:
                column = this.renderQuizContent();
                break;
            case Phase.ended:
                column = this.renderQuizContent();
                break;
        }

        return (
            <Row className="h-90 w-100 m-auto align-items-center justify-content-center">
                {column}
            </Row>
        );
    }

    renderLandingPage() {
        return (
            <Col className="h-100 w-100 justify-content-center">
                <Container className="h-100 w-100 justify-content-center">
                    <Row className="h-80 w-100 m-auto justify-content-center">
                        <Col className="h-100 w-100 d-flex justify-content-center">
                            {this.renderStartQuizGif()}
                        </Col>
                    </Row>
                    <Row className="h-20 mt-1 justify-content-center align-items-center">
                        <Col className="d-flex justify-content-center">
                            {this.renderStartButton()}
                        </Col>
                    </Row>
                </Container>
            </Col>
        );
    }

    renderStartQuizGif() {
        const start_gif = require('./media/gifs/start_quiz.gif').default;
        return (
            <Image src={start_gif} alt="start_gif" fluid className="h-100"/>
        );
    }

    renderStartButton() {
        return (
            <Button className=""
                    variant="success"
                    onClick={() => this.onStartButtonClick()}>
                Start Quiz
            </Button>
        );
    }

    renderQuizContent() {
        return (
            <>
                <Col className="h-fc">
                    {this.renderQuestion()}
                </Col>
                <Col className="h-fc">
                    {this.renderNao()}
                </Col>
            </>
        );
    }

    renderQuestion() {
        if (this.state.question == null) {
            return null;
        }

        return (
            <Card bg="light" className="h-100 w-questions-card">
                <Card.Header>
                    {this.state.question.question}
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
        return this.state.question.possible_answers.map((option, i) =>
            <Form.Check
                type="radio"
                id={option}
                ref={'radioAnswerOption' + i}
                label={option}
                name="radioAnswerOption"
                onClick={() => this.onAnswerOptionClick(i)}
            />,
        );
    }

    renderActionButtons() {
        switch (this.state.phase) {
            case Phase.quiz:
                return this.renderQuizPhaseActionButtons();
            case  Phase.ended:
                return this.renderEndedPhaseActionButtons();
            default:
                return null;
        }
    }

    renderQuizPhaseActionButtons() {
        return (
            <div className="mt-2">
                {this.renderSubmitButton()}
                {this.renderNextButton()}
                {this.renderSubmitResponse()}
                <br/>
                {this.renderAskNaoButton()}
                {this.renderHintResponse()}
            </div>
        );
    }

    renderSubmitButton() {
        if (this.isCorrectAnswer()) {
            return null;
        } else {
            return <Button onClick={this.onSubmitButtonClick}>
                Submit
            </Button>;
        }
    }

    renderNextButton() {
        if (this.isCorrectAnswer()) {
            return <Button
                onClick={this.onNextButtonClick}
                className="ml-1">
                Next Question
            </Button>;
        } else {
            return null;
        }
    }

    renderAskNaoButton() {
        return <Button
            variant="info" className="mt-2"
            onClick={this.onAskNaoButtonClick}>
            Ask Nao
        </Button>;
    }

    renderEndedPhaseActionButtons() {
        return (
            <Alert variant="success">
                Good Job!
            </Alert>
        );
    }

    renderSubmitResponse() {
        if (this.state.serverSubmitAnswer == null) {
            return null;
        }

        const variant = this.isCorrectAnswer() ? "success" : "danger";

        return (
            <Alert variant={variant} className="m-0 mt-1">
                {this.state.serverSubmitAnswer.response}
            </Alert>
        );
    }

    renderHintResponse() {
        if (this.state.hint == null) {
            return null;
        }

        return (
            <Alert variant="success" className="m-0 mt-1">
                {this.state.hint}
            </Alert>
        );
    }

    renderNao() {
        let nao_img;
        switch (this.state.phase) {
            case Phase.started:
                nao_img = require('./media/images/nao_picture.png');
                break;
            case Phase.quiz:
                if (this.state.serverSubmitAnswer == null) {
                    nao_img = require('./media/images/nao_picture.png');
                } else {
                    if (this.isCorrectAnswer()) {
                        nao_img = require('./media/gifs/correct_answer.gif');
                    } else {
                        nao_img = require('./media/gifs/incorrect_answer.gif');
                    }
                }
                break;
            case Phase.ended:
                // Need to get ending gif
                nao_img = require('./media/gifs/end_quiz.gif');
                break;
            default:
                nao_img = require('./media/images/nao_picture.png');
                break;
        }
        return (
            <Image src={nao_img.default} alt="nao_img" fluid className="h-100 max-vh-50"/>
        );
    }

    renderFooter() {
        return (
            <Row className="h-10 w-100 m-auto justify-content-center">
                <Col xs={2} sm={2} className="h-100">
                    {this.renderTechnionImage()}
                </Col>
                <Col xs={8} sm={8} className="h-100">
                    {this.renderMindfulLabImage()}
                </Col>
            </Row>
        );
    }

    renderTechnionImage() {
        const technion_img = require('./media/images/technion.png').default;
        return (
            <Image src={technion_img} alt="technion_img" fluid className="h-100"/>
        );
    }

    renderMindfulLabImage() {
        const mindful_lab_img = require('./media/images/mindful_lab.png').default;
        return (
            <Image src={mindful_lab_img} alt="mindful_lab_img" className="h-100 w-100"/>
        );
    }

    isCorrectAnswer() {
        return this.state.serverSubmitAnswer &&
            this.state.serverSubmitAnswer.answer === "correct";
    }

    onAnswerOptionClick = answer => {
        if (this.isCorrectAnswer()) {
            for (const [ref, object] of Object.entries(this.refs)) {
                if (ref.startsWith('radioAnswerOption')) {
                    object.checked = ref === 'radioAnswerOption' + this.state.userAnswer;
                }
            }
            return;
        }
        this.setState({
            userAnswer: answer,
        });
    };

    onSubmitButtonClick = () => {
        if (this.state.userAnswer == null) {
            this.setState({
                serverSubmitAnswer: "Please choose an answer",
            });
            return;
        }

        this.getServerSubmitAnswer();
    };

    onNextButtonClick = () => {
        this.getQuestion();
    };

    onAskNaoButtonClick = () => {
        this.getHint();
    };

    onStartButtonClick = () => {
        this.getQuestion(true);
    };
}

export default Quiz;
