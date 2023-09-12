import SideBar_Tradings from './SideBar_Transactions';
import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { noTokenRequest, withTokenRequest, requestHeaders, multipartFormData } from '../../../http';
import TextField from "@mui/material/TextField";
import Autocomplete from '@mui/material/Autocomplete';
import Button from "@mui/material/Button";
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import InputAdornment from '@mui/material/InputAdornment';
import Input from '@mui/material/Input';
import InputLabel from '@mui/material/InputLabel';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';

const EditRequest = () => {
    const location = useLocation();
    const requestId = location.state ? location.state.requestId : null;
    const navigate = useNavigate();
    const [pictures, setPictures] = useState([]);
    const [game_title, setGameTitle] = useState(null);
    const [category, setCategory] = useState(null);
    const [request_title, setRequestTitle] = useState(null);
    const [description, setDescription] = useState(null);
    const [min_price, setMinPrice] = useState(null);
    const [max_price, setMaxPrice] = useState(null);
    const [pageTitle, setPageTitle] = useState('New Request');
    const [registerButtonText, setRegisterButtonText] = useState('Register');
    const [gameTitles, setGameTitles] = useState(null);
    requestHeaders.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;
    multipartFormData.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;

    useEffect(() => {
        getGameTitles();
        if (requestId) {
            getRequestDetail();
        }
    }, []);

    function getGameTitles() {
        noTokenRequest.get('/getGameTitles', {
        }).then((res) => {
            setGameTitles(res.data.data.gameTitles);
        })
    }

    function getRequestDetail() {
        noTokenRequest.post('/getRequestDetail', {
            request_id: requestId,
        }).then((res) => {
            const data = res.data.data;
            if (!data.isDefaultPicture) {
                const pictureFiles = data.pictures.map(base64Data => {
                    const blob = dataURLtoBlob(base64Data);
                    const file = new File([blob], 'picture.png', { type: 'image/png' });
                    const dataUrl = URL.createObjectURL(file);
                    return { file, url: dataUrl };
                });
                setPictures(pictureFiles);
            }
            setGameTitle({ id: data.game.id, title: data.game.title });
            setCategory(data.category.id);
            setRequestTitle(data.request_title);
            setDescription(data.description);
            setMinPrice(data.min_price);
            setMaxPrice(data.max_price);
            setPageTitle('Edit Request');
            setRegisterButtonText('Update');
        })
    }

    function dataURLtoBlob(base64Data) {
        const byteString = atob(base64Data);
        const arrayBuffer = new ArrayBuffer(byteString.length);
        const uint8Array = new Uint8Array(arrayBuffer);
        for (let i = 0; i < byteString.length; i++) {
          uint8Array[i] = byteString.charCodeAt(i);
        }
        return new Blob([uint8Array], { type: 'image/png' });
    }

    const handlePictureUpload = (event) => {
        const selectedFiles = Array.from(event.target.files);
        const maxPictures = 10 - pictures.length;
        const filesToUpload = selectedFiles.slice(0, maxPictures);
        const uploadedPictures = filesToUpload.map((file) => ({
            file,
            url: URL.createObjectURL(file)
        }));
        setPictures((prevPictures) => [...prevPictures, ...uploadedPictures]);
    }

    const handlePictureRemove = (index) => {
        setPictures((prevPictures) => {
            const updatedPictures = [...prevPictures];
            updatedPictures.splice(index, 1);
            return updatedPictures;
        })
    }

    function handleChange(e, newValue, setterName, setterParams) {
        const target = e.target;
        const value = target.value;
        const name = target.name;
        switch (setterName) {
            case 'setGameTitle':
                setGameTitle({
                    ...game_title,
                    id: newValue ? newValue.id : null,
                    title: newValue ? newValue.title: ''
                });
                break;
            case 'setCategory':
                setCategory(newValue);
                break;
            case 'setRequestTitle':
                setRequestTitle(value);
                break;
            case 'setDescription':
                setDescription(value);
                break;
            case 'setMinPrice':
                setMinPrice(value)
                break;
            case 'setMaxPrice':
                setMaxPrice(value)
                break;
            default:
                break;
        }
    }

    function setRequest() {
        const formData = new FormData();
        pictures.forEach((picture, index) => {
            formData.append(`picture${index + 1}`, picture.file);
        })
        formData.append('request_id', requestId ? requestId : '');
        formData.append('game_title_id', game_title.id);
        formData.append('category', category);
        formData.append('request_title', request_title);
        formData.append('description', description);
        formData.append('min_price', min_price);
        formData.append('max_price', max_price);
        withTokenRequest.post('/setRequest', formData,
            {
                headers: multipartFormData
            }).then(() => {
                navigate('/requests');
            }).catch((error) => {
                console.log(error);
            })
    }

    if (gameTitles == null) {
        return (
            <></>
        );
    }

    const mainContents = {
        float: 'left',
        margin: '10px',
        // 'text-align': 'center',
        width: 'calc(100% - 362px)'
    }

    return (
        <div>
            <SideBar_Tradings />
            <div style={mainContents}>
                <h2>{pageTitle}</h2>
                <div>
                <label htmlFor="upload-input">
                    <input
                    id="upload-input"
                    type="file"
                    accept="image/*"
                    multiple
                    onChange={handlePictureUpload}
                    style={{ display: 'none' }}
                    />
                    <Button variant="contained" component="span">
                    Select File
                    </Button>
                </label><br /><br />
                    <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                        {pictures.map((picture, index) => (
                            <div key={index} style={{ position: 'relative', flexBasis: '20%', margin: '10px' }}>
                                <img src={picture.url} alt={`Picture ${index + 1}`} style={{ width: '100%', height: 'auto' }} />
                                <IconButton
                                    onClick={() => handlePictureRemove(index)}
                                    style={{
                                        position: 'absolute',
                                        top: '5px',
                                        right: '5px',
                                        backgroundColor: 'red',
                                        color: 'white',
                                    }}
                                >
                                    <DeleteIcon />
                                </IconButton>
                            </div>
                        ))}
                    </div>
                </div><br /><br />
                <Autocomplete
                    id="gameTitle"
                    value={game_title}
                    options={gameTitles}
                    getOptionLabel={(option) => option.title}
                    sx={{ width: 450 }}
                    renderInput={(params) => <TextField {...params} label='Game Title' />}
                    onChange={(event, newValue) => {handleChange(event, newValue, 'setGameTitle', null);}}
                    getOptionSelected={(option, value) => option.id === value.id}
                />
                <br /><br />
                <FormControl component='fieldset'>
                    <FormLabel component='legend'>Category</FormLabel>
                    <RadioGroup value={category} onChange={(event, newValue) => {handleChange(event, newValue, 'setCategory', null);}} row>
                        <FormControlLabel 
                            value='1'
                            control={<Radio />}
                            label='Pokémon'
                        />
                        <FormControlLabel 
                            value='2'
                            control={<Radio />}
                            label='Items'
                        />
                        <FormControlLabel 
                            value='3'
                            control={<Radio />}
                            label='Save Data'
                        />
                        <FormControlLabel 
                            value='4'
                            control={<Radio />}
                            label='Boosting'
                        />
                    </RadioGroup>
                </FormControl><br /><br />
                <TextField 
                    id='outlined-basic'
                    label='Request Title'
                    variant='outlined'
                    name="request_title"
                    value={request_title}
                    onChange={(event, newValue) => {handleChange(event, newValue, 'setRequestTitle', null);}}
                    sx={{ width: 1000 }}/><br /><br />
                <TextField 
                    multiline
                    maxRows={10}
                    rows={5}
                    label='Description'
                    name="description"
                    value={description}
                    onChange={(event, newValue) => {handleChange(event, newValue, 'setDescription', null);}}
                    sx={{ width: 1000 }}
                /><br /><br />
                <FormControl sx={{ width: 200 }} variant="standard">
                    <InputLabel htmlFor="standard-adornment-price">Min Price</InputLabel>
                    <Input
                        id="standard-adornment-price"
                        startAdornment={<InputAdornment position="start">$</InputAdornment>}
                        value={min_price}
                        onChange={(event, newValue) => {handleChange(event, newValue, 'setMinPrice', null);}}
                    />
                </FormControl><br /><br />
                <FormControl sx={{ width: 200 }} variant="standard">
                    <InputLabel htmlFor="standard-adornment-price">Max Price</InputLabel>
                    <Input
                        id="standard-adornment-price"
                        startAdornment={<InputAdornment position="start">$</InputAdornment>}
                        value={max_price}
                        onChange={(event, newValue) => {handleChange(event, newValue, 'setMaxPrice', null);}}
                    />
                </FormControl><br /><br />
                <br /><br /><br /><br />
                <Button variant="contained" onClick={setRequest}>{registerButtonText}</Button>
            </div>
        </div>
    );
}

export default EditRequest;