import { useEffect, useState } from 'react';
import { Outlet } from 'react-router-dom';
import NavBar from '../components/NavBar';
import { setUserInfo } from '../components/global';
import { ItemProvider } from '../components/ItemProvider';


function App() {
    const [ user, setUser ] = useState(null);
    const [ cartItems, setCartItems ] = useState([]);
    const [ orders, setOrders ] = useState([]);
    const [ reviews, setReviews ] = useState([]);
    const [ sellerItems, setSellerItems ] = useState([]);

    useEffect(() => {
        fetch('/authenticate')
        .then(r => 
            r.json().then(data => {
                if (r.ok) {
                    console.log('in App, full user data: ', data);
                    setUserInfo(data, setUser, setCartItems, setOrders, setReviews, setSellerItems);
                } else {
                    console.log('In App, error: ', data.message);
                }
            })
        )
    }, []);

    return (
        <div style={{display: 'grid', gridTemplateRows: 'max-content 1fr', }}>
            <header>
                <NavBar user={user} cartItems={cartItems} />
            </header>
            <main>
                <ItemProvider>
                    <Outlet context={{
                        user: user,
                        onSetUser: setUser,
                        cartItems: cartItems,
                        onSetCartItems: setCartItems,
                        orders: orders,
                        onSetOrders: setOrders,
                        reviews: reviews,
                        onSetReviews: setReviews,
                        sellerItems: sellerItems,
                        onSetSellerItems: setSellerItems, 
                    }} />
                </ItemProvider>
            </main>
        </div>
    );
}

export default App;