import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { noTokenRequest } from '../../../http';
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import { Link } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate();
  const [values, setValues] = useState({
    username: '',
    password: ''
  });

  function handleChange(e) {
    const target = e.target;
    const value = target.value;
    const name = target.name;
    setValues({ ...values, [name]: value });
  }

  function loginOperation() {
    noTokenRequest.post('/login', {
      username: values.username,
      password: values.password
    })
    .then((res) => {
      localStorage.setItem('access_token', res.data.data.access_token);
      localStorage.setItem('token_type', res.data.data.token_type);
      localStorage.setItem('user_id', res.data.data.id);
      if (res.data.data.is_staff) {
        localStorage.setItem('is_staff', true);
      }
      navigate('/home');
    })
    .catch((error) => {
      console.log(error);
    })
  }

  const loginForm = {
    margin: '50px'
  }

  const signupStyle = {
    width: '300px',
    border: '1px solid gray',
    margin: '50px'
  }

  return (
    <>
        <div style={loginForm}>
        <TextField id="outlined-basic" label="Username" variant="outlined" name="username" value={values.username} onChange={handleChange} />
        <TextField id="outlined-basic" label="Password" variant="outlined" name="password" value={values.password} onChange={handleChange} style={{'padding-left': '10px'}} />
        <Button variant="contained" style={{ margin: "10px" }} onClick={loginOperation}>
            Login
        </Button>
        </div>
        <div style={signupStyle}>
            <label style={{'padding-left': '20px'}}>Don't have an account?</label>
            <Link to="/Signup" style={{'padding-left': '20px'}}>Signup</Link>
        </div>
    </>
  );
};

export default Login;