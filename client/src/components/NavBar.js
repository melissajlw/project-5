import React from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Box, IconButton } from '@mui/material';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';

const NavBar = ({ user, cartItems }) => {
    const navigate = useNavigate();

    // Links displayed in the NavBar for the seller
    const sellerLinks = (
        <>
            <Button color="inherit" component={Link} to='/ordersinprogress'>Orders</Button>
            <Button color="inherit" component={Link} to='/addItem'>Add Product</Button>
        </>
    );

    // Links displayed in the NavBar for the buyer
    const buyerLinks = (
        <>
            <Button color="inherit" component={Link} to='/orders'>Orders</Button>
            <Button color="inherit" component={Link} to='/cart'>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <ShoppingCartIcon />
                    <Typography variant="body2" sx={{ marginLeft: 1 }}>
                        {cartItems.length}
                    </Typography>
                </Box>
            </Button>
        </>
    );

    return (
        <AppBar position="static" sx={{ backgroundColor: '#748B75' }}>
            <Toolbar>
                <Typography variant="h6" component={Link} to='/' sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}>
                    Home
                </Typography>
                {
                    user ?
                    <Button color="inherit" component={NavLink} to='/signout'>Sign Out</Button> :
                    <Button color="inherit" component={NavLink} to='/signin'>Sign In</Button>
                }
                {
                    user && user.seller ? sellerLinks : buyerLinks
                }
            </Toolbar>
        </AppBar>
    );
}

export default NavBar;