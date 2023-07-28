import { Box } from "@mui/material";
import { useNavigate } from "react-router-dom";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";

const HomeBar = () => {
  let navigate = useNavigate();

  const homeBarContentStyle = {
    fontSize: '20px',
    fontFamily: 'Century Gothic'
  };

  return (
      <Box>
        <AppBar position="static" style={{"background-color": "primary"}}>
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              <div style={{textAlign: 'center'}}>
                <IconButton onClick={() => navigate('/marketSales')} style={homeBarContentStyle}>Market Sales</IconButton>
              </div>
            </Typography>
          </Toolbar>
        </AppBar>
      </Box>
  );
};

export default HomeBar;