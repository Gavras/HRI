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
        this.getQuestion();
    }

    getQuestion() {
        const xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function () {
            if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
                for (const [ref, object] of Object.entries(this.refs)) {
                    if (ref.startsWith('radioAnswerOption')) {
                        object.checked = false;
                    }
                }
                this.setState({
                    question: JSON.parse(xmlHttp.responseText),
                    userAnswer: null,
                    serverSubmitAnswer: null,
                    hint: null,
                });
            }
        }.bind(this);
        xmlHttp.open('GET', this.BACKEND_URL + 'get_question', true);
        xmlHttp.send(null);
    }

    getServerSubmitAnswer() {
        const xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function () {
            if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
                this.setState({
                    serverSubmitAnswer: xmlHttp.responseText,
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
        let column = null;
        switch (this.state.phase) {
            case Phase.started:
                column = this.renderLandingPage();
                break;
            case Phase.quiz:
                column = this.renderQuizContent();
                break;
            case Phase.ended:
                break;
        }

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

    renderStartButton() {
        const start_button_img = require('./images/start_picture.png').default;
        return (
            <Image src={start_button_img} alt="start_button_img" fluid className="h-100 max-vh-50"
                   onClick={() => this.onStartButtonClick()}/>
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
                onClick={() => this.onAnswerOptionClick(option)}
            />,
        );
    }

    renderActionButtons() {
        const submitButton =
            <Button onClick={this.onSubmitButtonClick}>
                Submit
            </Button>;

        const nextButton =
            <Button
                onClick={this.onNextButtonClick}
                className="ml-1">
                Next Question
            </Button>;

        const askNaoButton =
            <Button
                variant="info" className="mt-2"
                onClick={this.onAskNaoButtonClick}>
                Ask Nao
            </Button>;

        return (
            <div className="mt-2">
                {submitButton}
                {nextButton}
                {this.renderSubmitResponse()}
                <br/>
                {askNaoButton}
                {this.renderHintResponse()}
            </div>
        );
    }

    renderSubmitResponse() {
        if (this.state.serverSubmitAnswer == null) {
            return null;
        }

        return (
            <Alert variant="success" className="m-0 mt-1">
                {this.state.serverSubmitAnswer}
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
        const nao_img = require('./images/nao_picture.png').default;
        return (
            <Image src={nao_img} alt="nao_img" fluid className="h-100 max-vh-50"/>
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
        this.setState({
            phase: Phase.quiz,
        });
    };
}

export default Quiz;
