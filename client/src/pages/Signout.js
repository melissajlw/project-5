import { useEffect } from 'react';
import { useOutletContext, useNavigate } from 'react-router-dom';
import { Box, Button, Typography, Container, Alert } from '@mui/material';

function Signout() {
    const { onSetUser, onSetCartItems, onSetOrders, onSetReviews, onSetSellerItems } = useOutletContext();
    const navigate = useNavigate();

    useEffect(() => {
        fetch('/authenticate', {
            method: 'DELETE',
        })
        .then(r => {
            if (r.ok) {
                onSetUser(null);
                onSetCartItems([]);
                onSetOrders([]);
                onSetReviews([]);
                onSetSellerItems([]);
                navigate('/');
            } else {
                console.log('Signout failed');
            }
        });
    }, [onSetUser, onSetCartItems, onSetOrders, onSetReviews, onSetSellerItems, navigate]);

    return (
        <Container maxWidth="sm" sx={{ mt: 8 }}>
            <Box sx={{ p: 4, border: '1px solid lightgrey', borderRadius: 1, backgroundColor: '#F5FBEF' }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    Signing out...
                </Typography>
                <Alert severity="info" sx={{ mt: 2 }}>
                    You are being signed out. Please wait...
                </Alert>
                <Button color="primary" variant="contained" fullWidth onClick={() => navigate('/')} sx={{ mt: 2 }}>
                    Go to Home
                </Button>
            </Box>
        </Container>
    );
}

export default Signout;