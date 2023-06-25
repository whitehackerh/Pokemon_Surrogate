import React, { useRef, useState, useEffect } from "react";
import SideBar_AccountSettings from './SideBar_AccountSettings'; 
import { withTokenRequest, requestHeaders } from '../../../http';
import Uploady from "@rpldy/uploady";
import UploadButton from "@rpldy/upload-button";
import UploadPreview from "@rpldy/upload-preview";
import "../../modules/crop/Crop.css";
import "../../modules/crop/CropImage";
import { ItemPreviewWithCrop } from "../../modules/crop/CropImage";
import Button from "@mui/material/Button";

const ProfilePictureSettings = () => {
    const previewMethodsRef = useRef();
    const [pictureBase64, setPictureBase64] = useState(null)
    const [defaultPicture, setDefaultPicture] = useState(true);
    requestHeaders.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;

    useEffect(() => {
        getProfilePicture();
    }, []);

    function getProfilePicture() {
        withTokenRequest.post('/getProfilePicture', {
            id: localStorage.getItem('user_id')
        }, {
            headers: requestHeaders
        }).then((res) => {
            setPictureBase64(res.data.data.picture);
            setDefaultPicture(res.data.data.default);
        })
    }

    function deleteProfilePicture() {
        withTokenRequest.post('/setProfilePicture', {
            id: localStorage.getItem('user_id'),
            delete: true
        }, {
            headers: requestHeaders
        }).then((res) => {
            getProfilePicture();
        })
    }

    /** css */
    const mainContents = {
        float: 'left',
        margin: '10px',
        'text-align': 'center',
        width: 'calc(100% - 362px)'
    }

    const profilePictureSettings = {
        margin: '10px',
        'text-align': 'center',
    }

    const croppedStyle = {
        width: '250px',
        height: '250px',
        cursor: 'pointer'
    }

    const deleteButtonStyle = {
        'margin-left': '50px'
    }

    return (
        <>
            <SideBar_AccountSettings />
            <div style={mainContents}>
                <h2>Profile Picture</h2>
                <Uploady
                    multiple={false}
                >
                    <div className="profilePicture" style={profilePictureSettings}>
                        <img src={`data:image/jpeg;base64,${pictureBase64}`} alt="picture" style={croppedStyle}>
                        </img><br></br>
                        <UploadButton className="MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium css-sghohy-MuiButtonBase-root-MuiButton-root">SETTINGS</UploadButton>
                        <Button variant="contained" style={deleteButtonStyle} onClick={() => deleteProfilePicture()} disabled={defaultPicture}>DELETE</Button>
                        <br />
                        <UploadPreview
                            PreviewComponent={ItemPreviewWithCrop}
                            previewComponentProps={{ 
                                previewMethods: previewMethodsRef, aspectProps: 1 / 1, api: 'setProfilePicture', 
                                aspectControllButtonsVisible: false, inputTextVisible: false,
                                distinctiveParam: {distinctiveFunc: getProfilePicture}
                            }}
                            previewMethodsRef={previewMethodsRef}
                        />
                    </div>
                </Uploady>
            </div>
        </>
    );
}

export default ProfilePictureSettings;