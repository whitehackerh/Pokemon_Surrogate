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

const TransactionChatListing = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const purchaseRequestId = location.state.purchaseRequestId;
    const [pictures, setPictures] = useState([]);
    const [purchaseRequestRecord, setPurchaseRequestRecord] = useState(null);
    const [inputPriceInNegotiation, setInputPriceInNegotiation] = useState(false);
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
    requestHeaders.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;
    multipartFormData.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;

    useEffect(() => {
        if (purchaseRequestId) {
            getPurchaseRequestDetail();
            getMessages();
        }
    }, []);

    useInterval(() => {
        getPurchaseRequestDetail();
        getMessagesLatest();
    }, 5000);

    function getPurchaseRequestDetail() {
        const user_id = localStorage.getItem('user_id');
        withTokenRequest.post('/getPurchaseRequestDetail', {
            purchase_request_id: purchaseRequestId,
            user_id: user_id
        }, {
            headers: requestHeaders
        }).then((res) => {
            const data = res.data.data;
            setPictures(data.listing_pictures);
            setPurchaseRequestRecord({
                seller_id: data.seller_id,
                seller_profile_picture: data.seller_profile_picture,
                seller_nickname: data.seller_nickname,
                buyer_id: data.buyer_id,
                buyer_profile_picture: data.buyer_profile_picture,
                buyer_nickname: data.buyer_nickname,
                status: data.status,
                game_title_id: data.game_title_id,
                game_title: data.game_title,
                category_id: data.category_id,
                category: data.category,
                listing_title: data.listing_title,
                description: data.description.split('\n'),
                price: data.price,
                price_negotiation: data.price_negotiation,
                price_in_negotiation: inputPriceInNegotiation ? purchaseRequestRecord.price_in_negotiation : data.price_in_negotiation,
                fee_id: data.fee_id,
                fee_percentage: data.fee_percentage,
                enable_cancel: data.enable_cancel,
                enable_request_change_price: data.enable_request_change_price,
                enable_response_change_price: data.enable_response_change_price,
                enable_payment: data.enable_payment,
                enable_deliver: data.enable_deliver,
                enable_complete: data.enable_complete,
                enable_send_message: data.enable_send_message
            });
            setAvatarPicture(user_id == data.seller_id ? data.seller_profile_picture : data.buyer_profile_picture);
            setOtherName(user_id == data.seller_id ? data.seller_nickname : data.buyer_nickname);
        })
    }

    function getMessages() {
        setFetching(true);
        const user_id = localStorage.getItem('user_id');
        withTokenRequest.post('/getMessagesPurchaseRequest', {
            purchase_request_id: purchaseRequestId,
            user_id: user_id,
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
            const user_id = localStorage.getItem('user_id');
            setFetching(true);
            withTokenRequest.post('/getMessagesPurchaseRequest', {
                purchase_request_id: purchaseRequestId,
                user_id: user_id,
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
        withTokenRequest.post('/setReadMessagesPurchaseRequest', {
            purchase_request_id: purchaseRequestId,
            user_id: localStorage.getItem('user_id'),
            displayed_latest_id: id
        }, {
            headers: requestHeaders
        }).then((res) => {
        });
    }

    function requestChangePrice() {
        withTokenRequest.post('/requestChangePricePurchaseRequest', {
            purchase_request_id: purchaseRequestId,
            buyer_id: localStorage.getItem('user_id'),
            request_price: purchaseRequestRecord.price_in_negotiation
        }, {
            headers: requestHeaders
        }).then((res) => {
            setInputPriceInNegotiation(false);
            getPurchaseRequestDetail();
        });
    }

    function responseChangePrice(response) {
        withTokenRequest.post('/responseChangePricePurchaseRequest', {
            purchase_request_id: purchaseRequestId,
            seller_id: localStorage.getItem('user_id'),
            response: response
        }, {
            headers: requestHeaders
        }).then((res) => {
            getPurchaseRequestDetail();
        });
    }

    function payForPurchaseRequest() {
        withTokenRequest.post('payForPurchaseRequest', {
            purchase_request_id: purchaseRequestId,
            buyer_id: localStorage.getItem('user_id')
        }, {
            headers: requestHeaders
        }).then((res) => {
            getPurchaseRequestDetail();
        });
    }

    function deliverProductPurchaseRequest() {
        withTokenRequest.post('deliverProductPurchaseRequest', {
            purchase_request_id: purchaseRequestId,
            seller_id: localStorage.getItem('user_id')
        }, {
            headers: requestHeaders
        }).then((res) => {
            getPurchaseRequestDetail();
        });
    }

    function completeTransactionPurchaseRequest() {
        withTokenRequest.post('completeTransactionPurchaseRequest', {
            purchase_request_id: purchaseRequestId,
            buyer_id: localStorage.getItem('user_id')
        }, {
            headers: requestHeaders
        }).then((res) => {
            getPurchaseRequestDetail();
        });
    }

    function cancelTransactionPurchaseRequest() {
        withTokenRequest.post('cancelTransactionPurchaseRequest', {
            purchase_request_id: purchaseRequestId,
            user_id: localStorage.getItem('user_id')
        }, {
            headers: requestHeaders
        }).then((res) => {
            getPurchaseRequestDetail();
        });
    }

    function handleChange(e, newValue, setterName, setterParams) {
        const target = e.target;
        const value = target.value;
        const name = target.name;
        switch (setterName) {
            case 'setPriceInNegotiation':
                setInputPriceInNegotiation(true);
                setPurchaseRequestRecord({
                    ...purchaseRequestRecord,
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
        submitData.append('purchase_request_id', purchaseRequestId);
        submitData.append('sender_id', localStorage.getItem('user_id'));
        submitData.append('message', requestMessage);
        submitData.append('picture', pictureBlob);
        withTokenRequest.post('/sendMessagePurchaseRequest', submitData, {
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
        if (purchaseRequestRecord.enable_send_message) {
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
        withTokenRequest.post('/deleteMessagePurchaseRequest', {
            message_id: message,
            purchase_request_id: purchaseRequestId,
            sender_id: localStorage.getItem('user_id'),
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

    if (!purchaseRequestRecord) {
        return (
            <></>
        )
    }
    let fees = '';
    if (localStorage.getItem('user_id') == purchaseRequestRecord.seller_id) {
        fees = <>
            <TableRow>
               <TableCell style={keyColumnStyle}>Fee ({purchaseRequestRecord.fee_percentage * 100}%)</TableCell>
               <TableCell style={{fontWeight: 'bold', fontSize: '20px', color: 'red'}}>${purchaseRequestRecord.price * purchaseRequestRecord.fee_percentage}</TableCell>
            </TableRow>
            <TableRow>
               <TableCell style={keyColumnStyle}>Revenue</TableCell>
               <TableCell style={{fontWeight: 'bold', fontSize: '20px', color: 'red'}}>${purchaseRequestRecord.price - purchaseRequestRecord.price * purchaseRequestRecord.fee_percentage}</TableCell>
            </TableRow>
        </>
    }
    let payComponent = '';
    if (purchaseRequestRecord.enable_payment) {
        payComponent = <>
            <ConfirmDialog text='Payment' message='Are you sure you want to payment?' callback={payForPurchaseRequest}/>
            <br /><br />
        </>;
    }
    let deliverComponent = '';
    if (purchaseRequestRecord.enable_deliver) {
        deliverComponent = <>
            <ConfirmDialog text='Complete Deliver' message='Are you sure you have completed delivery?' callback={deliverProductPurchaseRequest}/>
            <br /><br />
        </>;
    }
    let completeComponent = '';
    if (purchaseRequestRecord.enable_complete) {
        completeComponent = <>
            <ConfirmDialog text='Complete Transaction' message='Are you sure you want to complete transaction?' callback={completeTransactionPurchaseRequest}/>
            <br /><br />
        </>;
    }
    let requestChangePriceComponent = '';
    if (purchaseRequestRecord.price_negotiation && purchaseRequestRecord.buyer_id == localStorage.getItem('user_id') && (purchaseRequestRecord.status == 0 || purchaseRequestRecord.status == 1)) {
        requestChangePriceComponent = <>
            {purchaseRequestRecord.status == 0 && !purchaseRequestRecord.enable_response_change_price ? <p>Pending Approval</p> : null}
            <div style={{display: 'flex'}}>
                <FormControl sx={{ width: 200 }} variant="standard">
                    <InputLabel htmlFor="standard-adornment-price">Request Price</InputLabel>
                    <Input
                        id="standard-adornment-price"
                        startAdornment={<InputAdornment position="start">$</InputAdornment>}
                        value={purchaseRequestRecord.price_in_negotiation}
                        onChange={(event, newValue) => {handleChange(event, newValue, 'setPriceInNegotiation', null);}}
                        disabled={!purchaseRequestRecord.enable_request_change_price}
                    />
                </FormControl>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <Button variant="contained" disabled={!purchaseRequestRecord.enable_request_change_price} onClick={requestChangePrice}>Request</Button>
            </div><br /><br />
        </>
    }
    let responseChangePriceComponent = '';
    if (purchaseRequestRecord.enable_response_change_price) {
        responseChangePriceComponent = <>
            <p style={{'font-weight': 'bold'}}>Request Price: &nbsp;<span style={{'color': 'red'}}>${purchaseRequestRecord.price_in_negotiation}</span></p>
            <div style={{display: 'flex'}}>
            <Button variant="contained" onClick={() => responseChangePrice(true)}>Accept</Button>&nbsp;&nbsp;
            <Button variant="contained" onClick={() => responseChangePrice(false)}>Reject</Button>
            </div>
        </>;
    }
    let cancelComponent = '';
    if (purchaseRequestRecord.enable_cancel) {
        cancelComponent = <>
            <ConfirmDialog text='Cancel Transaction' message='Are you sure you want to cancel transaction?' callback={cancelTransactionPurchaseRequest}/>
            <br /><br />
        </>;
    }
    if (!purchaseRequestId) {
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
                    <h2 style={{backGroundColor: 'blue'}}>{purchaseRequestRecord.listing_title}</h2><br />
                    <div style={{fontWeight: 'bold', backgroundColor: 'black', color: 'white', width: '70%', height: '25px'}}>Description of product</div><br />
                    {purchaseRequestRecord.description.map((line, index) => (
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
                                    <TableCell>{purchaseRequestRecord.game_title}</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell style={keyColumnStyle}>Category</TableCell>
                                    <TableCell>{purchaseRequestRecord.category}</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell style={keyColumnStyle}>Price</TableCell>
                                    <TableCell style={{fontWeight: 'bold', fontSize: '20px', color: 'red'}}>${purchaseRequestRecord.price}</TableCell>
                                </TableRow>
                                {fees}
                                <TableRow>
                                    <TableCell style={keyColumnStyle}>Price Negotiation</TableCell>
                                    <TableCell>{purchaseRequestRecord.price_negotiation ? 'OK' : 'NG'}</TableCell>
                                </TableRow>
    
                            </TableBody>
                        </Table>
                    </TableContainer>
                    <br /><br />
                    <div style={{fontWeight: 'bold'}}>Seller</div><br />
                    <div style={{border: '1px solid black', height: '50px', width: '40%', display: 'flex'}}>
                        <img src={`data:image/jpeg;base64,${purchaseRequestRecord.seller_profile_picture}`} style={profilePictureStyle}></img>
                        <div style={{fontWeight: 'bold'}}>&nbsp;{purchaseRequestRecord.seller_nickname}</div>
                    </div><br />
                    <div style={{fontWeight: 'bold'}}>Buyer</div><br />
                    <div style={{border: '1px solid black', height: '50px', width: '40%', display: 'flex'}}>
                        <img src={`data:image/jpeg;base64,${purchaseRequestRecord.buyer_profile_picture}`} style={profilePictureStyle}></img>
                        <div style={{fontWeight: 'bold'}}>&nbsp;{purchaseRequestRecord.buyer_nickname}</div>
                    </div><br /><br />
                    {payComponent}
                    {deliverComponent}
                    {completeComponent}
                    {requestChangePriceComponent}
                    {responseChangePriceComponent}
                    {cancelComponent}
                </div>

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

export default TransactionChatListing;