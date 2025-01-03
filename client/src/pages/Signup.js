import { useState } from 'react';
import { useOutletContext, useNavigate } from 'react-router-dom';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { setUserInfo } from '../components/global';
import { Box, TextField, Button, Typography, Container, Alert, Divider, Checkbox, FormControlLabel } from '@mui/material';

function Signup() {
    const [isSeller, setIsSeller] = useState(false);
    const { onSetUser, onSetCartItems, onSetOrders, onSetReviews, onSetSellerItems } = useOutletContext();
    const navigate = useNavigate();

    const formSchema = yup.object().shape({
        name: isSeller ? yup.string().required('Must enter a name.') : null,
        firstName: !isSeller ? yup.string().required('Must enter a first name.') : null,
        lastName: !isSeller ? yup.string().required('Must enter a last name.') : null,
        username: yup.string().required('Must enter a username')
            .min(5, 'Must be between 5 and 20 characters')
            .max(20, 'Must be between 5 and 20 characters'),
        password: yup.string().required('Must enter a password')
            .min(5, 'Must be at least 5 characters long'),
        email: yup.string().matches(
            /^[A-Za-z]+[A-Za-z0-9]*\.?[A-Za-z0-9]+@[A-Za-z_\-]+\.[A-Za-z]{2,3}$/,
            'Invalid email address'
        ),
        mobile: !isSeller ? yup.string().matches(
            /^((([\(]?[0-9]{3,4}[\)]\s?)|([0-9]{3,4}[\-]))[0-9]{3,4}[\-][0-9]{4})|([0-9]{10,12})$/,
            'Mobile number is not valid'
        ) : null,
        phone: yup.string().matches(
            /^((([\(]?[0-9]{3,4}[\)]\s?)|([0-9]{3,4}[\-]))[0-9]{3,4}[\-][0-9]{4})|([0-9]{10,12})$/,
            'Phone number is not valid'
        ),
        zipCode: yup.string().matches(
            /^[0-9]{5}$/,
            'Zip code is not valid'            
        ),
    });

    const formik = useFormik({
        initialValues: {
            isSeller: isSeller,
            name: '',
            firstName: '',
            lastName: '',
            username: '',
            password: '',
            email: '',
            mobile: '',
            phone: '',
            street_1: '',
            street_2: '',
            city: '',
            state: '',
            zipCode: '',
        },
        validationSchema: formSchema,
        onSubmit: (values) => {
            fetch('/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(values),
            })
            .then(r => {
                r.json().then(data => {
                    if (r.ok) {
                        setUserInfo(data, onSetUser, onSetCartItems, onSetOrders, onSetReviews, onSetSellerItems);
                        navigate('/');
                    } else {
                        console.log("In Signup, error: ", data.message);
                        alert(`Error - New Account: ${data.message}`);
                    }
                })
            });
        },
    });

    function handleIsSellerCheck(bSeller) {
        setIsSeller(!bSeller);
        formik.setFieldValue('isSeller', !bSeller);
    }

    return (
        <Container maxWidth="sm" sx={{ mt: 8 }}>
            <Box sx={{ p: 4, border: '1px solid lightgrey', borderRadius: 1, backgroundColor: '#F5FBEF' }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    Create account
                </Typography>
                <form onSubmit={formik.handleSubmit}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={isSeller}
                                onChange={() => handleIsSellerCheck(isSeller)}
                                name="isSeller"
                                color="primary"
                            />
                        }
                        label="Create Seller Account"
                    />
                    {isSeller ? (
                        <TextField
                            fullWidth
                            id="name"
                            name="name"
                            label="Name"
                            value={formik.values.name}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            error={formik.touched.name && Boolean(formik.errors.name)}
                            helperText={formik.touched.name && formik.errors.name}
                            margin="normal"
                        />
                    ) : (
                        <>
                            <TextField
                                fullWidth
                                id="firstName"
                                name="firstName"
                                label="First Name"
                                value={formik.values.firstName}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                error={formik.touched.firstName && Boolean(formik.errors.firstName)}
                                helperText={formik.touched.firstName && formik.errors.firstName}
                                margin="normal"
                            />
                            <TextField
                                fullWidth
                                id="lastName"
                                name="lastName"
                                label="Last Name"
                                value={formik.values.lastName}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                error={formik.touched.lastName && Boolean(formik.errors.lastName)}
                                helperText={formik.touched.lastName && formik.errors.lastName}
                                margin="normal"
                            />
                        </>
                    )}
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
                    <TextField
                        fullWidth
                        id="email"
                        name="email"
                        label="Email"
                        value={formik.values.email}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                        error={formik.touched.email && Boolean(formik.errors.email)}
                        helperText={formik.touched.email && formik.errors.email}
                        margin="normal"
                    />
                    {!isSeller && (
                        <TextField
                            fullWidth
                            id="mobile"
                            name="mobile"
                            label="Mobile"
                            value={formik.values.mobile}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            error={formik.touched.mobile && Boolean(formik.errors.mobile)}
                            helperText={formik.touched.mobile && formik.errors.mobile}
                            margin="normal"
                        />
                    )}
                    <TextField
                        fullWidth
                        id="phone"
                        name="phone"
                        label="Phone"
                        value={formik.values.phone}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                        error={formik.touched.phone && Boolean(formik.errors.phone)}
                        helperText={formik.touched.phone && formik.errors.phone}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        id="street_1"
                        name="street_1"
                        label="Street 1"
                        value={formik.values.street_1}
                        onChange={formik.handleChange}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        id="street_2"
                        name="street_2"
                        label="Street 2"
                        value={formik.values.street_2}
                        onChange={formik.handleChange}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        id="city"
                        name="city"
                        label="City"
                        value={formik.values.city}
                        onChange={formik.handleChange}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        id="state"
                        name="state"
                        label="State"
                        value={formik.values.state}
                        onChange={formik.handleChange}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        id="zipCode"
                        name="zipCode"
                        label="Zip Code"
                        value={formik.values.zipCode}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                        error={formik.touched.zipCode && Boolean(formik.errors.zipCode)}
                        helperText={formik.touched.zipCode && formik.errors.zipCode}
                        margin="normal"
                    />
                    <Button color="primary" variant="contained" fullWidth type="submit" sx={{ mt: 2 }}>
                        Continue
                    </Button>
                </form>
                <Divider sx={{ my: 2 }} />
                <Button color="secondary" variant="outlined" fullWidth onClick={() => navigate('/signin')}>
                    Already have an account? Sign in
                </Button>
            </Box>
        </Container>
    );
}

export default Signup;