import PropTypes from 'prop-types';
import React from 'react';
import { Button, Form, FormGroup, Input, Label } from 'reactstrap';

class AuthForm extends React.Component {
  state = {
    username:'',
    password:'',
    error:'',
  };

  handleUserChange = (e) => {
    this.setState({username: e.target.value});
  }

  handlePassChange = (e) => {
    this.setState({password: e.target.value});
  }

  handleSubmit = event => {
    event.preventDefault();

    if (this.state.username == "test" && this.state.password == "dbshackathon") {
      window.location.href = "/dashboard";
    } else {
      this.setState({error: "Incorrect username and password. Please try again."});
    }
  };

  render() {
    const {
      usernameLabel,
      usernameInputProps,
      passwordLabel,
      passwordInputProps,
      children,
    } = this.props;
    const hStyle = { color: 'red' };

    return (
      <Form onSubmit={this.handleSubmit}>
        <FormGroup>
          <Label for={usernameLabel}>{usernameLabel}</Label>
          <Input {...usernameInputProps} onChange={e => this.handleUserChange(e)} />
        </FormGroup>
        <FormGroup>
          <Label for={passwordLabel}>{passwordLabel}</Label>
          <Input {...passwordInputProps} onChange={e => this.handlePassChange(e)} />
        </FormGroup>
        <hr />
        <Button
          size="lg"
          className="bg-gradient-theme-left border-0"
          block
          onClick={this.handleSubmit}>
          Login
        </Button>
        <Label style={hStyle}>{this.state.error}</Label>
        {children}
      </Form>
    );
  }
}

export const STATE_LOGIN = 'LOGIN';
export const STATE_SIGNUP = 'SIGNUP';

AuthForm.propTypes = {
  showLogo: PropTypes.bool,
  usernameLabel: PropTypes.string,
  usernameInputProps: PropTypes.object,
  passwordLabel: PropTypes.string,
  passwordInputProps: PropTypes.object,
  onLogoClick: PropTypes.func,
};

AuthForm.defaultProps = {
  showLogo: true,
  usernameLabel: 'Username',
  usernameInputProps: {
    type: 'string',
    placeholder: 'your username',
  },
  passwordLabel: 'Password',
  passwordInputProps: {
    type: 'password',
    placeholder: 'your password',
  },
  onLogoClick: () => {},
};

export default AuthForm;
