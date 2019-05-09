import React, {Component} from 'react';
import Button from '@material-ui/core/Button';
import Input from '@material-ui/core/Input';
import Typography from '@material-ui/core/Typography';
import './App.css';

class App extends Component{

    submitForm = () => {
        const data = new FormData();
        data.append('crn', this.state.crn)
        data.append('term', this.state.term)

        fetch("/submit", {
            method: 'POST',
            body: data
        }).then(
            (result) => {
                console.log(result.text())
            },
            (error) => {
            }
        )
    }

    crnchange = (e) => {
        this.setState({crn: e.target.value})
    }

    termchange = (e) => {
        this.setState({term: e.target.value})
    }

    render() {
        return (
            <div className="App">
                <Typography variant="h4" noWrap>
                    Enter Classes to Be Tracked
                </Typography>

                <div className="crnInput">
                    <Typography variant="h6" noWrap>
                        CRN:
                        <Input onChange={this.crnchange} className="data1" variant="outlined"></Input>
                    </Typography>
                </div>
                <div className="termInput">
                    <Typography variant="h6" noWrap>
                        Term:
                        <Input onChange={this.termchange} className="data1" variant="outlined"></Input>
                    </Typography>
                </div>
                <div className="submit">
                    <Button variant="contained" color="primary" onClick={this.submitForm}>
                        Submit Form
                    </Button>
                </div>
            </div>
        );
    }
}

export default App
