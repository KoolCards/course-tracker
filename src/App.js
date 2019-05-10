import React, {Component} from 'react';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Switch from '@material-ui/core/Switch'
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import './App.css';

const drawerWidth = 240;

const styles = theme => ({
    root: {
        display: 'flex',
    },
    toolbar: {
        paddingRight: 24, // keep right padding when drawer closed
    },
    toolbarIcon: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'flex-end',
        padding: '0 8px',
        ...theme.mixins.toolbar,
    },
    appBar: {
        zIndex: theme.zIndex.drawer + 1,
        transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
    },
    appBarShift: {
        marginLeft: drawerWidth,
        width: `calc(100% - ${drawerWidth}px)`,
        transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
    },
    submitButton: {
        marginTop: theme.spacing.unit * 2
    },
    crninput: {
        marginTop: theme.spacing.unit * 2
    },
    menuButtonHidden: {
        display: 'none',
    },
    title: {
        flexGrow: 1,
        marginBottom: theme.spacing.unit * 2,
        marginTop: theme.spacing.unit
    },
    drawerPaper: {
        position: 'relative',
        whiteSpace: 'nowrap',
        width: drawerWidth,
        transition: theme.transitions.create('width', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
    },
    drawerPaperClose: {
        overflowX: 'hidden',
        transition: theme.transitions.create('width', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
        width: theme.spacing.unit * 7,
        [theme.breakpoints.up('sm')]: {
            width: theme.spacing.unit * 9,
        },
    },
    appBarSpacer: theme.mixins.toolbar,
    content: {
        flexGrow: 1,
        padding: theme.spacing.unit * 3,
        height: '100vh',
        overflow: 'auto',
    },
    chartContainer: {
        marginLeft: -22,
    },
    tableContainer: {
        height: 320,
    },
    h3: {
        marginBottom: theme.spacing.unit * 2,
    },
    termInput: {
        marginTop: theme.spacing.unit * 2,
        marginLeft: theme.spacing.unit
    },
    formLabel: {
        marginLeft: theme.spacing.unit
    }
});

class App extends Component{

    state = {
        crn: "83870",
        term: "201908",
        checked: true,
        formLabelValue: "Add Courses"
    };

    submitForm = () => {
        const data = new FormData();
        data.append('crn', this.state.crn)
        data.append('term', this.state.term)
        data.append('track', this.state.checked)

        fetch("/submit", {
            method: 'POST',
            body: data
        }).then(
            (result) => {
                console.log(result.text().then(function(resText) {
                    alert(resText)
                }))
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

    switchChange = (e) => {
        this.setState({checked: e.target.checked})
        if (e.target.checked) {
            this.setState({formLabelValue: "Track Courses"})
        } else {
            this.setState({formLabelValue: "Untrack Courses"})
        }
    }

    render() {
        const { classes } = this.props;

        return (
            <div className="App">
                <Typography variant="h3" noWrap className={classes.title}>
                    GT Course Tracker
                </Typography>

                <Typography variant="body2" noWrap>
                    Enter the course CRN (i.e. 83870) and the term in the format year + start month (i.e. 201908).
                </Typography>

                <div className="inputData">
                    <TextField label="CRN: " defaultValue="83870" onChange={this.crnchange} className={classes.crninput} variant="outlined"></TextField>
                    <TextField label="Term: " defaultValue="201908" onChange={this.termchange} className={classes.termInput} variant="outlined"></TextField>
                </div>

                <div className={classes.submitButton}>
                    <Button variant="contained" color="secondary" onClick={this.submitForm}>
                        Submit
                    </Button>
                    <FormControlLabel className={classes.formLabel} control={<Switch checked={this.state.checked} onChange={this.switchChange}/>} label={this.state.formLabelValue}/>
                </div>
            </div>
        );
    }
}

export default withStyles(styles)(App)
