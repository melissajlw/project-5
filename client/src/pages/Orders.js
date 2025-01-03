import { useState, useEffect } from 'react';
import { useOutletContext, useNavigate } from 'react-router-dom';
import { applyUTCToOrder, formatDate } from '../components/global';
import { Box, Button, Card, CardContent, CardMedia, Container, Grid2, MenuItem, Select, Typography } from '@mui/material';

function Orders() {
    const { user, orders } = useOutletContext();
    const [period, setPeriod] = useState(2);
    const navigate = useNavigate();

    const periodOptions = [
        { key: 1, text: 'last 30 days', value: 1 },
        { key: 2, text: 'past 3 months', value: 2 },
        { key: 3, text: `${new Date().getFullYear()}`, value: 3 },
        { key: 4, text: `${new Date().getFullYear() - 1}`, value: 4 },
        { key: 5, text: `${new Date().getFullYear() - 2}`, value: 5 },
    ];

    useEffect(() => {
        if (!user || !user.customer) {
            navigate('/signin');
            return;
        }
    }, [user, navigate]);

    const handleNavigateItem = (itemId) => {
        navigate(`/items/${itemId}`);
    };

    const ordersLocalTime = orders.map(order => applyUTCToOrder(order));

    const thirtyDaysInMillisec = 1000 * 60 * 60 * 24 * 30;
    const ordersInPeriod = ordersLocalTime.filter(order => {
        switch (period) {
            case 1:
                return new Date() - order.ordered_date < thirtyDaysInMillisec;
            case 2:
                const threeMonthsAgo = new Date();
                const threeMonthsAgoTS = threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
                return order.ordered_date > threeMonthsAgoTS;
            case 3:
                return new Date(order.ordered_date).getFullYear() === new Date().getFullYear();
            case 4:
                return new Date(order.ordered_date).getFullYear() === new Date().getFullYear() - 1;
            case 5:
                return new Date(order.ordered_date).getFullYear() === new Date().getFullYear() - 2;
            default:
                return true;
        }
    });

    ordersInPeriod.sort((a, b) => b.ordered_date - a.ordered_date);

    const dispOrders = ordersInPeriod.map(order => {
        const total = Math.round(order.order_items.reduce((accum, oi) => accum + (oi.quantity * oi.price), 0) * 100) / 100;

        const dispOrderedItems = order.order_items.map(oi => (
            <Grid2 container key={oi.id} spacing={2} alignItems="center" sx={{ mb: 2 }}>
                <Grid2 item>
                    <CardMedia
                        component="img"
                        sx={{ width: 125, height: 150, cursor: 'pointer' }}
                        image={oi.item.images[0]}
                        alt={oi.item.name}
                        onClick={() => handleNavigateItem(oi.item_id)}
                    />
                </Grid2>
                <Grid2 item>
                    <Typography variant="h6" component="div" sx={{ cursor: 'pointer' }} onClick={() => handleNavigateItem(oi.item_id)}>
                        {oi.item.name}
                    </Typography>
                </Grid2>
            </Grid2>
        ));

        return (
            <Card key={order.id} sx={{ mb: 4 }}>
                <CardContent>
                    <Grid2 container spacing={2} alignItems="center">
                        <Grid2 item>
                            <Typography variant="subtitle2">ORDER PLACED</Typography>
                            <Typography variant="body1">{formatDate(order.ordered_date)}</Typography>
                        </Grid2>
                        <Grid2 item>
                            <Typography variant="subtitle2">TOTAL</Typography>
                            <Typography variant="body1">${total.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</Typography>
                        </Grid2>
                        <Grid2 item>
                            <Typography variant="subtitle2">SHIP TO</Typography>
                            <Typography variant="body1">{`${user.customer.first_name} ${user.customer.last_name}`}</Typography>
                        </Grid2>
                    </Grid2>
                    <Box sx={{ mt: 2 }}>
                        <Typography variant="h5" component="div" sx={{ fontWeight: 'bold', mb: 2 }}>
                            {!order.closed_date ? (
                                <Typography color="primary">In progress</Typography>
                            ) : (
                                <Typography>Delivered {formatDate(order.ordered_date).slice(0, -6)}</Typography>
                            )}
                        </Typography>
                        {dispOrderedItems}
                        <Button variant="outlined" fullWidth sx={{ mt: 2 }} onClick={() => navigate('/reviewlist')}>
                            Write a product review
                        </Button>
                    </Box>
                </CardContent>
            </Card>
        );
    });

    return (
        <Container sx={{ mt: 4 }}>
            <Typography variant="h4" component="h1" gutterBottom>
                Your Orders
            </Typography>
            <Box sx={{ mb: 4 }}>
                <Typography variant="h6" component="span" sx={{ fontWeight: 'bold' }}>
                    {`${ordersInPeriod.length} order${ordersInPeriod.length <= 1 ? '' : 's'} `}
                </Typography>
                <Typography variant="h6" component="span">
                    placed in
                </Typography>
                <Select
                    value={period}
                    onChange={(e) => setPeriod(e.target.value)}
                    sx={{ ml: 2, minWidth: 200 }}
                >
                    {periodOptions.map(option => (
                        <MenuItem key={option.key} value={option.value}>
                            {option.text}
                        </MenuItem>
                    ))}
                </Select>
            </Box>
            {dispOrders}
        </Container>
    );
}

export default Orders;