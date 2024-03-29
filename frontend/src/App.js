import logo from './logo.svg';
import './App.css';
import {
  BrowserRouter,
  Routes,
  Route,
  Outlet,
  Link,
  useLocation
} from "react-router-dom";
import Header from "./components/modules/Header";
import HomeBar from "./components/modules/HomeBar";
import Home from "./components/pages/home/Home";
import Login from "./components/pages/login/Login";
import Signup from "./components/pages/signup/Signup";
import ProfileSettings from "./components/pages/accountSettings/ProfileSettings";
import ProfilePictureSettings from './components/pages/accountSettings/ProfilePictureSettings';
import SignupStaff from "./components/pages/accountSettings/SignupStaff";
import ListingProducts from "./components/pages/transactions/ListingProducts";
import EditListing from "./components/pages/transactions/EditListing";
import ListingDetail from "./components/modules/common/ListingDetail";
import MarketSales from './components/pages/listings/MarketSales';
import PurchaseProducts from './components/pages/transactions/PurchaseProducts';
import TransactionChatListing from './components/pages/transactions/TransactionChatListing';
import EditRequest from './components/pages/transactions/EditRequest';
import Requests from './components/pages/transactions/Requests';
import RequestList from './components/pages/requests/RequestList';
import RequestDetail from './components/modules/common/RequestDetail';
import Accepts from './components/pages/transactions/Accepts';
import TransactionChatRequest from './components/pages/transactions/TransactionChatRequest';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  typography: {
    fontFamily: 'Century Gothic, sans-serif',
  },
});

const Top = () => {
  return (
    <h1></h1>
  );
};

const Menu = () => {
  let location = useLocation();
  return (
    <>
      <Header />
      <HomeBar />
      {location.pathname === "/" ? <Top /> : <></>}
      <Outlet />
    </>
  );
};

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Menu />}>
            <Route path="/home" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/profileSettings" element={<ProfileSettings />} />
            <Route path="/profilePictureSettings" element={<ProfilePictureSettings />} />
            <Route path="/signupStaff" element={<SignupStaff />} />
            <Route path="/listingProducts" element={<ListingProducts />} />
            <Route path="/editListing" element={<EditListing />} />
            <Route path="/listingDetail" element={<ListingDetail />} />
            <Route path='/marketSales' element={<MarketSales />} />
            <Route path='/purchaseProducts' element={<PurchaseProducts />} />
            <Route path='/transactionChatListing' element={<TransactionChatListing />} />
            <Route path='/requests' element={<Requests />} />
            <Route path='/editRequest' element={<EditRequest />} />
            <Route path='/requestList' element={<RequestList />} />
            <Route path='/requestDetail' element={<RequestDetail />} />
            <Route path='/accepts' element={<Accepts />} />
            <Route path='/transactionChatRequest' element={<TransactionChatRequest />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App;
