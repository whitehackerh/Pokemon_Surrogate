import { useNavigate } from "react-router-dom";
import { useState } from 'react';
import { withTokenRequest, requestHeaders } from '../../http';
import logo from "../../assets/img/logo.png";
import IconButton from "@mui/material/IconButton";
import Button from "@mui/material/Button";
import MenuItem from "@mui/material/MenuItem";
import Menu from "@mui/material/Menu";
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

const Header = () => {
    let navigate = useNavigate();
    const [anchorEl, setAnchorEl] = useState(null);
    const isMenuOpen = Boolean(anchorEl);
    const handleProfileMenuOpen = (event) => {
        setAnchorEl(event.currentTarget);
      }
    const handleMenuClose = () => {
      setAnchorEl(null);
    };

    let staffMenu = '';
    if (localStorage.getItem('is_staff')) {
      staffMenu = (
        <MenuItem onClick={() => {handleMenuClose(); navigate("/signupStaff");}}>Signup Staff</MenuItem>
      )
    }

    const renderMenu = () => {
        return (
            <Menu
              anchorEl={anchorEl}
              anchorOrigin={{ vertical: "top", horizontal: "right" }}
              transformOrigin={{ vertical: "top", horizontal: "right" }}
              open={isMenuOpen}
              onClose={handleMenuClose}
            >
              <MenuItem onClick={() => {handleMenuClose(); navigate("/profileSettings");}}>Account Settings</MenuItem>
              {staffMenu}
              <MenuItem onClick={() => {handleMenuClose(); LogoutEvent();}}>Logout</MenuItem>
            </Menu>
          );
    }

    const LogoutEvent = () => {
      requestHeaders.Authorization = `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`;
      withTokenRequest.post('/logout', {
      },{
        headers: requestHeaders
      }).then(() => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('token_type');
        localStorage.removeItem('user_id');
        localStorage.removeItem('is_staff');
        navigate('/');
      })
    };

    const headerButtonStyle = {
        float: 'right',
        'margin-right': '30px',
        padding: '20px 0'
    }

    let AuthMenu = '';
    if (localStorage.getItem('access_token')) {
      AuthMenu = (
        <>
        <IconButton 
        aria-owns={isMenuOpen ? "material-appbar" : undefined}
        aria-haspopup="true"
        onClick={handleProfileMenuOpen}
        style={headerButtonStyle}
        color="inherit">
            <AccountCircleIcon />
        </IconButton>
        </>
      );
    } else {
      AuthMenu = (
      <Button style={headerButtonStyle} color="inherit" onClick={() => navigate('/login')}>
        Login
      </Button>
      );
    }

    return (
        <>
            <img src={logo} alt="picture" onClick={() => navigate('/')} style={{cursor: 'pointer', height: '60px', 'margin-left': '50px'}}/>
            {AuthMenu}
            {renderMenu()}
        </>
    )
}

export default Header;