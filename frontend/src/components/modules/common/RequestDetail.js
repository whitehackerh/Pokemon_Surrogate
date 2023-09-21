import React, { useRef, useState, useEffect } from "react";
import { useNavigate, useLocation } from 'react-router-dom';
import { noTokenRequest, withTokenRequest, requestHeaders } from '../../../http';
import Button from "@mui/material/Button";
import SideBar_Transactions from '../../pages/transactions/SideBar_Transactions';
import CustomSlider from "../CustomSlider/CustomSlider";
import { Table, TableBody, TableCell, TableRow, TableContainer, Paper } from '@mui/material';
import ConfirmDialog from "../../modules/dialogs/ConfirmDialog";

const RequestDetail = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const requestId = location.state.requestId;
    const from = location.state.from;
    const [pictures, setPictures] = useState([]);
    const [record, setRecord] = useState(null);
    requestHeaders.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;

    useEffect(() => {
        getRequestDetail();
    }, []);

    function getRequestDetail() {
        withTokenRequest.post('/getRequestDetail', {
            request_id: requestId
        }, {
            headers: requestHeaders
        }).then((res) => {
            const data = res.data.data;
            setPictures(data.pictures);       
            setRecord({
                seller_id: data.seller_id,
                client: {
                    user_id: data.client.user_id,
                    profile_picture: data.client.profile_picture,
                    nickname: data.client.nickname
                },
                status: data.status,
                enables: {
                    edit: data.enables.edit,
                    accept: data.enables.accept
                },
                game: {
                    id: data.game.id,
                    title: data.game.title
                },
                category: {
                    id: data.category.id,
                    name: data.category.name
                },
                request_title: data.request_title,
                description: data.description.split('\n'),
                min_price: data.min_price,
                max_price: data.max_price,
            });
        })
    }

    function removeRequest() {
        withTokenRequest.post('/removeRequest', {
            request_id: requestId
        }, {
            headers: requestHeaders
        }).then((res) => {
            getRequestDetail();
        })
    }

    function clickEdit() {
        navigate('/editRequest', { state: {requestId: requestId}});
    }

    function setAccept() {
        withTokenRequest.post('/setAccept', {
            request_id: requestId
        }, {
            headers: requestHeaders
        }).then((res) => {
            // TODO navigation
            navigate('/home');
        })
    }

    const mainContents = {
        float: 'left',
        margin: '10px',
        marginLeft: from == 'requests' ? '10px' : '500px',
        // 'text-align': 'center',
        width: 'calc(100% - 362px)'
    }
    const sliderStyle = {
        width: '30%'
    }
    const keyColumnStyle = {
        width: '30%',
        backgroundColor: 'gray',
        fontWeight: 'bold'
    }
    const profilePictureStyle = {
        width: '50px',
        height: '50px'
    }

    let sideBar = '';
    if (from == 'requests') {
        sideBar = <>
            <SideBar_Transactions />
        </>
    }
    if (!pictures.length) {
        return (
            <></>
        )
    }
    let buttons = '';
    if (record.enables.edit) {
        buttons = <>
            <div style={{display: 'flex'}}>
                <Button variant="contained" onClick={clickEdit}>Edit</Button>&nbsp;&nbsp;&nbsp;&nbsp;
                <br /><br />
                <ConfirmDialog text='remove' message='Are you sure you want to remove this request?' callback={removeRequest}/>
            </div>
        </>
    } else if (record.enables.accept) {
        buttons = <>
            <ConfirmDialog text='Accept this request' message='Are you sure you want to accept this request?' callback={setAccept}/>
        </>;
    }

    return (
        <>
            {sideBar}
            <div style={mainContents}>
                <div style={sliderStyle}>
                    <CustomSlider>
                        {pictures.map((picture, index) => {
                            return <img key={index} src={`data:image/jpeg;base64,${picture}`}/>;
                        })}
                    </CustomSlider>
                </div>
                <br /><br />
                <h2 style={{backGroundColor: 'blue'}}>{record.request_title}</h2><br />
                <div style={{fontWeight: 'bold', backgroundColor: 'black', color: 'white', width: '40%', height: '25px'}}>Description of request</div><br />
                {record.description.map((line, index) => (
                    <>
                    {line}
                    <br />
                    </>
                ))}
                <br />
                <TableContainer component={Paper} style={{width: '40%'}}>
                    <Table>
                        <TableBody>
                            <TableRow>
                                <TableCell style={keyColumnStyle}>Game Title</TableCell>
                                <TableCell>{record.game.title}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell style={keyColumnStyle}>Category</TableCell>
                                <TableCell>{record.category.name}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell style={keyColumnStyle}>Price</TableCell>
                                <TableCell style={{fontWeight: 'bold', fontSize: '20px', color: 'red'}}>${record.min_price} - ${record.max_price}</TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </TableContainer>
                <br /><br />
                <div style={{fontWeight: 'bold'}}>Client</div><br />
                <div style={{border: '1px solid black', height: '50px', width: '30%', display: 'flex'}}>
                    <img src={`data:image/jpeg;base64,${record.client.profile_picture}`} style={profilePictureStyle}></img>
                    <div style={{fontWeight: 'bold'}}>&nbsp;{record.client.nickname}</div>
                </div><br /><br />
                {buttons}
            </div>
        </>
    )
}

export default RequestDetail;