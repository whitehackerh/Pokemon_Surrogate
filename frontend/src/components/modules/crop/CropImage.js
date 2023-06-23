import React, { useState, useCallback } from "react";
import styled from "styled-components";
import Cropper from "react-easy-crop";
import getCroppedImg from "./CropUtils";
import "./Crop.css";
import { withTokenRequest, multipartFormData } from '../../../http';
import { createImage } from "./CropUtils";
import { PREVIEW_TYPES } from "@rpldy/upload-preview";
import {
    withRequestPreSendUpdate,
    useItemFinalizeListener,
    useItemProgressListener
} from "@rpldy/uploady";
import Button from "@mui/material/Button";

    const PreviewImage = styled.img`
        margin: 5px;
        max-width: 200px;
        height: auto;
        max-height: 200px;
    `;

    const ButtonsWrapper = styled.div`
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 10px;
        position: absolute;
        top: 0;
        right: 0;
    `;

    const PreviewButtons = ({
        finished,
        crop,
        updateRequest,
        onUploadCancel,
        onUploadCrop
    }) => {
        return (
            <ButtonsWrapper>
            <Button
                variant="contained"
                style={{
                display: !finished && updateRequest && crop ? "block" : "none",
                'margin-right': '10px'
                }}
                onClick={onUploadCrop}
            >
                Upload
            </Button>
            <Button
                variant="contained"
                style={{
                display: !finished && updateRequest && crop ? "block" : "none",
                'margin-top': '10px',
                'margin-right': '10px'
                }}
                onClick={onUploadCancel}
            >
                Cancel
            </Button>
            </ButtonsWrapper>
        );
    };

    const UPLOAD_STATES = {
        NONE: 0,
        UPLOADING: 1,
        FINISHED: 2
    };

    /* API REQUEST */
    function SetProfilePicture(croppedPicture, multipartFormDataParam, callback) {
        const submitData = new FormData();
        submitData.append("id", localStorage.getItem('user_id'));
        submitData.append("delete", false);
        submitData.append("picture", croppedPicture);
        console.log(croppedPicture);
        withTokenRequest.post('/setProfilePicture', submitData,
            {
                headers: multipartFormDataParam
            })
            .then(() => {
                callback();
            })
            .catch((error) => {
                console.log(error);
            });
    }

    export const ItemPreviewWithCrop = withRequestPreSendUpdate((props) => {
        const {
        id,
        url,
        isFallback,
        type,
        updateRequest,
        requestData,
        previewMethods,
        aspectProps,
        api,
        aspectControllButtonsVisible,
        inputTextVisible,
        distinctiveParam
        } = props;
        multipartFormData.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;
        const [uploadState, setUploadState] = useState(UPLOAD_STATES.NONE);
        const [croppedImg, setCroppedImg] = useState(null);
        const [values, setValues] = useState(null);
        const [aspect, setAspect] = useState(aspectProps);
    
        //data for react-easy-crop
        const [crop, setCrop] = useState({ x: 0, y: 0 });
        const [zoom, setZoom] = useState(1);
        const [croppedAreaPixels, setCroppedAreaPixels] = useState(null);
        console.log(requestData);
        const onCropComplete = useCallback((croppedArea, croppedAreaPixels) => {
        // console.log(croppedArea, croppedAreaPixels);
        setCroppedAreaPixels(croppedAreaPixels);
        }, []);

        function handleChange(e) {
            const target = e.target;
            const value = target.value;
            const name = target.name;
            setValues({ ...values, [name]: value });
        }
    
        const isFinished = uploadState === UPLOAD_STATES.FINISHED;
    
        useItemProgressListener(() => setUploadState(UPLOAD_STATES.UPLOADING), id);
        useItemFinalizeListener(() => setUploadState(UPLOAD_STATES.FINISHED), id);
    
        const onUploadCrop = useCallback(async () => {
        if (updateRequest && croppedAreaPixels) {
            const [croppedBlob, croppedUri] = await getCroppedImg(
            url,
            croppedAreaPixels
            );
            requestData.items[0].file = croppedBlob;
            
            const originalPicture = await createImage(url);
            const originalPictureSize = {
                width: originalPicture.width,
                height: originalPicture.height,
                x: 0,
                y: 0
            };
            const [originalBlob, originalUri] = await getCroppedImg(url, originalPictureSize);
    
            updateRequest({ items: requestData.items });

            switch (api) {
                case 'setProfilePicture':
                    SetProfilePicture(requestData.items[0].file, multipartFormData, distinctiveParam.distinctiveFunc);
                    break;
                default:
                    break;
            }
            //setCroppedImg(croppedUri);
        }
        }, [url, requestData, updateRequest, croppedAreaPixels]);
    
        const onUploadCancel = useCallback(() => {
            updateRequest(false);
            if (previewMethods.current?.clear) {
                previewMethods.current.clear();
            }
        }, [updateRequest, previewMethods]);
    
        return isFallback || type !== PREVIEW_TYPES.IMAGE ? (
        null
        ) : (
        <>
            {requestData && uploadState === UPLOAD_STATES.NONE ? (
            <div className="crop-view">
                <div className="crop-container">
                <Cropper
                    image={url}
                    crop={crop}
                    zoom={zoom}
                    aspect={aspect}
                    onCropChange={setCrop}
                    onCropComplete={onCropComplete}
                    onZoomChange={setZoom}
                />
                </div>
                <div className="aspectControll" style={{ position: 'absolute', display: aspectControllButtonsVisible ? '' : 'none' }}>
                    <button onClick={() => setAspect(1/1)}>Square</button>
                    <button onClick={() => setAspect(5/4)}>Portrait</button>
                    <button onClick={() => setAspect(1/1.91)}>Landscape</button>
                </div>
                <div className="inputText" style={{ position: 'absolute', display: inputTextVisible ? '' : 'none' }}>
                    <textarea onChange={handleChange}></textarea>
                </div>
                <div className="controls">
                <input
                    type="range"
                    value={zoom}
                    min={1}
                    max={3}
                    step={0.1}
                    aria-labelledby="Zoom"
                    onChange={(e) => {
                    setZoom(e.target.value);
                    }}
                    className="zoom-range"
                />
                </div>
            </div>
            ) : (
            null
            )}
            <PreviewButtons
            finished={isFinished}
            crop={crop}
            updateRequest={updateRequest}
            onUploadCancel={onUploadCancel}
            onUploadCrop={onUploadCrop}
            />
        </>
        );
    });
