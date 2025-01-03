import { useState, useEffect } from 'react';
import { useParams, useOutletContext, useNavigate } from 'react-router-dom';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { dispRating, handleReviewDelete, handleReviewChange } from '../components/global';
import { Box, Button, Container, Divider, Grid2, IconButton, TextField, Typography } from '@mui/material';
import ClearIcon from '@mui/icons-material/Clear';
import ErrorIcon from '@mui/icons-material/Error';

function Review() {
    const { user, reviews, onSetReviews } = useOutletContext();
    const [itemReview, setItemReview] = useState({
        item: null,
        review: null,
    });
    const [validateAfterSubmit, setValidateAfterSubmit] = useState(false);
    const { itemId } = useParams();
    const iid = parseInt(itemId);
    const navigate = useNavigate();

    useEffect(() => {
        const reviewTmp = reviews.find(r => r.item_id === iid && !r.review_done);
        if (reviewTmp) {
            setItemReview({
                item: reviewTmp.item,
                review: reviewTmp,
            });
            formik.setFieldValue('rating', reviewTmp.rating);
        } else {
            fetch(`/items/${iid}`)
                .then(r => {
                    r.json().then(data => {
                        if (r.ok) {
                            setItemReview({
                                item: data,
                                review: null,
                            });
                            formik.resetForm();
                            setValidateAfterSubmit(false);
                        } else {
                            if (r.status === 401 || r.status === 403) {
                                console.log(data);
                                alert(data.message);
                            } else {
                                console.log("Server Error - Can't retrieve this item: ", data);
                                alert(`Server Error - Can't retrieve this item: ${data.message}`);
                            }
                        }
                    });
                });
        }
    }, [itemId, reviews]);

    const formSchema = yup.object().shape({
        rating: yup.number().required('Please select a star rating')
            .min(1, 'Your rating should be in between 1 and 5.')
            .max(5, 'Your rating should be in between 1 and 5.'),
        headline: yup.string().required('Please enter your headline.'),
        content: yup.string().required('Please add a review.'),
    });

    const formik = useFormik({
        initialValues: {
            rating: null,
            headline: '',
            content: '',
        },
        validationSchema: formSchema,
        validateOnChange: validateAfterSubmit,
        validateOnBlur: false,
        onSubmit: values => {
            handleReviewChange({
                id: itemReview.review.id,
                rating: formik.values.rating,
                headline: formik.values.headline,
                content: formik.values.content,
                review_done: 1,
            }, reviews, onSetReviews, () => navigate('/reviewlist'));
        },
    });

    if (!itemReview.item)
        return null;

    return (
        <Container maxWidth="md" sx={{ mt: 4 }}>
            <Typography variant="h4" component="h1" gutterBottom>
                Create Review
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Box
                    sx={{
                        width: 65,
                        height: 77,
                        backgroundImage: `url(${itemReview.item.images[0]})`,
                        backgroundSize: 'contain',
                        backgroundRepeat: 'no-repeat',
                        backgroundPosition: 'center',
                    }}
                />
                <Typography variant="h6" component="div" sx={{ ml: 2 }}>
                    {itemReview.item.name.length > 30 ? itemReview.item.name.slice(0, 85) + '...' : itemReview.item.name}
                </Typography>
            </Box>
            <Divider sx={{ backgroundColor: 'gainsboro', mb: 2 }} />

            <form onSubmit={formik.handleSubmit}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Box>
                        <Typography variant="h6" component="div" sx={{ fontWeight: 'bold' }}>
                            Overall rating
                        </Typography>
                        <Box sx={{ my: 2 }}>
                            {dispRating(itemReview.item.id, itemReview.review, user, reviews, onSetReviews)}
                        </Box>
                        {formik.errors.rating && (
                            <Box sx={{ mt: 2, color: 'crimson', display: 'flex', alignItems: 'center' }}>
                                <ErrorIcon sx={{ mr: 1 }} />
                                <Typography variant="body1">{formik.errors.rating}</Typography>
                            </Box>
                        )}
                    </Box>
                    {itemReview.review && (
                        <IconButton color="primary" onClick={() => handleReviewDelete(itemReview.review, reviews, onSetReviews)}>
                            <ClearIcon />
                        </IconButton>
                    )}
                </Box>
                <Divider sx={{ backgroundColor: 'gainsboro', mb: 2 }} />
                <Box sx={{ mb: 2 }}>
                    <Typography variant="h6" component="div" sx={{ fontWeight: 'bold' }}>
                        Add a headline
                    </Typography>
                    <TextField
                        fullWidth
                        id="headline"
                        name="headline"
                        placeholder="What's most important to know?"
                        value={formik.values.headline}
                        onChange={formik.handleChange}
                        error={formik.touched.headline && Boolean(formik.errors.headline)}
                        helperText={formik.touched.headline && formik.errors.headline}
                        sx={{ mt: 2 }}
                    />
                </Box>
                <Divider sx={{ backgroundColor: 'gainsboro', mb: 2 }} />
                <Box sx={{ mb: 2 }}>
                    <Typography variant="h6" component="div" sx={{ fontWeight: 'bold' }}>
                        Add a written review
                    </Typography>
                    <TextField
                        fullWidth
                        id="content"
                        name="content"
                        placeholder="What did you like or dislike? What did you use this product for?"
                        value={formik.values.content}
                        onChange={formik.handleChange}
                        error={formik.touched.content && Boolean(formik.errors.content)}
                        helperText={formik.touched.content && formik.errors.content}
                        multiline
                        rows={6}
                        sx={{ mt: 2 }}
                    />
                </Box>
                <Divider sx={{ backgroundColor: 'gainsboro', mb: 2 }} />
                <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    sx={{ float: 'right', borderRadius: 2 }}
                    onClick={() => setValidateAfterSubmit(true)}
                >
                    Submit
                </Button>
            </form>
        </Container>
    );
}

export default Review;