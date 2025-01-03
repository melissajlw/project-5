import { useEffect, useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { ItemContext } from '../components/ItemProvider';
import { Box, Grid, Typography, Card, CardMedia, CardContent, Container, Paper } from '@mui/material';

function Home() {
    const [topSalesItems, setTopSalesItems] = useState([]);
    const [topReviewedItems, setTopReviewedItems] = useState([]);
    const [items, setItems] = useState([]);
    const { item, setItem } = useContext(ItemContext);
    const navigate = useNavigate();

    useEffect(() => {
        fetch('/items/sales')
            .then(r => r.json())
            .then(data => {
                setTopSalesItems(data);
            });

        fetch('/items/rating')
            .then(r => r.json())
            .then(data => {
                setTopReviewedItems(data);
            });

        fetch('/items')
            .then(r => r.json())
            .then(data => {
                setItems(data);
            });
    }, []);

    const handleItemClick = (item) => {
        setItem(item);
        navigate(`/items/${item.id}`);
    };

    return (
        <Box sx={{ backgroundColor: '#F5FBEF', minHeight: '100vh', paddingBottom: 4 }}>
            <Box
                sx={{
                    backgroundColor: '#92AD94',
                    height: '250px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: '#F5FBEF',
                    textShadow: '2px 2px 4px rgba(0,0,0,0.7)',
                }}
            >
                <Typography variant="h1" component="h1">
                    Welcome to Our E-Commerce Site!
                </Typography>
            </Box>
            <br/>
            <Container>
                <Paper elevation={3} sx={{ padding: 3, marginBottom: 4 }}>
                    <Typography variant="h4" component="h2" sx={{ mb: 2, color: '#503D42' }}>
                        Best Sellers
                    </Typography>
                    <Grid container spacing={2}>
                        {topSalesItems.map(item => (
                            <Grid item xs={12} sm={6} md={3} key={item.id}>
                                <Card className='link' onClick={() => handleItemClick(item)} sx={{ backgroundColor: '#748B75' }}>
                                    <CardMedia
                                        component="img"
                                        sx={{ width: '100%', height: 200 }}
                                        image={item.images[0]}
                                        alt={item.name}
                                    />
                                    <CardContent>
                                        <Typography variant="body2" color="text.secondary" sx={{ color: '#F5FBEF' }}>
                                            {`${item.name.slice(0, 17)}...`}
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                        ))}
                    </Grid>
                </Paper>

                <Paper elevation={3} sx={{ padding: 3, marginBottom: 4 }}>
                    <Typography variant="h4" component="h2" sx={{ mb: 2, color: '#503D42' }}>
                        Best Rated
                    </Typography>
                    <Grid container spacing={2}>
                        {topReviewedItems.map(item => (
                            <Grid item xs={12} sm={6} md={3} key={item.id}>
                                <Card className='link' onClick={() => handleItemClick(item)} sx={{ backgroundColor: '#748B75' }}>
                                    <CardMedia
                                        component="img"
                                        sx={{ width: '100%', height: 200 }}
                                        image={item.images[0]}
                                        alt={item.name}
                                    />
                                    <CardContent>
                                        <Typography variant="body2" color="text.secondary" sx={{ color: '#F5FBEF' }}>
                                            {`${item.name.slice(0, 17)}...`}
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                        ))}
                    </Grid>
                </Paper>

                <Paper elevation={3} sx={{ padding: 3, marginBottom: 4 }}>
                    <Typography variant="h4" component="h2" sx={{ mb: 2, color: '#503D42' }}>
                        All Products
                    </Typography>
                    <Grid container spacing={2}>
                        {items.map(item => (
                            <Grid item xs={12} sm={6} md={3} key={item.id}>
                                <Card className='link' onClick={() => handleItemClick(item)} sx={{ backgroundColor: '#748B75' }}>
                                    <CardMedia
                                        component="img"
                                        sx={{ width: '100%', height: 200 }}
                                        image={item.images[0]}
                                        alt={item.name}
                                    />
                                    <CardContent>
                                        <Typography variant="body2" color="text.secondary" sx={{ color: '#F5FBEF' }}>
                                            {`${item.name.slice(0, 17)}...`}
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                        ))}
                    </Grid>
                </Paper>
            </Container>
        </Box>
    );
}

export default Home;