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
    /*-----*/
    const [inputMessage, setInputMessage] = useState(null);
    const [picturePreview, setPicturePreview] = useState(false);
    const [pictureBlob, setPictureBlob] = useState(null);
    const [avatarPicture, setAvatarPicture] = useState(null);
    const [otherName, setOtherName] = useState(null);
    const [messages, setMessages] = useState([]);
    const [fetching, setFetching] = useState(false);
    const [firstRequest, setFirstRequest] = useState(true);
    const [displayedLatestId, setDisplayedLatestId] = useState(null);
    const [deletingMessage, setDeletingMessage] = useState(false);
    /*---*/
    requestHeaders.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;
    multipartFormData.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;

    useEffect(() => {
        if (acceptId) {
            getAcceptDetail();
            getMessages();
        }
    }, []);

    useInterval(() => {
        getAcceptDetail();
        getMessagesLatest();
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
                price_in_negotiation: inputPriceInNegotiation ? acceptRecord.price_in_negotiation : data.price_in_negotiation,
                min_price: data.price_range.min,
                max_price: data.price_range.max,
                fee_id: data.fee.id,
                fee_percentage: data.fee.percentage,
                enable_cancel: data.enables.cancel,
                enable_request_price: data.enables.request_price,
                enable_response_price: data.enables.response_price,
                enable_payment: data.enables.payment,
                enable_deliver: data.enables.deliver,
                enable_complete: data.enables.complete,
                enable_send_message: data.enables.send_message
            });
            setAvatarPicture(user_id == data.client.id ? data.client.profile_picture : data.contractor.profile_picture);
            setOtherName(user_id == data.client_id ? data.client.nickname : data.contractor.nickname);
        })
    }

    function getMessages() {
        setFetching(true);
        withTokenRequest.post('/getMessagesAccept', {
            accept_id: acceptId,
            displayed_latest_id: null
        }, {
            headers: requestHeaders
        }).then((res) => {
            if (res.data.data.messages.length) {
                setMessages(res.data.data.messages);
                setReadMessages(res.data.data.messages[res.data.data.messages.length - 1].id);
                setDisplayedLatestId(res.data.data.messages[res.data.data.messages.length - 1].id);
            }
            setFirstRequest(false);
            setFetching(false);
        })
    }

    function getMessagesLatest() {
        if (!firstRequest && !fetching && !deletingMessage) {
            setFetching(true);
            withTokenRequest.post('/getMessagesAccept', {
                accept_id: acceptId,
                displayed_latest_id: displayedLatestId
            }, {
                headers: requestHeaders
            }).then((res) => {
                if (res.data.data.messages.length) {
                    setDisplayedLatestId(res.data.data.messages[res.data.data.messages.length - 1].id);
                    setMessages(prevArray => prevArray.concat(res.data.data.messages));
                    setReadMessages(res.data.data.messages[res.data.data.messages.length - 1].id);
                }
                setFetching(false);
            })
        }
    }

    function setReadMessages(id) {
        withTokenRequest.post('/setReadMessagesAccept', {
            accept_id: acceptId,
            displayed_latest_id: id
        }, {
            headers: requestHeaders
        }).then((res) => {
        });
    }

    function requestPrice() {
        withTokenRequest.post('/requestPriceAccept', {
            accept_id: acceptId,
            request_price: acceptRecord.price_in_negotiation,
        }, {
            headers: requestHeaders
        }).then((res) => {
            setInputPriceInNegotiation(false);
            getAcceptDetail();
        });
    }

    function responsePrice(response) {
        withTokenRequest.post('/responsePriceAccept', {
            accept_id: acceptId,
            response: response
        }, {
            headers: requestHeaders
        }).then((res) => {
            getAcceptDetail();
        });
    }

    function payForAccept() {
        withTokenRequest.post('/payForAccept', {
            accept_id: acceptId,
        }, {
            headers: requestHeaders
        }).then((res) => {
            getAcceptDetail();
        });
    }

    function deliverProductAccept() {
        withTokenRequest.post('deliverProductAccept', {
            accept_id: acceptId,
        }, {
            headers: requestHeaders
        }).then((res) => {
            getAcceptDetail();
        });
    }

    function completeTransactionAccept() {
        withTokenRequest.post('completeTransactionAccept', {
            accept_id: acceptId,
        }, {
            headers: requestHeaders
        }).then((res) => {
            getAcceptDetail();
        });
    }

    function cancelTransactionAccept() {
        withTokenRequest.post('cancelTransactionAccept', {
            accept_id: acceptId,
        }, {
            headers: requestHeaders
        }).then((res) => {
            getAcceptDetail();
        });
    }

    function handleChange(e, newValue, setterName, setterParams) {
        const target = e.target;
        const value = target.value;
        const name = target.name;
        switch (setterName) {
            case 'setPriceInNegotiation':
                setInputPriceInNegotiation(true);
                setAcceptRecord({
                    ...acceptRecord,
                    price_in_negotiation: value
                });
                break;
            }
    }

    const messageGroups = groupByDate(messages);
    function groupByDate(messages) {
        return messages.reduce((groups, message) => {
            const date = new Date(message.created_at).toLocaleDateString('ja-JP', { year: 'numeric', month: '2-digit', day: '2-digit' }).split('/').reverse().join('/');
            const lastGroup = groups[groups.length - 1];
        
            if (lastGroup && lastGroup.date === date) {
              lastGroup.messages.push(message);
            } else {
              groups.push({ date, messages: [message] });
            }
            return groups;
          }, []);
    }

    function sendMessage() {
        let requestMessage = inputMessage;
        if (requestMessage.includes('<inputmessage>')) {
            requestMessage = requestMessage.substring(requestMessage.indexOf('<inputmessage>') + 14, requestMessage.indexOf('</inputmessage>'));
            requestMessage = requestMessage.replace(/n/, '');
        }
        if (requestMessage == '' || !requestMessage.length || requestMessage == null) {
            requestMessage = '';
        }
        const submitData = new FormData();
        submitData.append('accept_id', acceptId);
        submitData.append('message', requestMessage);
        submitData.append('picture', pictureBlob);
        withTokenRequest.post('/sendMessageAccept', submitData, {
            headers: multipartFormData
        }).then(() => {
            setInputMessage(null);
            setPicturePreview(false);
            setPictureBlob(null);
            getMessagesLatest();
        })
    }

    const handleAttachClick = () => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        input.onchange = (event) => {
          const file = event.target.files[0];
          const reader = new FileReader();
          reader.readAsDataURL(file);
          reader.onload = () => {
            setPicturePreview(true);
            setPictureBlob(file);
            setInputMessage(`
            <div style={{ position: 'relative', display: 'inline-block' }}>
                <img src="${reader.result}" alt="attachment preview" width="200" style={{ zIndex: 1 }} />
            </div><br><inputmessage>${inputMessage || ''}</inputmessage>
            `);       
          };
        };
        input.click();
    };

    function handleRemoveInputPicture() {
        let temp = inputMessage.substring(inputMessage.indexOf('<inputmessage>') + 14, inputMessage.indexOf('</inputmessage>'));
        if (temp < 0) {
            setInputMessage(null);
        } else {
            setInputMessage(temp.replace(/n/, ''));
        }
        setPicturePreview(false);
        setPictureBlob(null);
    };

    const handleInputMessage = (innerHtml, textContent, innerText, nodes) => {
        if (inputMessage == null || !inputMessage.includes('<inputmessage></inputmessage>')) {
            setInputMessage(innerHtml);
        } else if (inputMessage.includes('<inputmessage></inputmessage>')) {
            setInputMessage(inputMessage.replace('<inputmessage></inputmessage>', '<inputmessage>' + innerText + '</inputmessage>'))
        }
    };

    const handleMouseEnter = (messageId) => {
        if (acceptRecord.enable_send_message) {
            document.getElementById(`delete-button-${messageId}`).style.display = "inline";
            document.getElementById(`message-${messageId}`).style.marginLeft="5px";
        }
    }
    
    const handleMouseLeave = (messageId) => {
        document.getElementById(`delete-button-${messageId}`).style.display = "none";
        document.getElementById(`message-${messageId}`).style.removeProperty('margin-left');
    }

    const deleteMessage = (message) => {
        setDeletingMessage(message);
        withTokenRequest.post('/deleteMessageAccept', {
            message_id: message,
            accept_id: acceptId,
        }, {
            headers: requestHeaders
        }).then(() => {
            setDeletingMessage(null);
            getMessages();
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
    const styledTextArea = styled.textarea`
        width: 100%;
        height: 100%;
        resize: none;
        border: none;
        padding: 10px;
        font-size: 16px;
        box-sizing: border-box;
        white-space: pre-wrap;
        caret-color: #2a9d8f;
        `;
    const messageFrame = {
        margin: '20px auto',
        border: 'solid black',
        width: '100%',
        position: 'relative',
        height: '900px'
    };

    if (!acceptRecord) {
        return (
            <></>
        )
    }
    let fees = '';
    if (localStorage.getItem('user_id') == acceptRecord.contractor_id) {
        fees = <>
            <TableRow>
               <TableCell style={keyColumnStyle}>Fee {acceptRecord.fee_id ? (`(${acceptRecord.fee_percentage * 100}%)`) : (null)}</TableCell>
               <TableCell style={{fontWeight: 'bold', fontSize: '20px', color: 'red'}}>{acceptRecord.price ? (`$${acceptRecord.price * acceptRecord.fee_percentage}`) : (`-`)}</TableCell>
            </TableRow>
            <TableRow>
               <TableCell style={keyColumnStyle}>Revenue</TableCell>
               <TableCell style={{fontWeight: 'bold', fontSize: '20px', color: 'red'}}>{acceptRecord.price ? (`$${acceptRecord.price - acceptRecord.price * acceptRecord.fee_percentage}`) : (`-`)}</TableCell>
            </TableRow>
        </>
    }
    let requestPriceComponent = '';
    if (acceptRecord.status <= 1 && acceptRecord.client_id == localStorage.getItem('user_id')) {
        requestPriceComponent = <>
            {acceptRecord.status == 0 && !acceptRecord.enable_response_price ? <p>Pending Approval</p> : null}
            <div style={{display: 'flex'}}>
                <FormControl sx={{ width: 200 }} variant="standard">
                    <InputLabel htmlFor="standard-adornment-price">Request Price</InputLabel>
                    <Input
                        id="standard-adornment-price"
                        startAdornment={<InputAdornment position="start">$</InputAdornment>}
                        value={acceptRecord.price_in_negotiation}
                        onChange={(event, newValue) => {handleChange(event, newValue, 'setPriceInNegotiation', null);}}
                        disabled={!acceptRecord.enable_request_price}
                    />
                </FormControl>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <Button variant="contained" disabled={!acceptRecord.enable_request_price} onClick={requestPrice}>Request</Button>
            </div>
        </>
    }
    let responsePriceComponent = '';
    if (acceptRecord.enable_response_price) {
        responsePriceComponent = <>
            <p style={{'font-weight': 'bold'}}>Request Price: &nbsp;<span style={{'color': 'red'}}>${acceptRecord.price_in_negotiation}</span></p>
            <div style={{display: 'flex'}}>
                <Button variant="contained" onClick={() => responsePrice(true)}>Accept</Button>&nbsp;&nbsp;
                <Button variant="contained" onClick={() => responsePrice(false)}>Reject</Button>
            </div>
        </>;
    }
    let payComponent = '';
    if (acceptRecord.enable_payment) {
        payComponent = <>
            <ConfirmDialog text='Payment' message='Are you sure you want to payment?' callback={payForAccept}/>
            <br /><br />
        </>;
    }
    let deliverComponent = '';
    if (acceptRecord.enable_deliver) {
        deliverComponent = <>
            <ConfirmDialog text='Complete Deliver' message='Are you sure you have completed delivery?' callback={deliverProductAccept}/>
            <br /><br />
        </>;
    }
    let completeComponent = '';
    if (acceptRecord.enable_complete) {
        completeComponent = <>
            <ConfirmDialog text='Complete Transaction' message='Are you sure you want to complete transaction?' callback={completeTransactionAccept}/>
            <br /><br />
        </>;
    }
    let cancelComponent = '';
    if (acceptRecord.enable_cancel) {
        cancelComponent = <>
            <ConfirmDialog text='Cancel Transaction' message='Are you sure you want to cancel transaction?' callback={cancelTransactionAccept}/>
            <br /><br />
        </>;
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
                                <TableRow>
                                    <TableCell style={keyColumnStyle}>Price Range</TableCell>
                                    <TableCell style={{fontWeight: 'bold', fontSize: '20px', color: 'red'}}>${acceptRecord.min_price} - ${acceptRecord.max_price}</TableCell>
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
                    {payComponent}<br />
                    {deliverComponent}<br />
                    {completeComponent}<br />
                    {requestPriceComponent}<br />
                    {responsePriceComponent}<br />
                    {cancelComponent}<br />
                </div>

                {/*  */}

                <div style={messageFrame}>
                    <ChatContainer>
                        <ConversationHeader>
                            <Avatar src={`data:image/jpeg;base64,${avatarPicture}`}></Avatar>
                            <ConversationHeader.Content
                                userName={otherName}
                            />
                        </ConversationHeader>
                            <MessageList style={{height: '800px'}}>
                            {messageGroups.map((group, index) => (
                                <>
                                {<MessageSeparator content={group.date}/>}
                                {group.messages.map((message) => (
                                    <>
                                        {message.sender_id == localStorage.getItem('user_id') && message.message != null && !message.picture && (
                                            <div style={{display: 'flex'}} key={message.id} onMouseEnter={() => handleMouseEnter(message.id)} onMouseLeave={() => handleMouseLeave(message.id)}>
                                                <Delete
                                                    id={`delete-button-${message.id}`}
                                                    style={{ display: 'none', cursor: 'pointer', 'margin-right': '0px', 'margin-left': 'auto' }}
                                                    onClick={() => {
                                                        if (window.confirm('Are you sure you want to delete?')) {
                                                            deleteMessage(message.id);
                                                        }
                                                    }}
                                                />
                                                <Message className="outgoing"
                                                id={`message-${message.id}`}
                                                model={{
                                                message: message.message,
                                                direction: 'outgoing',
                                                position: 'single',
                                                }}
                                                >
                                                    <Message.Footer sentTime={message.created_at.split('.')[0].split('T')[1]} />
                                                </Message>
                                            </div>
                                        )}
                                        {message.sender_id == localStorage.getItem('user_id') && message.message == null && message.picture && (
                                            <div style={{display: 'flex'}} key={message.id} onMouseEnter={() => handleMouseEnter(message.id)} onMouseLeave={() => handleMouseLeave(message.id)}>
                                                <Delete
                                                    id={`delete-button-${message.id}`}
                                                    style={{ display: 'none', cursor: 'pointer', 'margin-right': '0px', 'margin-left': 'auto' }}
                                                    onClick={() => {
                                                        if (window.confirm('Are you sure you want to delete?')) {
                                                            deleteMessage(message.id);
                                                        }
                                                    }}
                                                />
                                                <Message className="outgoing"
                                                id={`message-${message.id}`}
                                                model={{
                                                direction: 'outgoing',
                                                position: 'single',
                                                }}
                                            >
                                                <Message.ImageContent src={`data:image/jpeg;base64,${message.picture}`} alt="picture" width={300} />
                                                <Message.Footer sentTime={message.created_at.split('.')[0].split('T')[1]} />
                                            </Message>
                                            </div>
                                        )}
                                        {message.sender_id == localStorage.getItem('user_id') && message.message != null && message.picture && (
                                            <>
                                                <div key={message.id} onMouseEnter={() => handleMouseEnter(message.id)} onMouseLeave={() => handleMouseLeave(message.id)}>
                                                    <div style={{display: 'flex'}}>
                                                        <Delete
                                                            id={`delete-button-${message.id}`}
                                                            style={{ display: 'none', cursor: 'pointer', 'margin-right': '0px', 'margin-left': 'auto' }}
                                                            onClick={() => {
                                                                if (window.confirm('Are you sure you want to delete?')) {
                                                                    deleteMessage(message.id);
                                                                }
                                                            }}
                                                        />
                                                        <Message className="outgoing"
                                                        id={`message-${message.id}`}
                                                        model={{
                                                        direction: 'outgoing',
                                                        position: 'single',
                                                        }}
                                                    >
                                                        <Message.ImageContent src={`data:image/jpeg;base64,${message.picture}`} alt="picture" width={300} />
                                                    </Message>
                                                    </div>
                                                    <Message
                                                        model={{
                                                            message: message.message,
                                                            direction: 'outgoing',
                                                            position: 'bottom',
                                                        }}
                                                    ><Message.Footer sentTime={message.created_at.split('.')[0].split('T')[1]} />
                                                    </Message>
                                                </div>
                                            </>
                                        )}
                                        {message.sender_id != localStorage.getItem('user_id') && message.message != null && !message.picture && (
                                                <Message
                                                model={{
                                                message: message.message,
                                                direction: 'incoming',
                                                position: 'single',
                                                }}
                                                >
                                                    <Message.Footer sender={message.created_at.split('.')[0].split('T')[1]} />
                                                </Message>
                                        )}
                                        {message.sender_id != localStorage.getItem('user_id') && message.message == null && message.picture && (
                                                <Message
                                                model={{
                                                direction: 'incoming',
                                                position: 'single',
                                                }}
                                            >
                                                <Message.ImageContent src={`data:image/jpeg;base64,${message.picture}`} alt="picture" width={300} />
                                                <Message.Footer sender={message.created_at.split('.')[0].split('T')[1]} />
                                            </Message>
                                        )}
                                        {message.sender_id != localStorage.getItem('user_id') && message.message != null && message.picture && (
                                            <>
                                                <Message
                                                model={{
                                                direction: 'incoming',
                                                position: 'single',
                                                }}
                                                >
                                                    <Message.ImageContent src={`data:image/jpeg;base64,${message.picture}`} alt="picture" width={300} />
                                                </Message>
                                                <Message
                                                    model={{
                                                        message: message.message,
                                                        direction: 'incoming',
                                                        position: 'bottom',
                                                    }}
                                                >
                                                    <Message.Footer sender={message.created_at.split('.')[0].split('T')[1]} />
                                                </Message>
                                            </> 
                                        )}
                                    </>
                                ))}
                                </>
                            ))}
                            </MessageList>
                        <MessageInput
                            placeholder="Type your message here..."
                            multiline={true}
                            onSend={sendMessage}
                            value={inputMessage}
                            onChange={handleInputMessage}
                            attachButton={true}
                            attachDisabled={picturePreview}
                            sendButton={true}
                            sendDisabled={false}
                            onAttachClick={handleAttachClick}
                            style={{styledTextArea}}
                         >
                        </MessageInput>
                    </ChatContainer>
                    <Delete className="deletePreview" style={{visibility: picturePreview ? 'visible' : 'hidden', width: '30px', position: 'absolute', top: '800px', left: '6px'}} onClick={handleRemoveInputPicture}></Delete>
                </div>
            </div>
        </>
    )
}

export default TransactionChatRequest;