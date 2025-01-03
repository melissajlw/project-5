import { useState } from 'react';
import { useOutletContext, useNavigate } from 'react-router-dom';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { setUserInfo } from '../components/global';
import { Box, TextField, Button, Typography, Container, Alert, Divider } from '@mui/material';

function Signin() {
    const { onSetUser, onSetCartItems, onSetOrders, onSetReviews, onSetSellerItems } = useOutletContext();
    const [isSigninFail, setIsSigninFail] = useState(false);
    const navigate = useNavigate();

    const formSchema = yup.object().shape({
        username: yup.string().min(5, 'Must be between 5 and 20 characters')
            .max(20, 'Must be between 5 and 20 characters'),
        password: yup.string().min(5, 'Must be at least 5 characters long'),
    });

    const formik = useFormik({
        initialValues: {
            username: '',
            password: '',
        },
        validationSchema: formSchema,
        onSubmit: (values) => {
            fetch('/authenticate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(values),
            })
            .then(r => 
                r.json().then(data => {
                    if (r.ok) {
                        setUserInfo(data, onSetUser, onSetCartItems, onSetOrders, onSetReviews, onSetSellerItems);
                        navigate('/');
                    } else {
                        console.log('in Signin, error: ', data.message);
                        setIsSigninFail(true);
                    }
                })
            );
        },
    });

    return (
        <Container maxWidth="sm" sx={{ mt: 8 }}>
            <Box sx={{ p: 4, border: '1px solid lightgrey', borderRadius: 1, backgroundColor: '#F5FBEF' }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    Sign in
                </Typography>
                <form onSubmit={formik.handleSubmit}>
                    <TextField
                        fullWidth
                        id="username"
                        name="username"
                        label="Username"
                        value={formik.values.username}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                        error={formik.touched.username && Boolean(formik.errors.username)}
                        helperText={formik.touched.username && formik.errors.username}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        id="password"
                        name="password"
                        label="Password"
                        type="password"
                        value={formik.values.password}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                        error={formik.touched.password && Boolean(formik.errors.password)}
                        helperText={formik.touched.password && formik.errors.password}
                        margin="normal"
                    />
                    {isSigninFail && (
                        <Alert severity="error" sx={{ mt: 2 }}>
                            Invalid username or password. Please, try again.
                        </Alert>
                    )}
                    <Button color="primary" variant="contained" fullWidth type="submit" sx={{ mt: 2 }}>
                        Continue
                    </Button>
                </form>
                <Divider sx={{ my: 2 }} />
                <Button color="secondary" variant="outlined" fullWidth onClick={() => navigate('/signup')}>
                    Create your account
                </Button>
            </Box>
        </Container>
    );
}

export default Signin;