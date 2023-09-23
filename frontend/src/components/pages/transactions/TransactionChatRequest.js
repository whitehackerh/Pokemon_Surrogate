import { useRef, useState, useEffect } from "react";
import { useNavigate, useLocation } from 'react-router-dom';
import { withTokenRequest, requestHeaders, multipartFormData } from '../../../http';
import Button from "@mui/material/Button";
import CustomSlider from "../../modules/CustomSlider/CustomSlider";
import { Table, TableBody, TableCell, TableRow, TableContainer, Paper } from '@mui/material';
import ConfirmDialog from "../../modules/dialogs/ConfirmDialog";
import FormControl from '@mui/material/FormControl';
import InputAdornment from '@mui/material/InputAdornment';
import Input from '@mui/material/Input';
import InputLabel from '@mui/material/InputLabel';
import useInterval from 'use-interval';
import { ChatContainer, MessageList, Message, MessageInput, ConversationHeader, Avatar, MessageSeparator } from '@chatscope/chat-ui-kit-react';
import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import styled from 'styled-components';
import Delete from '@mui/icons-material/Delete';

const TransactionChatRequest = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const acceptId = location.state.acceptId;
    const [pictures, setPictures] = useState([]);
    const [acceptRecord, setAcceptRecord] = useState(null);
    const [inputPriceInNegotiation, setInputPriceInNegotiation] = useState(false);
    requestHeaders.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;
    multipartFormData.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;

    useEffect(() => {
        if (acceptId) {
            getAcceptDetail();
        }
    }, []);

    useInterval(() => {
        getAcceptDetail();
    }, 5000);

    function getAcceptDetail() {
        const user_id = localStorage.getItem('user_id');
        withTokenRequest.post('/getAcceptDetail', {
            accept_id: acceptId
        }, {
            headers: requestHeaders
        }).then((res) => {
            const data = res.data.data;
            setPictures(data.request_pictures);
            setAcceptRecord({
                client_id: data.client.id,
                client_profile_picture: data.client.profile_picture,
                client_nickname: data.client.nickname,
                contractor_id: data.contractor.id,
                contractor_profile_picture: data.contractor.profile_picture,
                contractor_nickname: data.contractor.nickname,
                status: data.status,
                game_title_id: data.game.id,
                game_title: data.game.title,
                category_id: data.category.id,
                category: data.category.name,
                request_title: data.request_title,
                description: data.description.split('\n'),
                price: data.price,
                price_negotiation: data.price_negotiation,
                price_in_negotiation: inputPriceInNegotiation ? acceptRecord.price_in_negotiation : data.price_in_negotiation,
                min_price: data.price_range.min,
                max_price: data.price_range.max,
                fee_id: data.fee.id,
                fee_percentage: data.fee.percentage,
                enable_cancel: data.enables.cancel,
                enable_request_change_price: data.enables.request_change_price,
                enable_response_change_price: data.enables.response_change_price,
                enable_payment: data.enables.payment,
                enable_deliver: data.enables.deliver,
                enable_complete: data.enables.complete,
                enable_send_message: data.enables.send_message
            });
        })
    }

    const mainContents = {
        float: 'left',
        margin: '10px',
        // 'text-align': 'center',
        width: 'calc(100% - 362px)',
        display: 'flex'
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

    if (!acceptRecord) {
        return (
            <></>
        )
    }
    let fees = '';
    if (localStorage.getItem('user_id') == acceptRecord.contractor_id) {
        fees = <>
            <TableRow>
               <TableCell style={keyColumnStyle}>Fee {acceptRecord.fee_id ? (`${acceptRecord.fee_percentage * 100}%`) : (null)}</TableCell>
               <TableCell style={{fontWeight: 'bold', fontSize: '20px', color: 'red'}}>{acceptRecord.price ? (`$${acceptRecord.price * acceptRecord.fee_percentage}`) : (`-`)}</TableCell>
            </TableRow>
            <TableRow>
               <TableCell style={keyColumnStyle}>Revenue</TableCell>
               <TableCell style={{fontWeight: 'bold', fontSize: '20px', color: 'red'}}>{acceptRecord.price ? (`$${acceptRecord.price - acceptRecord.price * acceptRecord.fee_percentage}`) : (`-`)}</TableCell>
            </TableRow>
        </>
    }
    if (!acceptId) {
        return <></>;
    }
    return (
        <>
            <div style={mainContents}>
                <div style={{ width: '100%'}}>
                    <div style={sliderStyle}>
                        <CustomSlider>
                            {pictures.map((picture, index) => {
                                return <img key={index} src={`data:image/jpeg;base64,${picture}`}/>;
                            })}
                        </CustomSlider>
                    </div>
                    <br /><br />
                    <h2 style={{backGroundColor: 'blue'}}>{acceptRecord.request_title}</h2><br />
                    <div style={{fontWeight: 'bold', backgroundColor: 'black', color: 'white', width: '70%', height: '25px'}}>Description of request</div><br />
                    {acceptRecord.description.map((line, index) => (
                        <>
                        {line}
                        <br />
                        </>
                    ))}
                    <br />
                    <TableContainer component={Paper} style={{width: '70%'}}>
                        <Table>
                            <TableBody>
                                <TableRow>
                                    <TableCell style={keyColumnStyle}>Game Title</TableCell>
                                    <TableCell>{acceptRecord.game_title}</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell style={keyColumnStyle}>Category</TableCell>
                                    <TableCell>{acceptRecord.category}</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell style={keyColumnStyle}>Price</TableCell>
                                    <TableCell style={{fontWeight: 'bold', fontSize: '20px', color: 'red'}}>{acceptRecord.price ? (`$${acceptRecord.price}`) : (`T.B.D`)}</TableCell>
                                </TableRow>
                                {fees}
                            </TableBody>
                        </Table>
                    </TableContainer>
                    <br /><br />
                    <div style={{fontWeight: 'bold'}}>Client</div><br />
                    <div style={{border: '1px solid black', height: '50px', width: '40%', display: 'flex'}}>
                        <img src={`data:image/jpeg;base64,${acceptRecord.client_profile_picture}`} style={profilePictureStyle}></img>
                        <div style={{fontWeight: 'bold'}}>&nbsp;{acceptRecord.client_nickname}</div>
                    </div><br />
                    <div style={{fontWeight: 'bold'}}>Contractor</div><br />
                    <div style={{border: '1px solid black', height: '50px', width: '40%', display: 'flex'}}>
                        <img src={`data:image/jpeg;base64,${acceptRecord.contractor_profile_picture}`} style={profilePictureStyle}></img>
                        <div style={{fontWeight: 'bold'}}>&nbsp;{acceptRecord.contractor_nickname}</div>
                    </div><br /><br />
                </div>
            </div>
        </>
    )
}

export default TransactionChatRequest;