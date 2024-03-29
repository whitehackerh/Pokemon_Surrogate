import SideBar_Transactions from './SideBar_Transactions';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { withTokenRequest, requestHeaders } from '../../../http';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';

const Requests = () => {
  const navigate = useNavigate();
  const [tab, setTab] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [page, setPage] = useState(1);
  const [requestStatus, setRequestStatus] = useState(0);
  const [requests, setRequests] = useState(null);
  const [acceptStatus, setAcceptStatus] = useState(null);
  const [accepts, setAccepts] = useState(null);
  requestHeaders.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;

  useEffect(() => {
    loadRequestsNotTransaction(1, 0);
  }, []);

  function loadRequestsNotTransaction(page, status) {
    setRequestStatus(status);
    getRequestsSummary(status);
    getRequests(page, status);
  }
  function getRequestsSummary(status) {
    withTokenRequest
      .post('/getRequestsSummary', {
        status: status,
      }, {
        headers: requestHeaders
      })
      .then((res) => {
        setTotalPages(res.data.data.pages);
      });
  }
  function getRequests(page, status) {
    withTokenRequest
      .post('/getRequests', {
        page: page,
        status: status,
      }, {
        headers: requestHeaders
      })
      .then((res) => {
        setRequests(res.data.data.requests);
      });
  }
  function loadAccepts(page, status) {
    setAcceptStatus(status);
    getAcceptsSummary(status);
    getAccepts(page, status);
  }
  function getAcceptsSummary(status) {
    withTokenRequest.post('/getAcceptsSummary', {
      status: status,
      client: true
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
      client: true,
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
    setRequests(null);
    setAccepts(null);
    if (value === 0) {
      setAcceptStatus(null);
      loadRequestsNotTransaction(1, 0);
    } else if (value == 1) {
      setRequestStatus(null);
      loadAccepts(1, 0);
    } else if (value == 2) {
      setRequestStatus(null);
      loadAccepts(1, 4);
    } else if (value === 3) {
      setAcceptStatus(null);
      loadRequestsNotTransaction(1, 2);
    }
  }

  function movePage(event, value) {
    setPage(value);
    setRequests(null);
    setAccepts(null);
    if (requestStatus != null) {
      loadRequestsNotTransaction(value, requestStatus);
    } else if (acceptStatus != null) {
      loadAccepts(value, acceptStatus);
    }
  }

  const clickRequest = (requestId) => {
    navigate('/requestDetail', { state: {requestId: requestId, from: 'requests'}});
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
  const requestMainStyle = {
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

  const notTransactions = (requests) => (
        <>
            {requests.map((request, index) => (
                <div key={request.request_id} style={parentFlameStyle}
                     onClick={() => clickRequest(request.request_id)}>
                    <div style={childFlameStyle}>
                        <div style={containerStyle}>
                            <div style={imageContainerStyle}>
                                <img
                                src={`data:image/jpeg;base64,${request.picture}`}
                                alt="picture"
                                style={pictureStyle}
                                ></img>
                            </div>
                        </div>
                        <div style={requestMainStyle}>
                            <h4 style={{ margin: 0 }}>{request.request_title}</h4>
                            <div style={gameTitleStyle}>
                                <h5 style={{ margin: 0 }}>{request.game_title}</h5>
                            </div>
                        </div>
                        <div style={priceStyle}>${request.min_price} - ${request.max_price}</div>
                    </div>
                </div>
            ))}
        </>
  );

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
                  <div style={requestMainStyle}>
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

  if ((requestStatus != null && !requests) || (acceptStatus != null && !accepts)) {
    return <></>;
  }
  return (
    <>
      <SideBar_Transactions />
      <div style={mainContents}>
        <Tabs value={tab} onChange={changeTab}>
          <Tab label="Accepting" />
          <Tab label='During Trading' />
          <Tab label='Completion / Cancel' />
          <Tab label="End of Request" />
        </Tabs>
        {tab === 0 && (
          <Box>
            <br /><br />
            {requests ? (notTransactions(requests)) : null}
          </Box>
        )}
        {tab === 1 && (
          <Box>
            <br /><br />
            {accepts ? (transactions(accepts)) : null}
          </Box>
        )}
        {tab === 2 && (
          <Box>
            <br /><br />
            {accepts ? (transactions(accepts)) : null}
          </Box>
        )}
        {tab === 3 && (
          <Box>
            <br /><br />
            {requests ? (notTransactions(requests)) : null}
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

export default Requests;
