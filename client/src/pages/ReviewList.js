import { useEffect, useState } from 'react';
import { useOutletContext, useNavigate } from 'react-router-dom';
import { applyUTCToOrder, dispRating } from '../components/global';
import { Box, Button, Card, CardContent, CardMedia, Container, Divider, Grid2, Typography } from '@mui/material';

function ReviewList() {
    const { user, orders, reviews, onSetReviews } = useOutletContext();
    const [itemsReviewed, setItemsReviewed] = useState({});
    const navigate = useNavigate();

    useEffect(() => {
        const itemsReviewedTmp = {};
        reviews.forEach(review => {
            if (!itemsReviewedTmp.hasOwnProperty(review.item_id)) {
                itemsReviewedTmp[review.item_id] = review;
            }
        });
        setItemsReviewed(itemsReviewedTmp);
    }, [reviews]);

    function handleNavigateReview(itemId) {
        navigate(`/reviewlist/${itemId}`);
    }

    const ordersLocalTime = orders.map(order => applyUTCToOrder(order));
    ordersLocalTime.sort((a, b) => b.date - a.date);

    const itemsNotReviewed = [];
    const itemsInList = {};

    ordersLocalTime.forEach(order => {
        order.order_items.forEach(oi => {
            if (!itemsInList.hasOwnProperty(oi.item_id) &&
                (!itemsReviewed.hasOwnProperty(oi.item_id) || !itemsReviewed[oi.item_id].review_done) &&
                oi.item.active) {
                itemsNotReviewed.push(oi.item);
                itemsInList[oi.item_id] = oi;
            }
        });
    });

    const dispReviewCards = itemsNotReviewed.map(item => (
        <Grid2 item xs={12} sm={6} md={4} key={item.id}>
            <Card sx={{ minWidth: 200, borderWidth: 0, alignItems: 'center' }}>
                <CardMedia
                    component="div"
                    sx={{
                        width: '90%',
                        height: 250,
                        margin: 'auto',
                        backgroundImage: `url(${item.images[0]})`,
                        backgroundSize: 'contain',
                        backgroundRepeat: 'no-repeat',
                        backgroundPosition: 'center',
                        cursor: 'pointer',
                    }}
                    onClick={() => handleNavigateReview(item.id)}
                />
                <CardContent>
                    <Typography
                        variant="h6"
                        component="div"
                        sx={{ fontSize: '1.1em', margin: '10px auto 0', cursor: 'pointer' }}
                        onClick={() => handleNavigateReview(item.id)}
                    >
                        {item.name.length <= 20 ? item.name : item.name.slice(0, 20) + '...'}
                    </Typography>
                    <Box sx={{ margin: '10px auto' }}>
                        {dispRating(item.id,
                            itemsReviewed.hasOwnProperty(item.id) ? itemsReviewed[item.id] : null,
                            user, reviews, onSetReviews)}
                    </Box>
                    {itemsReviewed.hasOwnProperty(item.id) && (
                        <Button
                            variant="outlined"
                            sx={{
                                color: 'black',
                                backgroundColor: 'white',
                                fontSize: '0.8em',
                                padding: '5px 30px',
                                marginBottom: '10px',
                                border: '1px solid lightgray',
                                borderRadius: '10px',
                            }}
                            onClick={() => handleNavigateReview(item.id)}
                        >
                            Write a review
                        </Button>
                    )}
                </CardContent>
            </Card>
        </Grid2>
    ));

    return (
        <Container sx={{ padding: '0 140px' }}>
            <Typography variant="h4" component="div" sx={{ margin: '30px 0' }}>
                Review Your Purchases
            </Typography>
            <Divider />
            <Grid2 container spacing={3} sx={{ marginTop: '5px', minWidth: '815px' }}>
                {dispReviewCards}
            </Grid2>
        </Container>
    );
}

export default ReviewList;