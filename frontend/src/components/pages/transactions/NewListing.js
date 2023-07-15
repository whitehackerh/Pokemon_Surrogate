import SideBar_Tradings from './SideBar_Transactions';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
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
import Checkbox from '@mui/material/Checkbox';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';

const NewListing = () => {
    const navigate = useNavigate();
    const [pictures, setPictures] = useState([]);
    const [game_title, setGameTitle] = useState(null);
    const [category, setCategory] = useState(null);
    const [listing_title, setListingTitle] = useState(null);
    const [description, setDescription] = useState(null);
    const [price, setPrice] = useState(null);
    const [fee, setFee] = useState(null);
    const [revenue, setRevenue] = useState(null);
    const [price_negotiation_checked, setPriceNegotiationChecked] = useState(false);
    const [price_negotiation, setPriceNegotiation] = useState(0);
    const [gameTitles, setGameTitles] = useState(null);
    const [availableFee, setAvailableFee] = useState(null);
    requestHeaders.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;
    multipartFormData.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;

    useEffect(() => {
        getGameTitles();
        getAvailableFee();
    }, []);

    useEffect(() => {
        if (price) {
            setFee(price * availableFee.percentage);
        }
    }, [price]);

    useEffect(() => {
        if (price && fee) {
            setRevenue(price - (price * availableFee.percentage));
        }
    }, [price, fee]);

    useEffect(() => {
        setPriceNegotiation(price_negotiation_checked ? 1 : 0);
    }, [price_negotiation_checked]);

    function getGameTitles() {
        noTokenRequest.get('/getGameTitles', {
        }).then((res) => {
            setGameTitles(res.data.data.gameTitles);
        })
    }

    function getAvailableFee() {
        noTokenRequest.get('/getAvailableFee', {
        }).then((res) => {
            setAvailableFee(res.data.data);
        })
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
            case 'setListingTitle':
                setListingTitle(value);
                break;
            case 'setDescription':
                setDescription(value);
                break;
            case 'setPrice':
                setPrice(value)
                break;
            case 'setPriceNegotiationChecked':
                setPriceNegotiationChecked(newValue);
                break;
        }
    }

    function setListing() {
        let formData = new FormData();
        pictures.forEach((picture, index) => {
            formData.append(`picture${index + 1}`, picture.file);
        });
        formData.append('seller_id', localStorage.getItem('user_id'));
        formData.append('game_title_id', game_title.id);
        formData.append('category', category);
        formData.append('listing_title', listing_title);
        formData.append('description', description);
        formData.append('price_negotiation', price_negotiation);
        formData.append('price', price);
        formData.append('create', true);
        withTokenRequest.post('/setListing', formData,
            {
                headers: multipartFormData
            }).then(() => {
                navigate('/listingProducts');
            })
            .catch((error) => {
                console.log(error);
            });
    }

    if (gameTitles == null || availableFee == null) {
        return (
            <></>
        )
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
                <h2>New Listing</h2>
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
                    defaultValue={null}
                    options={gameTitles}
                    getOptionLabel={(option) => option.title}
                    sx={{ width: 450 }}
                    renderInput={(params) => <TextField {...params} label='Game Title' />}
                    onChange={(event, newValue) => {handleChange(event, newValue, 'setGameTitle', null);}}>
                </Autocomplete><br /><br />
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
                    label='Listing Title'
                    variant='outlined'
                    name="lising_title"
                    value={listing_title}
                    onChange={(event, newValue) => {handleChange(event, newValue, 'setListingTitle', null);}}
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
                    <InputLabel htmlFor="standard-adornment-price">Price</InputLabel>
                    <Input
                        id="standard-adornment-price"
                        startAdornment={<InputAdornment position="start">$</InputAdornment>}
                        value={price}
                        onChange={(event, newValue) => {handleChange(event, newValue, 'setPrice', null);}}
                    />
                </FormControl><br /><br />
                <div>Fee ({availableFee.percentage * 100}%) : &nbsp;&nbsp;&nbsp;${fee}</div>
                <div>Revenue : &nbsp;&nbsp;&nbsp;${revenue}</div><br />
                <FormControlLabel 
                    control={
                        <Checkbox 
                            checked={price_negotiation_checked}
                            onChange={(event, newValue) => {handleChange(event, newValue, 'setPriceNegotiationChecked', null);}}
                            name='Price negotiation'
                            color="primary"
                        />
                    }
                    label="Price negotiation"
                />
                
                <br /><br /><br /><br />
                <Button variant="contained" onClick={setListing}>Register</Button>
            </div>
        </div>
    )
}

export default NewListing;