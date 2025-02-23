import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { Button } from 'reactstrap';
import 'bootstrap/dist/css/bootstrap.css';

const LoginButton = () => {
  const { loginWithRedirect } = useAuth0();

  return <Button classname='login-button' onClick={() => loginWithRedirect()}>Login with Google</Button>;
};

export default LoginButton;