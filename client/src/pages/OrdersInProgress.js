import { useState, useEffect } from 'react';
import { useOutletContext, useNavigate } from 'react-router-dom';
import { formatDate, applyUTCToOrder } from '../components/global';
import { Box, Button, Container, Grid2, MenuItem, Select, Typography, Card, CardContent, CardMedia, Divider } from '@mui/material';

function OrdersInProgress() {
    const { user, sellerItems, onSetSellerItems } = useOutletContext();
    const [filterItemId, setFilterItemId] = useState(-1);
    const navigate = useNavigate();

    const otherItemOptions = sellerItems.map((item, i) => ({
        key: i,
        text: item.name.slice(0, 20) + '...',
        value: item.id,
    }));
    const itemOptions = [{ key: -1, text: 'All', value: -1 }, ...otherItemOptions];

    // RBAC
    useEffect(() => {
        if (!user || !user.seller) {
            navigate('/signin');
            return;
        }
    }, [user, navigate]);

    async function handleOrderItem(orderItem, sellerItem) {
        const curDate = new Date();
        const year = curDate.getUTCFullYear();
        const month = String(curDate.getUTCMonth() + 1).padStart(2, '0');
        const day = String(curDate.getUTCDate()).padStart(2, '0');
        const hours = String(curDate.getUTCHours()).padStart(2, '0');
        const minutes = String(curDate.getUTCMinutes()).padStart(2, '0');
        const seconds = String(curDate.getUTCSeconds()).padStart(2, '0');

        const curDateUTC = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;

        let curOrder = null;
        await fetch(`/orders/${orderItem.order_id}`)
            .then(async r => {
                await r.json().then(data => {
                    if (r.ok) {
                        curOrder = data;
                    } else {
                        if (r.status === 401 || r.status === 403) {
                            console.log(data);
                            alert(data.message);
                        } else {
                            console.log("Server Error - Can't retrieve the order: ", data);
                            alert(`Server Error - Can't retrieve the order: ${data.message}`);
                            return;
                        }
                    }
                });
            });

        await fetch(`/orderitems/${orderItem.id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                processed_date: curDateUTC,
            })
        })
            .then(async r => {
                await r.json().then(async data => {
                    if (r.ok) {
                        const si = {
                            ...sellerItem,
                            order_items: sellerItem.order_items.map(oi =>
                                oi.id === data.id ? { ...oi, ...data } : oi),
                        };
                        onSetSellerItems(sellerItems.map(item => item.id === si.id ? si : item));

                        if (!curOrder) return;
                        const isCompleteOrder = curOrder.order_items.reduce((acc, oi) => {
                            return acc && (oi.id === data.id ? true : !!oi.processed_date);
                        }, true);

                        if (isCompleteOrder) {
                            await fetch(`/orders/${curOrder.id}`, {
                                method: 'PATCH',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    closed_date: curDateUTC,
                                })
                            })
                                .then(async r => {
                                    await r.json().then(data => {
                                        if (r.ok) {
                                        } else {
                                            if (r.status === 401 || r.status === 403) {
                                                console.log(data);
                                                alert(data.message);
                                            } else {
                                                console.log("Server Error - Can't update the order: ", data);
                                                alert(`Server Error - Can't update the order: ${data.message}`);
                                                return;
                                            }
                                        }
                                    });
                                });
                        }
                    } else {
                        if (r.status === 401 || r.status === 403) {
                            console.log(data);
                            alert(data.message);
                        } else {
                            console.log("Server Error - Can't update an order item: ", data);
                            alert(`Server Error - Can't update an order item: ${data.message}`);
                        }
                    }
                });
            });
    }

    const filteredSellerItems = sellerItems.filter(item => filterItemId === -1 || item.id === filterItemId);

    const dispOrdersInProgress = filteredSellerItems.map(item => {
        const orderItemsLocalTime = item.order_items.map(oi => ({
            ...oi,
            order: applyUTCToOrder(oi.order),
        }));
        orderItemsLocalTime.sort((a, b) => b.order.ordered_date - a.order.ordered_date);

        const dispOrderItemsInProgress = orderItemsLocalTime.map(oi => (
            oi.processed_date ? null :
                <Card key={`${item.id}-${oi.id}`} sx={{ marginTop: 2 }}>
                    <CardMedia
                        component="div"
                        sx={{
                            width: '80px',
                            height: '100px',
                            marginLeft: 2,
                            backgroundImage: `url(${item.images[0]})`,
                            backgroundSize: 'contain',
                            backgroundRepeat: 'no-repeat',
                            backgroundPosition: 'center',
                        }}
                    />
                    <CardContent sx={{ marginLeft: 4, marginRight: 4 }}>
                        <Typography variant="h6">{item.name}</Typography>
                        <ul>
                            <li>Ordered Date: {formatDate(oi.order.ordered_date)}</li>
                            <li>Price: ${oi.price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</li>
                        </ul>
                        <Divider sx={{ my: 1 }} />
                        <ul>
                            <li>Size: {`${item.amounts[oi.item_idx].toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ${item.units[oi.item_idx].charAt(0).toUpperCase() + item.units[oi.item_idx].slice(1)} (Pack of ${item.packs[oi.item_idx].toLocaleString('en-US')})`}</li>
                            <li>Quantity: {oi.quantity.toLocaleString('en-US')}</li>
                            <li>Shipping Address:
                                <div>{oi.order.customer.first_name} {oi.order.customer.last_name}</div>
                                <div>{oi.order.street_1}</div>
                                <div>{oi.order.street_2}</div>
                                <div>{oi.order.city} {oi.order.state} {oi.order.zip_code}</div>
                            </li>
                        </ul>
                        <Button
                            variant="contained"
                            color="warning"
                            sx={{ width: '250px', fontSize: '1.1em', borderRadius: 2, mt: 2 }}
                            onClick={() => handleOrderItem(oi, item)}
                        >
                            Complete Order
                        </Button>
                    </CardContent>
                </Card>
        ));

        return dispOrderItemsInProgress;
    });

    return (
        <Container sx={{ marginTop: 4 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h4">Order Queue</Typography>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Typography variant="body1" sx={{ mr: 2 }}>Filter by</Typography>
                    <Select
                        value={filterItemId}
                        onChange={(e) => setFilterItemId(e.target.value)}
                        sx={{ minWidth: 200 }}
                    >
                        {itemOptions.map(option => (
                            <MenuItem key={option.key} value={option.value}>
                                {option.text}
                            </MenuItem>
                        ))}
                    </Select>
                </Box>
            </Box>
            <Grid2 container spacing={2}>
                {dispOrdersInProgress}
            </Grid2>
        </Container>
    );
}

export default OrdersInProgress;