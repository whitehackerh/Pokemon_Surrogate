import SideBar_Transactions from './SideBar_Transactions';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { withTokenRequest, requestHeaders } from '../../../http';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';

const ListingProducts = () => {
  const navigate = useNavigate();
  const [tab, setTab] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [page, setPage] = useState(1);
  const [listingStatus, setListingStatus] = useState(0);
  const [listingsPersonal, setListingsPersonal] = useState(null);
  requestHeaders.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;

  useEffect(() => {
    loadListingsProductsNotTransaction(1, 0);
  }, []);

  function loadListingsProductsNotTransaction(page, status) {
    setListingStatus(status);
    getListingsPersonalSummary(status);
    getListingsPersonal(page, status);
  }
  function getListingsPersonalSummary(status) {
    withTokenRequest
      .post('/getListingsPersonalSummary', {
        seller_id: localStorage.getItem('user_id'),
        status: status,
      }, {
        headers: requestHeaders
      })
      .then((res) => {
        setTotalPages(res.data.data.pages);
      });
  }
  function getListingsPersonal(page, status) {
    withTokenRequest
      .post('/getListingsPersonal', {
        seller_id: localStorage.getItem('user_id'),
        page: page,
        status: status,
      }, {
        headers: requestHeaders
      })
      .then((res) => {
        setListingsPersonal(res.data.data.listings);
      });
  }

  function changeTab(event, value) {
    setTab(value);
    setListingsPersonal(null);
    if (value === 0) {
      loadListingsProductsNotTransaction(1, 0);
    } else if (value === 1) {
      loadListingsProductsNotTransaction(1, 2);
    }
  }

  function movePage(event, value) {
    setPage(value);
    setListingsPersonal(null);
    loadListingsProductsNotTransaction(value, listingStatus);
  }

  const clickListing = (listingId) => {
    navigate('/listingDetail', { state: {listingId: listingId, from: 'listingProducts'}})
  }

  const mainContents = {
    float: 'left',
    margin: '10px',
    // 'text-align': 'center',
    width: 'calc(100% - 362px)',
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

  const notTransactions = (listingsPersonal) => (
        <>
            {listingsPersonal.map((listing, index) => (
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

  if (listingsPersonal === null) {
    return <></>;
  }
  return (
    <>
      <SideBar_Transactions />
      <div style={mainContents}>
        <Tabs value={tab} onChange={changeTab}>
          <Tab label="Exhibiting" />
          <Tab label="End of Listing" />
        </Tabs>
        {tab === 0 && (
          <Box>
            <br /><br />
            {listingsPersonal ? (notTransactions(listingsPersonal)) : null}
          </Box>
        )}
        {tab === 1 && (
          <Box>
            <br /><br />
            {listingsPersonal ? (notTransactions(listingsPersonal)) : null}
          </Box>
        )}
        <br /><br />
        <Stack spacing={2}>
          <Pagination count={totalPages} page={page} onChange={movePage} color="primary" />
        </Stack>
      </div>
    </>
  );
};

export default ListingProducts;
