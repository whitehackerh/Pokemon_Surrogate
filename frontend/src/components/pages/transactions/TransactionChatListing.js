import { useRef, useState, useEffect } from "react";
import { useNavigate, useLocation } from 'react-router-dom';
import { withTokenRequest, requestHeaders } from '../../../http';
import Button from "@mui/material/Button";
import CustomSlider from "../../modules/CustomSlider/CustomSlider";
import { Table, TableBody, TableCell, TableRow, TableContainer, Paper } from '@mui/material';
import ConfirmDialog from "../../modules/dialogs/ConfirmDialog";
import FormControl from '@mui/material/FormControl';
import InputAdornment from '@mui/material/InputAdornment';
import Input from '@mui/material/Input';
import InputLabel from '@mui/material/InputLabel';
import useInterval from 'use-interval';

const TransactionChatListing = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const purchaseRequestId = location.state.purchaseRequestId;
    const [pictures, setPictures] = useState([]);
    const [purchaseRequestRecord, setPurchaseRequestRecord] = useState(null);
    const [inputPriceInNegotiation, setInputPriceInNegotiation] = useState(false);
    requestHeaders.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;

    useEffect(() => {
        if (purchaseRequestId) {
            getPurchaseRequestDetail();
        }
    }, []);

    useInterval(() => {
        getPurchaseRequestDetail();
    }, 5000);

    function getPurchaseRequestDetail() {
        withTokenRequest.post('/getPurchaseRequestDetail', {
            purchase_request_id: purchaseRequestId,
            user_id: localStorage.getItem('user_id')
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
                enable_complete: data.enable_complete
            });
        })
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

    const mainContents = {
        float: 'left',
        margin: '10px',
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
            </div>
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
    if (!purchaseRequestId) {
        return <></>;
    }
    return (
        <>
            <div style={mainContents}>
                <div style={sliderStyle}>
                    <CustomSlider>
                        {pictures.map((picture, index) => {
                            return <img key={index} src={`data:image/jpeg;base64,${picture}`}/>;
                        })}
                    </CustomSlider>
                </div>
                <br /><br />
                <h2 style={{backGroundColor: 'blue'}}>{purchaseRequestRecord.listing_title}</h2><br />
                <div style={{fontWeight: 'bold', backgroundColor: 'black', color: 'white', width: '40%', height: '25px'}}>Description of product</div><br />
                {purchaseRequestRecord.description.map((line, index) => (
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
                <div style={{border: '1px solid black', height: '50px', width: '30%', display: 'flex'}}>
                    <img src={`data:image/jpeg;base64,${purchaseRequestRecord.seller_profile_picture}`} style={profilePictureStyle}></img>
                    <div style={{fontWeight: 'bold'}}>&nbsp;{purchaseRequestRecord.seller_nickname}</div>
                </div><br />
                <div style={{fontWeight: 'bold'}}>Buyer</div><br />
                <div style={{border: '1px solid black', height: '50px', width: '30%', display: 'flex'}}>
                    <img src={`data:image/jpeg;base64,${purchaseRequestRecord.buyer_profile_picture}`} style={profilePictureStyle}></img>
                    <div style={{fontWeight: 'bold'}}>&nbsp;{purchaseRequestRecord.buyer_nickname}</div>
                </div><br /><br />
                {payComponent}
                {requestChangePriceComponent}
                {responseChangePriceComponent}
            </div>
        </>
    )
}

export default TransactionChatListing;