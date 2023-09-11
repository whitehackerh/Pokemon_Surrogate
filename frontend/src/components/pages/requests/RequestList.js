import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { noTokenRequest } from '../../../http';
import Box from '@mui/material/Box';
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';

const RequestList = () => {
    const navigate = useNavigate();
    const [totalPages, setTotalPages] = useState(1);
    const [page, setPage] = useState(1);
    const [requests, setRequests] = useState(null);

    useEffect(() => {
        loadRequests(1);
    }, []);

    function loadRequests(page) {
        getRequestsSummary();
        getRequests(page);
    }

    function getRequestsSummary() {
        noTokenRequest.post('/getRequestsSummary', {
            status: null
        }).then((res) => {
            setTotalPages(res.data.data.pages);
        });
    }

    function getRequests(page) {
        noTokenRequest.post('/getRequests', {
            page: page,
            status: null
        }).then((res) => {
            setRequests(res.data.data.requests);
        });
    }

    function movePage(event, value) {
        setPage(value);
        setRequests(null);
        loadRequests(value);
    }

    const clickRequest = (requestId) => {
        navigate('/requestDetail', { state: {requestId: requestId, from: 'requestList'}});
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

    const requestList = (requests) => (
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

    if (requests === null) {
        return <></>;
    }

    return (
        <>
            <div style={mainContents}>
                <h2>Now On Sale</h2>
                <Box>
                    <br /><br />
                    {requestList(requests)}
                </Box>
                <br /><br />
                <Stack spacing={2}>
                    <Pagination count={totalPages} page={page} onChange={movePage} color="primary" />
                </Stack>
            </div>
        </>
    )
}

export default RequestList;