import { noTokenRequest } from '../../../http';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";

export default function Signup() {
    const navigate = useNavigate();
    const [values, setValues] = useState({
        username: '',
        password: '',
        email: '',
        first_name: '',
        last_name: '',
        nickname: '',
        bank_account: '',
    });

    function handleChange(e) {
        const target = e.target;
        const value = target.value;
        const name = target.name;
        setValues({...values, [name]: value});
    }

    function registerUser() {    
        noTokenRequest.post('/signup', {
            username: values.username,
            password: values.password,
            first_name: values.first_name,
            last_name: values.last_name,
            nickname: values.nickname,
            email: values.email,
            bank_account: values.bank_account
        })
        .then((res) => {
            localStorage.setItem('access_token', res.data.data.access_token);
            localStorage.setItem('token_type', res.data.data.token_type);
            localStorage.setItem('user_id', res.data.data.id);
            navigate('/home');
        })
        .catch((error) => {
            console.log(error);
        });
    }

    const signupForm = {
        'margin-top': '50px',
        'text-align': 'center'
    };

    return (
        <>
            <div style={signupForm}>
                <h2>Signup</h2>
                <TextField id="outlined-basic" label="Username" variant='outlined' name="username" value={values.username} onChange={handleChange}/><br /><br />
                <TextField id="outlined-basic" type="password" label="Password" variant='outlined' name="password" value={values.password} onChange={handleChange}/><br /><br />
                <TextField id="outlined-basic" label="First Name" variant='outlined' name="first_name" value={values.first_name} onChange={handleChange}/><br /><br />
                <TextField id="outlined-basic" label="Last Name" variant='outlined' name="last_name" value={values.last_name} onChange={handleChange}/><br /><br />
                <TextField id="outlined-basic" label="Nickname" variant='outlined' name="nickname" value={values.nickname} onChange={handleChange}/><br /><br />
                <TextField id="outlined-basic" label="Email" variant='outlined' name="email" value={values.email} onChange={handleChange}/><br /><br />
                <TextField id="outlined-basic" label="Bank Account" variant='outlined' name="bank_account" value={values.bank_account} onChange={handleChange}/><br /><br />
                <Button variant="contained" style={{ margin: "10px" }} onClick={registerUser}>Register</Button>
            </div>
        </>
    )
}

