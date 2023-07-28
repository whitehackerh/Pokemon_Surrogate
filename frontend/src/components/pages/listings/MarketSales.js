import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { noTokenRequest } from '../../../http';
import Box from '@mui/material/Box';
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';

const MarketSales = () => {
    const navigate = useNavigate();
    const [totalPages, setTotalPages] = useState(1);
    const [page, setPage] = useState(1);
    const [listingsPublic, setListingsPublic] = useState(null);

    useEffect(() => {
        loadListingsPublic(1);
    }, []);

    function loadListingsPublic(page) {
        getListingsPublicSummary();
        getListingsPublic(page);
    }

    function getListingsPublicSummary() {
        noTokenRequest.post('/getListingsPublicSummary', { 
        }).then((res) => {
            setTotalPages(res.data.data.pages);
        });
    }

    function getListingsPublic(page) {
        noTokenRequest.post('/getListingsPublic', {
            page: page
        }).then((res) => {
            setListingsPublic(res.data.data.listings);
        });
    }

    function movePage(event, value) {
        setPage(value);
        setListingsPublic(null);
        loadListingsPublic(value);
    }

    const clickListing = (listingId) => {
        navigate('/listingDetail', { state: {listingId: listingId, from: 'marketSales'}});
    };

    const mainContents = {
        float: 'left',
        margin: '10px',
        marginLeft: '500px',
        // 'text-align': 'center',
        width: 'calc(100% - 362px)'
    };
    const parentFlameStyle = {
        outline: 'solid 1px #333',
        minHeight: '115px',
        display: 'flex',
        alignItems: 'center',
        margin: '10px',
        width: '60%',
        position: 'relative',
        cursor: 'pointer'
    };
    const childFlameStyle = {
      display: 'flex',
      alignItems: 'center',
      margin: '10px',
      position: 'relative',
      width: '100%'
    };
    const containerStyle = {
      display: 'flex',
      alignItems: 'center',
      marginRight: '10px',
    };
    const imageContainerStyle = {
      width: '125px',
      height: '115px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    };
    const pictureStyle = {
      width: '125px',
      height: 'auto',
      objectFit: 'contain'
    };
    const listingMainStyle = {
      marginLeft: '10px',
      alignSelf: 'flex-start'
    };
    const gameTitleStyle = {
      marginTop: '25px',
    }
    const priceStyle = {
      position: 'absolute',
      bottom: '10px',
      right: '10px',
      color: 'red',
      fontWeight: 'bold',
      fontSize: '25px',
      whiteSpace: 'nowrap'
    };

    const listingList = (listingsPublic) => (
        <>
            {listingsPublic.map((listing, index) => (
                <div key={listing.listing_id} style={parentFlameStyle}
                     onClick={() => clickListing(listing.listing_id)}>
                    <div style={childFlameStyle}>
                        <div style={containerStyle}>
                            <div style={imageContainerStyle}>
                                <img
                                src={`data:image/jpeg;base64,${listing.picture}`}
                                alt="picture"
                                style={pictureStyle}
                                ></img>
                            </div>
                        </div>
                        <div style={listingMainStyle}>
                            <h4 style={{ margin: 0 }}>{listing.listing_title}</h4>
                            <div style={gameTitleStyle}>
                                <h5 style={{ margin: 0 }}>{listing.game_title}</h5>
                            </div>
                        </div>
                        <div style={priceStyle}>${listing.price}</div>
                    </div>
                </div>
            ))}
        </>
    );

    if (listingsPublic === null) {
        return <></>;
    }

    return (
        <>
            <div style={mainContents}>
                <h2>Now On Sale</h2>
                <Box>
                    <br /><br />
                    {listingList(listingsPublic)}
                </Box>
                <br /><br />
                <Stack spacing={2}>
                    <Pagination count={totalPages} page={page} onChange={movePage} color="primary" />
                </Stack>
            </div>
        </>
    )
}

export default MarketSales;