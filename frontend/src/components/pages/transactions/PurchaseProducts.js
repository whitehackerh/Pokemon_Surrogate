import SideBar_Transactions from './SideBar_Transactions';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { withTokenRequest, requestHeaders } from '../../../http';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';

const PurchaseProducts = () => {
    const navigate = useNavigate();
    const [tab, setTab] = useState(0);
    const [totalPages, setTotalPages] = useState(1);
    const [page, setPage] = useState(1);
    const [purchaseRequestStatus, setPurchaseRequestStatus] = useState(null);
    const [purchaseRequests, setPurchaseRequests] = useState(null);
    requestHeaders.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;

    useEffect(() => {
        loadListingsProductsTransaction(1, 0);
    }, []);

    function loadListingsProductsTransaction(page, status) {
        setPurchaseRequestStatus(status);
        getPurchaseRequestsSummary(status);
        getPurchaseRequests(page, status);
    }
    function getPurchaseRequestsSummary(status) {
        withTokenRequest.post('/getPurchaseRequestsSummary', {
          status: status,
          seller_id: null,
          buyer_id: localStorage.getItem('user_id')
        }, {
          headers: requestHeaders
        })
        .then((res) => {
          setTotalPages(res.data.data.pages);
        });
    }
    function getPurchaseRequests(page, status) {
        withTokenRequest.post('/getPurchaseRequests', {
          status: status,
          seller_id: null,
          buyer_id: localStorage.getItem('user_id'),
          page: page
        }, {
          headers: requestHeaders
        })
        .then((res) => {
          setPurchaseRequests(res.data.data.purchaseRequests);
        });
    }

    function changeTab(event, value) {
        setTab(value);
        setPage(1);
        setPurchaseRequests(null);
        if (value === 0) {
            loadListingsProductsTransaction(1, 0);
        } else if (value == 1) {
            loadListingsProductsTransaction(1, 3);
        }
    }

    function movePage(event, value) {
        setPage(value);
        setPurchaseRequests(null);
        loadListingsProductsTransaction(value, purchaseRequestStatus);
    }

    const clickPurchaseRequest = (purchaseRequestId) => {
        // TODO Navigate
        navigate('/home');
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

    const transactions = (purchaseRequests) => (
        <>
          {purchaseRequests.map((purchaseRequest, index) => (
            <div key={purchaseRequest.purchase_request_id} style={parentFlameStyle}
                 onClick={() => clickPurchaseRequest(purchaseRequest.purchase_request_id)}>
                <div style={childFlameStyle}>
                    <div style={containerStyle}>
                        <div style={imageContainerStyle}>
                            <img
                              src={`data:image/jpeg;base64,${purchaseRequest.picture}`}
                              alt="picture"
                              style={pictureStyle}
                            ></img>
                        </div>
                    </div>
                    <div style={listingMainStyle}>
                        <h4 style={{ margin: 0 }}>{purchaseRequest.listing_title}</h4>
                        <div style={gameTitleStyle}>
                            <h5 style={{ margin: 0 }}>{purchaseRequest.game_title}</h5>
                        </div>
                    </div>
                    <div style={priceStyle}>${purchaseRequest.price}</div>
                </div>
            </div>
          ))}
        </>
    );

    if (purchaseRequestStatus != null && !purchaseRequests) {
        return <></>;
    }
    return (
        <>
          <SideBar_Transactions />
          <div style={mainContents}>
            <Tabs value={tab} onChange={changeTab}>
              <Tab label='During Trading' />
              <Tab label='Completion / Cancel' />
            </Tabs>
            {tab === 0 && (
              <Box>
                <br /><br />
                {purchaseRequests ? (transactions(purchaseRequests)) : null}
              </Box>
            )}
            {tab === 1 && (
              <Box>
                <br /><br />
                {purchaseRequests ? (transactions(purchaseRequests)) : null}
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

export default PurchaseProducts;