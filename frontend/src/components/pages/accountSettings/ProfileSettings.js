import SideBar_AccountSettings from './SideBar_AccountSettings';
import { useEffect, useState } from 'react';
import { withTokenRequest, requestHeaders } from '../../../http';
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";

const ProfileSettings = () => {
    const [values, setValues] = useState({
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        nickname: '',
        bank_account: '',
    });
    requestHeaders.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;

    useEffect(() => {
        getUserProfile();
    }, []);

    function getUserProfile() {
        withTokenRequest.post('/getUserProfile', {
            id: localStorage.getItem('user_id')
        }, {
            headers: requestHeaders
        }).then((res) => {
            setValues(res.data.data);
        })
    }

    function setUserProfile() {
        withTokenRequest.post('/setUserProfile', {
            id: localStorage.getItem('user_id'),
            username: values.username,
            first_name: values.first_name,
            last_name: values.last_name,
            nickname: values.nickname,
            email: values.email,
            bank_account: values.bank_account
        }, {
            headers: requestHeaders
        }).then(() => {
            getUserProfile();
        }).catch((error) => {
            console.log(error);
        })
    }

    function handleChange(e) {
        const target = e.target;
        const value = target.value;
        const name = target.name;
        setValues({...values, [name]: value});
    }

    const mainContents = {
        float: 'left',
        margin: '10px',
        'text-align': 'center',
        width: 'calc(100% - 362px)'
    }

    return (
        <>
            <div>
                <SideBar_AccountSettings />
                <div style={mainContents}>
                    <h2>Profile Settings</h2>
                    <TextField id="outlined-basic" label="Username" variant='outlined' name="username" value={values.username} onChange={handleChange}/><br /><br />
                    <TextField id="outlined-basic" label="First Name" variant='outlined' name="first_name" value={values.first_name} onChange={handleChange}/><br /><br />
                    <TextField id="outlined-basic" label="Last Name" variant='outlined' name="last_name" value={values.last_name} onChange={handleChange}/><br /><br />
                    <TextField id="outlined-basic" label="Nickname" variant='outlined' name="nickname" value={values.nickname} onChange={handleChange}/><br /><br />
                    <TextField id="outlined-basic" label="Email" variant='outlined' name="email" value={values.email} onChange={handleChange}/><br /><br />
                    <TextField id="outlined-basic" label="Bank Account" variant='outlined' name="bank_account" value={values.bank_account} onChange={handleChange}/><br /><br />
                    <Button variant="contained" style={{ margin: "10px" }} onClick={setUserProfile}>Save</Button>
                </div>
            </div>
        </>
    )
}

export default ProfileSettings;