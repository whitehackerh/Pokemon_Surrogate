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
import NewListing from "./components/pages/transactions/NewListing";

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
          <Route path="/newListing" element={<NewListing />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App;
