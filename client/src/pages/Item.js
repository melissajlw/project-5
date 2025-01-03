import { useEffect, useState, useContext } from 'react';
import { useParams, useOutletContext, useNavigate, } from 'react-router-dom'; 
//bkj - active
import { displayPrice, dispListPrice, handleCItemAdd, handleCItemChange, 
    formatDate, convertUTCDate, handleInactvateItem, dispAvgRating, } from '../components/global';
import { ItemContext } from '../components/ItemProvider';
import { Table, TableBody, TableCell, TableRow, Box, ButtonGroup, Button, Card, CardMedia, Container, Divider, IconButton, MenuItem, Select, Typography, LinearProgress, Avatar, Grid2, Paper, } from '@mui/material';
import { Clear as ClearIcon, Edit as EditIcon, Delete as DeleteIcon, AddShoppingCart as AddShoppingCartIcon, ShoppingCart as ShoppingCartIcon } from '@mui/icons-material';
import StarIcon from '@mui/icons-material/Star';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

function Item() {
    const { id } = useParams();
    const { item, setItem } = useContext(ItemContext);
    const [ activeItemIdx, setActiveItemIdx ] = useState(0);
    const [ activeImageIdx, setActiveImageIdx ] = useState(0);
    const [ quantity, setQuantity ] = useState(1);
    const [ itemReviews, setItemReviews ] = useState([]);

    const [ avgRating, setAvgRating ] = useState(0);
    const [ starCounts, setStarCounts ] = useState([0, 0, 0, 0, 0]);
    
    const { user, cartItems, onSetCartItems, orders, onSetOrders, } = useOutletContext();
    const navigate = useNavigate();
    

    const quantityOptions = [];
    for (let i = 1; i <= 30; i++)
        quantityOptions.push({
            key: i,
            text: `${i}`,
            value: i
        });

    useEffect(() => {
        if (item && item.id === parseInt(id)) {
            if (item.default_item_idx >= 0 && item.default_item_idx < item.prices.length)
                setActiveItemIdx(item.default_item_idx);
        } else {
            fetch(`/items/${id}`)
            .then(r => {
                r.json().then(data => {
                    if (r.ok) {
                        setItem(data);
                        if (data.default_item_idx >= 0 && data.default_item_idx < data.prices.length)
                            setActiveItemIdx(data.default_item_idx);
                    } else {
                        console.log('Error: ', data.message);
                    }
                });
            })
        }

        fetch(`/reviews/items/${id}`)
        .then(r => {
            r.json().then(data => {
                if (r.ok) {
                    setItemReviews(data);
                    setAvgRating(
                        Math.round(data.reduce((avg, review, i) => 
                            review.review_done ? 
                            avg + (review.rating - avg) / (i+1) :
                            avg
                        , 0) * 10) / 10);
                    const starCountsTmp = [0, 0, 0, 0, 0];
                    data.forEach(review => starCountsTmp[review.rating-1] += 1);
                    setStarCounts(starCountsTmp);
                } else {
                    console.log(data);
                    alert(data.message);
                }
            });
        });

    }, []);

    function dispAllSizes() {
        const packs = item.packs.map((pack, i) => {
            return (
                <div key={pack} className={`${i === activeItemIdx ? 'size-active-link' : 'size-link'} link`} 
                    onClick={() => setActiveItemIdx(i)}>
                    {
                        `${item.amounts[i]} \
                        ${item.units[i].charAt(0).toUpperCase() + item.units[i].slice(1)} \
                        (Pack of ${pack})`
                    }
                </div>
            );
        });
        return packs;
    }

    function dispDetail_1() {
        return (
            <Table sx={{ border: 'none' }}>
                <TableBody>
                    {item.details_1.map((pair, i) => {
                        const pairArray = pair.split(';-;');
    
                        return (
                            <TableRow key={i}>
                                <TableCell sx={{ width: '40%', fontWeight: 'bold', paddingLeft: 0 }}>
                                    {pairArray[0]}
                                </TableCell>
                                <TableCell sx={{ width: '60%', paddingLeft: 0 }}>
                                    {pairArray[1]}
                                </TableCell>
                            </TableRow>
                        );
                    })}
                </TableBody>
            </Table>
        );
    }

    function dispDetail_2() {
        return (
            <Box sx={{ margin: '15px', fontSize: '1.1em' }}>
                {
                    item.details_2.map((pair, i) => {
                        const pairArray = pair.split(';-;');
    
                        return (
                            <Box key={i} sx={{ marginBottom: '8px' }}>
                                <Typography component="span" sx={{ fontWeight: 'bold' }}>
                                    {`${pairArray[0]} : `}
                                </Typography>
                                <Typography component="span">
                                    {pairArray[1]}
                                </Typography>
                            </Box>
                        );
                    })
                }
            </Box>
        );
    }

    function dispAboutItem() {
        return (
            <ul style={{marginLeft: '15px', }}>
                {item.about_item.map((info, i) =>
                    <li key={i}>{info}</li>
                )}
            </ul>
        );
    }

    function handleThumnailMouseEnter(idx) {
        setActiveImageIdx(idx);
    }

    function dispThumbnails() {
        return (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {item.images.map((thumbnail, i) => (
                    <CardMedia
                        key={i}
                        component="img"
                        src={thumbnail}
                        alt="product thumbnail"
                        sx={{
                            width: 60,
                            height: 60,
                            objectFit: 'cover',
                            cursor: 'pointer',
                            border: activeImageIdx === i ? '2px solid #92AD94' : '2px solid transparent',
                            borderRadius: 1,
                            '&:hover': {
                                border: '2px solid #92AD94',
                            },
                        }}
                        onMouseEnter={() => handleThumnailMouseEnter(i)}
                    />
                ))}
            </Box>
        );
    }

    function dispStarDistribution() {
        return (
            starCounts.map((cnt, i) => {
                const percentage = Math.round((starCounts[4 - i] / itemReviews.length) * 100);
    
                return (
                    <Box key={i} sx={{ display: 'flex', alignItems: 'center', margin: '15px 0' }}>
                        <Typography variant="body1" sx={{ fontSize: '1.1em', width: '60px' }}>
                            {5 - i} star
                        </Typography>
                        <Box sx={{ width: '200px', marginLeft: '15px', marginRight: '15px' }}>
                            <LinearProgress variant="determinate" value={percentage} sx={{ height: '10px', borderRadius: '5px', backgroundColor: 'lightgray' }} />
                        </Box>
                        <Typography variant="body2" sx={{ width: '40px' }}>
                            {percentage}%
                        </Typography>
                    </Box>
                );
            })
        );
    }

    function dispReviewRating(review) {
        const stars = [];
    
        for (let i = 1; i <= 5; i++) {
            stars.push(
                <Box key={i} sx={{ display: 'inline-block', width: '17px', height: '17px' }}>
                    {review.rating >= i ? (
                        <StarIcon sx={{ color: '#FFD700', width: '100%', height: '100%' }} />
                    ) : (
                        <StarBorderIcon sx={{ color: '#FFD700', width: '100%', height: '100%' }} />
                    )}
                </Box>
            );
        }
    
        return <Box sx={{ display: 'flex', alignItems: 'center' }}>{stars}</Box>;
    }

    function dispReviews() {
        return (
            itemReviews.map(review => 
                review.review_done ? 
                <Paper key={review.id} sx={{ padding: 2, margin: '15px 0', fontSize: '1.1em' }}>
                    <Grid2 container spacing={2} alignItems="center">
                        <Grid2 item>
                            <Avatar sx={{ bgcolor: 'lightgray' }}>
                                <AccountCircleIcon />
                            </Avatar>
                        </Grid2>
                        <Grid2 item>
                            <Typography variant="body1">
                                {review.customer.nickname ? review.customer.nickname : review.customer.first_name}
                            </Typography>
                        </Grid2>
                    </Grid2>
                    <Box sx={{ display: 'grid', gridTemplateColumns: 'max-content 1fr', alignItems: 'center', marginTop: '7px' }}>
                        <Box>{dispReviewRating(review)}</Box>
                        <Typography variant="h6" sx={{ fontWeight: 'bold', marginLeft: '10px' }}>
                            {review.headline}
                        </Typography>
                    </Box>
                    <Typography variant="body2" color="textSecondary">
                        Reviewed on {formatDate(convertUTCDate(review.date))}
                    </Typography>
                    <Box sx={{ margin: '5px 0' }}>
                        <Typography variant="body1">
                            {review.content}
                        </Typography>
                    </Box>
                </Paper> : 
                null
            )
        );
    }

    function handleAddToCart() {
        if (!item) return;

        if (!user || !user.customer) {
            alert("Please, signin with your customer account.");
            navigate('/signin');
            return;
        }

        const cItem = cartItems.find(cItem => 
            cItem.item_id === item.id && cItem.item_idx === activeItemIdx);
        
        if (cItem) {
            handleCItemChange({
                ...cItem,
                quantity: cItem.quantity + quantity,
            }, onSetCartItems, () => navigate('/cart'));
        } else {
            handleCItemAdd({
                checked: 1,
                quantity: quantity,
                item_idx: activeItemIdx,
                item_id: item.id,
                customer_id: user.customer.id,
            }, onSetCartItems, () => navigate('/cart'));
        }
    }


    function handlePlaceOrder() {
        if (!item) return;

        if (!user || !user.customer) {
            alert("Please, signin with your customer account.");
            navigate('/signin');
            return;
        }

        fetch('/orders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                street_1: user.street_1,
                street_2: user.street_2,
                city: user.city,
                state: user.state,
                zip_code: user.zip_code,
                customer_id: user.customer.id,
            }),
        })
        .then(r => {
            r.json().then(data1 => {
                if (r.ok) {
                    const orderTmp = data1;
                    fetch('/orderitems', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            quantity: quantity,
                            price: item.discount_prices[activeItemIdx],
                            item_idx: activeItemIdx, 
                            item_id: item.id,
                            order_id: orderTmp.id,
                        }),
                    })
                    .then(r => {
                        r.json().then(data2 => {
                            if (r.ok) {
                                const orderItemTmp = data2;
                                orderItemTmp.item = item;
                                orderTmp.order_items.push(orderItemTmp);
                                onSetOrders([
                                    ...orders,
                                    orderTmp
                                ]);

                                navigate('/orders');
                            } else {
                                if (r.status === 401 || r.status === 403) {
                                    console.log(data2); 
                                    alert(data2.message);
                                } else {
                                    console.log("Server Error - Can't add an order item: ", data2);
                                    alert(`Server Error - Can't add an order item: ${data2.message}`);

                                    fetch(`/orders/${orderTmp.id}`, {
                                        method: 'DELETE',
                                    })
                                }
                            }
                        });
                    });
                } else {
                    if (r.status === 401 || r.status === 403) {
                        console.log(data1);
                        alert(data1.message);
                    } else {
                        console.log("Server Error - Can't place an order: ", data1);
                        alert(`Server Error - Can't place an order: ${data1.message}`);
                    }
                }
            });
        });
    }

    function removeItemNavigateHome(itm) {
        setItem(null);
        navigate('/');
    }


    if (!item || item.id !== parseInt(id))
        return;

    return (
        <Container sx={{ padding: '15px', minWidth: '850px' }}>
            <Grid2 container spacing={4}>
                <Grid2 item xs={12} md={6}>
                    <Box className='sticky'>
                        <Grid2 container spacing={2}>
                            <Grid2 item xs={2}>
                                {dispThumbnails()}
                            </Grid2>
                            <Grid2 item xs={10}>
                                {activeImageIdx !== null && (
                                    <CardMedia
                                        component="img"
                                        sx={{ objectFit: 'contain', width: '100%', height: '100%', maxWidth: '630px', maxHeight: '630px', margin: '0 auto' }}
                                        image={item.images[activeImageIdx]}
                                        alt='product image'
                                    />
                                )}
                            </Grid2>
                        </Grid2>
                    </Box>
                </Grid2>

                <Grid2 item xs={12} md={6}>
                    <Typography variant="h4" component="h1" sx={{ fontWeight: 'normal' }}>
                        {item.name}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 2 }}>
                        <Typography variant="h6">{avgRating.toFixed(1)}</Typography>
                        <Box sx={{ ml: 1 }}>{dispAvgRating(item, 17, 17)}</Box>
                        <a href='#customer_reviews' className='link1 link' style={{ marginLeft: '20px' }}>
                            {item.accum_review_cnt.toLocaleString('en-US')} rating{item.accum_review_cnt > 1 ? 's' : null}
                        </a>
                    </Box>

                    <Divider sx={{ my: 2 }} />

                    <Box sx={{ mt: 2 }}>
                        {item.prices[activeItemIdx] !== item.discount_prices[activeItemIdx] && (
                            <Typography variant="h5" component="span" sx={{ color: 'red', mr: 2 }}>
                                -{Math.round((1 - item.discount_prices[activeItemIdx] / item.prices[activeItemIdx]) * 100)}%
                            </Typography>
                        )}
                        {displayPrice(item, activeItemIdx)}
                    </Box>
                    {item.prices[activeItemIdx] !== item.discount_prices[activeItemIdx] && (
                        <Box sx={{ mt: 1 }}>
                            <Typography variant="body2" component="span" sx={{ mr: 1 }}>List Price:</Typography>
                            {dispListPrice(item, activeItemIdx)}
                        </Box>
                    )}

                    <Box sx={{ display: 'flex', mt: 3 }}>
                        <Box>
                            <Typography variant="h6" component="span" sx={{ mr: 2 }}>Size:</Typography>
                            <Typography variant="h6" component="span" sx={{ fontWeight: 'bold' }}>
                                {`${item.amounts[activeItemIdx].toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ${item.units[activeItemIdx].charAt(0).toUpperCase() + item.units[activeItemIdx].slice(1)} (Pack of ${item.packs[activeItemIdx].toLocaleString('en-US')})`}
                            </Typography>
                            <Box sx={{ mt: 2 }}>{dispAllSizes()}</Box>
                        </Box>
                        <Box sx={{ ml: 3 }}>
                            {user && user.seller ? (
                                user.seller.id === item.seller_id && (
                                    <Box>
                                        <Button
                                            variant="outlined"
                                            startIcon={<EditIcon />}
                                            sx={{ display: 'block', borderRadius: 2, width: '220px', mb: 2 }}
                                            onClick={() => navigate(`/additem/${item.id}`)}
                                        >
                                            Edit
                                        </Button>
                                        <Button
                                            variant="contained"
                                            color="error"
                                            startIcon={<DeleteIcon />}
                                            sx={{ display: 'block', borderRadius: 2, width: '220px' }}
                                            onClick={() => handleInactvateItem(item, removeItemNavigateHome)}
                                        >
                                            Delete
                                        </Button>
                                    </Box>
                                )
                            ) : (
                                <Box>
                                    <ButtonGroup>
                                        <Button
                                            sx={{ borderRadius: '40px 0 0 20px', width: '15px', color: 'gray', border: '1px solid gray', background: `${quantity <= 1 ? 'lightgray' : 'white'}` }}
                                            disabled={quantity <= 1}
                                            onClick={() => setQuantity(quantity - 1)}
                                        >
                                            -
                                        </Button>
                                        <Select
                                            value={quantity}
                                            onChange={(e) => setQuantity(e.target.value)}
                                            sx={{ width: '200px', height: '37px', border: '1px solid grey', borderRadius: '0', background: 'white' }}
                                        >
                                            {quantityOptions.map(option => (
                                                <MenuItem key={option.value} value={option.value}>
                                                    {option.text}
                                                </MenuItem>
                                            ))}
                                        </Select>
                                        <Button
                                            sx={{ borderRadius: '0 20px 20px 0', width: '50px', color: 'gray', border: '1px solid gray', background: `${quantity >= 30 ? 'lightgray' : 'white'}` }}
                                            disabled={quantity >= 30}
                                            onClick={() => setQuantity(quantity + 1)}
                                        >
                                            +
                                        </Button>
                                    </ButtonGroup>
                                    <Button
                                        variant="contained"
                                        color="warning"
                                        startIcon={<AddShoppingCartIcon />}
                                        sx={{ display: 'block', borderRadius: 2, width: '220px', mt: 2 }}
                                        onClick={handleAddToCart}
                                    >
                                        Add to Cart
                                    </Button>
                                    <Button
                                        variant="contained"
                                        color="primary"
                                        startIcon={<ShoppingCartIcon />}
                                        sx={{ display: 'block', borderRadius: 2, width: '220px', mt: 2 }}
                                        onClick={handlePlaceOrder}
                                    >
                                        Buy Now
                                    </Button>
                                </Box>
                            )}
                        </Box>
                    </Box>

                    <Box sx={{ mt: 4 }}>{dispDetail_1()}</Box>
                    <Divider sx={{ my: 2 }} />
                    <Box sx={{ mt: 4 }}>
                        <Typography variant="h6" component="div" sx={{ fontWeight: 'bold', mb: 2 }}>
                            About this item
                        </Typography>
                        {dispAboutItem()}
                    </Box>
                </Grid2>
            </Grid2>

            <Divider sx={{ my: 4 }} />
            <Box>
                <Typography variant="h5" component="div" sx={{ fontWeight: 'bold', mb: 2 }}>
                    Product details
                </Typography>
                {dispDetail_2()}
            </Box>

            <Divider sx={{ my: 4 }} />
            <Box id='customer_reviews'>
                <Typography variant="h5" component="div" sx={{ fontWeight: 'bold', mb: 2 }}>
                    Customer reviews
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Box>{dispAvgRating(item, 20, 20)}</Box>
                    <Typography variant="h6" component="div" sx={{ ml: 2 }}>
                        {avgRating.toFixed(1)} out of 5
                    </Typography>
                </Box>
                <Typography variant="body1" component="div" sx={{ mb: 2 }}>
                    {item.accum_review_cnt.toLocaleString('en-US')} rating{item.accum_review_cnt > 1 ? 's' : null}
                </Typography>
                <Box sx={{ mb: 4 }}>{dispStarDistribution()}</Box>
                <Box>{dispReviews()}</Box>
            </Box>
        </Container>
    );
}

export default Item;