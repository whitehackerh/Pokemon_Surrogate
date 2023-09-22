import { Link } from "react-router-dom";

const SideBar_Transactions = () => {
    const style = {
        position: 'sticky',
        width: '300px',
        border: '1px solid blue',
        margin: '10px',
        padding: '10px',
        float: 'left'
    };
    return (
        <div style={style}>
            <Link to="/listingProducts">Listing Products</Link><br /><br />
            <Link to="/purchaseProducts">Purchased Products</Link><br /><br />
            <Link to="/editListing">New Listing</Link><br /><br />
            <Link to="/requests">Requests</Link><br /><br />
            <Link to='/accepts'>Accepts</Link><br /><br />
            <Link to='/editRequest'>New Request</Link><br /><br />
        </div>
    );
};

export default SideBar_Transactions;