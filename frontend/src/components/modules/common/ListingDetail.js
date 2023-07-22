import React, { useRef, useState, useEffect } from "react";
import { useNavigate, useLocation } from 'react-router-dom';
import { noTokenRequest, withTokenRequest, requestHeaders } from '../../../http';
import Button from "@mui/material/Button";
import SideBar_Transactions from '../../pages/transactions/SideBar_Transactions';
import CustomSlider from "../CustomSlider/CustomSlider";
import { Table, TableBody, TableCell, TableRow, TableContainer, Paper } from '@mui/material';

const ListingDetail = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const listingId = location.state.listingId;
    const from = location.state.from;
    const [pictures, setPictures] = useState([]);
    const [record, setRecord] = useState(null);

    useEffect(() => {
        getListingDetail();
    }, []);

    function getListingDetail() {
        noTokenRequest.post('/getListingDetail', {
            listing_id: listingId,
            user_id: localStorage.getItem('user_id') ? localStorage.getItem('user_id') : null
        }).then((res) => {
            const data = res.data.data;
            setPictures(data.pictures);       
            setRecord({
                seller_id: data.seller_id,
                profile_picture: data.sellers_profile_picture,
                nickname: data.nickname,
                status: data.status,
                edit_available: data.edit_available,
                enable_purchase: data.enable_purchase,
                game_title_id: data.game_title_id,
                game_title: data.game_title,
                category_id: data.category_id,
                category: data.category,
                listing_title: data.listing_title,
                description: data.description.split('\n'),
                price_negotiation: data.price_negotiation,
                price: data.price,
                fee_id: data.fee_id,
                fee_percentage: data.fee_percentage
            });
        })
    }

    function clickEdit() {
        navigate('/editListing', { state: {listingId: listingId}});
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

    let sideBar = '';
    if (from == 'listingProducts') {
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
    if (record.edit_available) {
        buttons = <>
         {/* TODO Navigation */}
            <Button variant="contained" onClick={clickEdit}>Edit</Button>
        </>
    } else if (record.enable_purchase) {
        buttons = <>
        {/* TODO Navigation */}
            <Button variant="contained">Go to purchase procedure</Button>
        </>
    }
    let fees = '';
    if (localStorage.getItem('user_id') == record.seller_id) {
        fees = <>
            <TableRow>
               <TableCell style={keyColumnStyle}>Fee ({record.fee_percentage * 100}%)</TableCell>
               <TableCell style={{fontWeight: 'bold', fontSize: '20px', color: 'red'}}>${record.price * record.fee_percentage}</TableCell>
            </TableRow>
            <TableRow>
               <TableCell style={keyColumnStyle}>Revenue</TableCell>
               <TableCell style={{fontWeight: 'bold', fontSize: '20px', color: 'red'}}>${record.price - record.price * record.fee_percentage}</TableCell>
            </TableRow>
        </>
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
                <h2 style={{backGroundColor: 'blue'}}>{record.listing_title}</h2><br />
                <div style={{fontWeight: 'bold', backgroundColor: 'black', color: 'white', width: '40%', height: '25px'}}>Description of product</div><br />
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
                                <TableCell>{record.game_title}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell style={keyColumnStyle}>Category</TableCell>
                                <TableCell>{record.category}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell style={keyColumnStyle}>Price</TableCell>
                                <TableCell style={{fontWeight: 'bold', fontSize: '20px', color: 'red'}}>${record.price}</TableCell>
                            </TableRow>
                            {fees}
                            <TableRow>
                                <TableCell style={keyColumnStyle}>Price Negotiation</TableCell>
                                <TableCell>{record.price_negotiation ? 'OK' : 'NG'}</TableCell>
                            </TableRow>
 
                        </TableBody>
                    </Table>
                </TableContainer>
                <br /><br />
                <div style={{fontWeight: 'bold'}}>Seller</div><br />
                <div style={{border: '1px solid black', height: '50px', width: '30%', display: 'flex'}}>
                    <img src={`data:image/jpeg;base64,${record.profile_picture}`} style={profilePictureStyle}></img>
                    <div style={{fontWeight: 'bold'}}>&nbsp;{record.nickname}</div>
                </div><br />
                {buttons}
            </div>
        </>
    )
}

export default ListingDetail;