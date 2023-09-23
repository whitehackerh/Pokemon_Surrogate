import SideBar_Transactions from './SideBar_Transactions';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { withTokenRequest, requestHeaders } from '../../../http';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';

const Accepts = () => {
    const navigate = useNavigate();
    const [tab, setTab] = useState(0);
    const [totalPages, setTotalPages] = useState(1);
    const [page, setPage] = useState(1);
    const [acceptStatus, setAcceptStatus] = useState(null);
    const [accepts, setAccepts] = useState(null);
    requestHeaders.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;

    useEffect(() => {
        loadAccepts(1, 0);
    }, []);

    function loadAccepts(page, status) {
        setAcceptStatus(status);
        getAcceptsSummary(status);
        getAccepts(page, status);
    }
    function getAcceptsSummary(status) {
        withTokenRequest.post('/getAcceptsSummary', {
          status: status,
          client: false
        }, {
          headers: requestHeaders
        })
        .then((res) => {
          setTotalPages(res.data.data.pages);
        });
    }
    function getAccepts(page, status) {
        withTokenRequest.post('/getAccepts', {
          status: status,
          client: false,
          page: page
        }, {
          headers: requestHeaders
        })
        .then((res) => {
          setAccepts(res.data.data.accepts);
        });
    }

    function changeTab(event, value) {
        setTab(value);
        setPage(1);
        setAccepts(null);
        if (value === 0) {
            loadAccepts(1, 0);
        } else if (value == 1) {
            loadAccepts(1, 4);
        }
    }

    function movePage(event, value) {
        setPage(value);
        setAccepts(null);
        loadAccepts(value, acceptStatus);
    }

    const clickAccept = (acceptId) => {
        navigate('/transactionChatRequest', { state: {acceptId: acceptId}});
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
    const acceptMainStyle = {
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

    const transactions = (accepts) => (
        <>
          {accepts.map((accept, index) => (
              <div key={accept.accept_id} style={parentFlameStyle}
                  onClick={() => clickAccept(accept.accept_id)}>
                  <div style={childFlameStyle}>
                      <div style={containerStyle}>
                          <div style={imageContainerStyle}>
                              <img
                                src={`data:image/jpeg;base64,${accept.picture}`}
                                alt="picture"
                                style={pictureStyle}
                              ></img>
                          </div>
                      </div>
                      <div style={acceptMainStyle}>
                          <h4 style={{ margin: 0 }}>{accept.request_title}</h4>
                          <div style={gameTitleStyle}>
                              <h5 style={{ margin: 0 }}>{accept.game_title}</h5>
                          </div>
                      </div>
                      <div style={priceStyle}>
                        {accept.price ? (
                          `$${accept.price}`
                        ) : (
                          `$${accept.min_price} - $${accept.max_price}`
                        )}
                      </div>
                  </div>
              </div>
            ))}
        </>
      );

    if (acceptStatus != null && !accepts) {
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
                {accepts ? (transactions(accepts)) : null}
              </Box>
            )}
            {tab === 1 && (
              <Box>
                <br /><br />
                {accepts ? (transactions(accepts)) : null}
              </Box>
            )}
            <br /><br />
            <Stack spacing={2}>
              <Pagination count={totalPages} page={page} onChange={movePage} color="primary" />
            </Stack>
          </div>
        </>
      );
}

export default Accepts;