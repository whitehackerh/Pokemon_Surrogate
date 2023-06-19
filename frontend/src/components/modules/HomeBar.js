import { Box } from "@mui/material";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";

const HomeBar = () => {
    return (
        <Box>
          <AppBar position="static" style={{"background-color": "primary"}}>
            <Toolbar>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              </Typography>
            </Toolbar>
          </AppBar>
        </Box>
      );
};

export default HomeBar;