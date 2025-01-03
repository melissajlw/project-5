import { useEffect, useState, useContext } from 'react';
import { useOutletContext, useNavigate, useParams } from 'react-router-dom';
import { useFormik, FormikProvider, FieldArray } from 'formik';
import * as yup from 'yup';
import ImgDropzone from '../components/ImageDropzone';
import { ItemContext } from '../components/ItemProvider';
import { setUserInfo } from '../components/global';
import { Box, Button, Container, Divider, Grid2, IconButton, Input, Radio, TextField, Typography } from '@mui/material';
import { AddCircle as AddCircleIcon, RemoveCircle as RemoveCircleIcon, Warning as WarningIcon, Delete as DeleteIcon } from '@mui/icons-material';

function AddItem() {
    const [imgFiles, setImgFiles] = useState([]);
    const { user, onSetUser, onSetCartItems, onSetOrders, onSetReviews, onSetSellerItems } = useOutletContext();
    const navigate = useNavigate();
    const { id } = useParams();
    const { item, setItem } = useContext(ItemContext);

    console.log('in AddItem, id: ', id, ', item: ', item);

    useEffect(() => {
        console.log('in Additem, user: ', user);
        if (!user || !user.seller) {
            console.log("herer?????");
            navigate('/signin');
            return;
        }

        if (id && item && parseInt(id) === item.id) {
            formik.setFieldValue('name', item.name);
            formik.setFieldValue('brand', item.brand);
            formik.setFieldValue('default_item_idx', item.default_item_idx);
            formik.setFieldValue('prices', item.prices);
            formik.setFieldValue('discount_prices', item.discount_prices);
            formik.setFieldValue('amounts', item.amounts);
            formik.setFieldValue('units', item.units);
            formik.setFieldValue('packs', item.packs);
            formik.setFieldValue('about_item', item.about_item);
            const details_1_key = [], details_1_val = [];
            item.details_1.forEach(dtl => {
                const pair = dtl.split(';-;');
                details_1_key.push(pair[0]);
                details_1_val.push(pair[1]);
            });
            formik.setFieldValue('details_1_key', details_1_key);
            formik.setFieldValue('details_1_val', details_1_val);

            const details_2_key = [], details_2_val = [];
            item.details_2.forEach(dtl => {
                const pair = dtl.split(';-;');
                details_2_key.push(pair[0]);
                details_2_val.push(pair[1]);
            });
            formik.setFieldValue('details_2_key', details_2_key);
            formik.setFieldValue('details_2_val', details_2_val);

            formik.setFieldValue('images', item.images);
            setImgFiles(item.images);
        }
    }, []);

    const formSchema = yup.object().shape({
        name: yup.string().required('Required')
            .max(200, 'Please, enter name up to 200 characters.'),
        prices: yup.array().of(
            yup.string().required('Required')
                .matches(/^[0-9]*([.]{1}[0-9]{1,2})?$/, 
                    'Please, enter a decimal number with two digits of fractional part. ')
        ),
        discount_prices: yup.array().of(
            yup.string().required('Required')
                .matches(/^[0-9]*([.]{1}[0-9]{1,2})?$/, 
                    'Please, enter a decimal number with two digits of fractional part. ')
        ),
        amounts: yup.array().of(
            yup.string().required('Required')
                .matches(/^([0-9]*)([.]{1}[0-9]{1,2})?$/, 
                    'Please, enter a decimal number with one or two digits of fractional part. ')
        ),
        units: yup.array().of(
            yup.string().required('Required')
        ),
        packs: yup.array().of(
            yup.string().required('Required')
                .matches(/^[1-9]+[0-9]*$/, 
                    'Please, enter an integer.'
                )
        ),
        details_1_key: yup.array().of(
            yup.string().required('required')
        ),
        details_1_val: yup.array().of(
            yup.string().required('required')
        ),
        about_item: yup.array().of(
            yup.string().required('Required')
        ), 
        details_2_key: yup.array().of(
            yup.string().required('required')
        ),
        details_2_val: yup.array().of(
            yup.string().required('required')
        ),
        images: yup.array().min(1, 'At least one image must be uploaded.').max(10, 'Up to 10 images are allowed to upload.')
    });

    const formik = useFormik({
        initialValues: {
            name: '',
            brand: '',
            default_item_idx: 0,
            prices: [''],
            discount_prices: [''],
            amounts: [''],
            units: [''],
            packs: [''],
            about_item: [''], // bullet points
            details_1_key: [''],
            details_1_val: [''],
            details_2_key: [''],
            details_2_val: [''],
            images: [],
            category_id: null,
            seller_id: null,
        },
        validationSchema: formSchema,
        onSubmit: async values => {
            const uploadedImages = [];
            const cloudName = 'dfsqyivhu';
            for (const file of imgFiles) {
                if (typeof(file) === 'string') {
                    uploadedImages.push(file);
                } else {
                    const publicId = file.name.split('.').slice(0, -1).join('.');
                    const formData = new FormData();
                    formData.append('file', file);
                    formData.append('upload_preset', 'flatiron_p5_pjt_imgs');
                    formData.append('public_id', publicId);

                    try {
                        const response = await fetch(`https://api.cloudinary.com/v1_1/${cloudName}/upload`, {
                            method: 'POST',
                            body: formData,
                        });
                        const data = await response.json();
                        uploadedImages.push(data.secure_url);
                    } catch (error) {
                        console.log('Cloudinary Image Upload Error: ', error);
                    }
                }
            };
            values.images = uploadedImages;

            if (values.prices[values.prices.length-1] === '')
                values.prices.pop();
            if (values.discount_prices[values.discount_prices.length-1] === '')
                values.discount_prices.pop();
            if (values.amounts[values.amounts.length-1] === '')
                values.amounts.pop();
            if (values.units[values.units.length-1] === '')
                values.units.pop();
            if (values.packs[values.packs.length-1] === '')
                values.packs.pop();
            if (values.about_item[values.about_item.length-1] === '')
                values.about_item.pop();
            if (values.details_1_key[values.details_1_key.length-1] === '')
                values.details_1_key.pop();
            if (values.details_1_val[values.details_1_val.length-1] === '')
                values.details_1_val.pop();
            if (values.details_2_key[values.details_2_key.length-1] === '')
                values.details_2_key.pop();
            if (values.details_2_val[values.details_2_val.length-1] === '')
                values.details_2_val.pop();

            const details_1 = values.details_1_key.map((key, i) => key + ';-;' + values.details_1_val[i]);
            const details_2 = values.details_2_key.map((key, i) => key + ';-;' + values.details_2_val[i]);

            const postValues = {
                name: values.name,
                brand: values.brand, 
                default_item_idx: values.default_item_idx,
                prices: values.prices.map(price => parseFloat(price)),
                discount_prices: values.discount_prices.map(price => parseFloat(price)),
                amounts: values.amounts.map(amt => parseFloat(amt)),
                units: values.units,
                packs: values.packs.map(pack => parseFloat(pack)),
                about_item: values.about_item, 
                details_1: details_1,
                details_2: details_2,
                images: uploadedImages,
                category_id: null,
                seller_id: user.seller.id,
            };

            const url = id && item && parseInt(id) === item.id ? `/items/${id}` : '/items'
            await fetch(url, {
                method: id && item && parseInt(id) === item.id ? 'PATCH' : 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(postValues),
            })
            .then(async r1 => {
                await r1.json().then(async data => {
                    if (r1.ok) {
                        setItem(data);

                        await fetch('/authenticate')
                        .then(async r2 => 
                            await r2.json().then(userData => {
                                if (r2.ok) {
                                    setUserInfo(userData, onSetUser, onSetCartItems, onSetOrders, onSetReviews, onSetSellerItems);
                                } else {
                                    console.log('In App, error: ', data.message);
                                }
                            })
                        )

                        alert('Item is successfully updated.');
                        navigate(`/items/${data.id}`);
                    } else {
                        if (r1.status === 401 || r1.status === 403) {
                            console.log(data);
                            alert(data.message);
                        } else {
                            console.log("Server Error - Can't post this item: ", data);
                            alert(`Server Error - Can't post this item: ${data.message}`);
                        }
                    }
                })
            });
        },
    });

    const pricesFA = {field: 'prices', placeholder: 'Price', insert: null, remove: null, push: null, width: '1fr', };
    const discount_pricesFA = {field: 'discount_prices', placeholder: 'Discounted Price', insert: null, remove: null, push: null, width: '1fr', };
    const amountsFA = {field: 'amounts', placeholder: 'Volume', insert: null, remove: null, push: null, width: '1fr', };
    const unitsFA = {field: 'units', placeholder: 'Unit Measure', insert: null, remove: null, push: null, width: '1fr', };
    const packsFA = {field: 'packs', placeholder: 'Pack Quantity', insert: null, remove: null, push: null, width: '1fr', };
    const priceSizeFAs = [pricesFA, discount_pricesFA, amountsFA, unitsFA, packsFA];

    const aboutThisItemFAs = [{field: 'about_item', placeholder: '', insert: null, remove: null, push: null, width: '1fr', }];

    const details_1_FAs = [
        {field: 'details_1_key', placeholder: 'Key', insert: null, remove: null, push: null, width: '1fr', },
        {field: 'details_1_val', placeholder: 'Value', insert: null, remove: null, push: null, width: '1.6fr', }
    ];

    const details_2_FAs = [
        {field: 'details_2_key', placeholder: 'Key', insert: null, remove: null, push: null, width: '1fr', },
        {field: 'details_2_val', placeholder: 'Value', insert: null, remove: null, push: null, width: '1.6fr', }
    ];

    function handleImgDrop(acceptedFiles) {

        const imgFilesDict = {};
        imgFiles.forEach(file => {
            if (typeof(file) === 'string') {
                const urlStrs = file.split('/');
                imgFilesDict[urlStrs[urlStrs.length-1]] = file;
            } else
                imgFilesDict[file.name] = file;
        });

        const imgFilesTmp = [...imgFiles];
        acceptedFiles.forEach(file => {
            if (!(file.name in imgFilesDict)) {
                imgFilesDict[file.name] = file;
                imgFilesTmp.push(Object.assign(file, {preview: URL.createObjectURL(file)}));
            }
        });
        formik.setFieldValue('images', imgFilesTmp);
        setImgFiles(imgFilesTmp);
    };

    function removeImgFile(imgFile) {
        const imgFilesTmp = typeof(imgFile) === 'string' ? 
            imgFiles.filter(file => typeof(file) !== 'string' || file !== imgFile) : 
            imgFiles.filter(file => typeof(file) === 'string' || file.name !== imgFile.name);
        formik.setFieldValue('images', imgFilesTmp);
        setImgFiles(files => imgFilesTmp);
    }

    function getFirstErrorInFieldArrays(fieldArrays) {
        for (const fa of fieldArrays) {
            if (isErrorFieldArray(fa)) {
                for (let i = 0; i < formik.values[fa.field].length; i++) {
                    if (formik.errors[fa.field][i] && formik.touched[fa.field][i]) {
                        return (
                            <Box sx={{ display: 'flex', alignItems: 'center', color: 'error.main', mt: 1 }}>
                                <WarningIcon />
                                <Typography variant="body2" sx={{ ml: 1 }}>
                                    {fa.placeholder ? `${fa.placeholder}: ${formik.errors[fa.field][i]}` : `${formik.errors[fa.field][i]}`}
                                </Typography>
                            </Box>
                        );
                    }
                }
            } else
                continue;
        }

        return null;
    }

    function addFieldArrays(fieldArrays, bUpdateRadioBtn) {
        const gridColumns = [];
        if (bUpdateRadioBtn)
            gridColumns.push('45px');
        fieldArrays.forEach(fa => gridColumns.push(fa.width));
        gridColumns.push('30px');
        gridColumns.push('30px');
        const gridColumnsStr = gridColumns.join(' ');

        return (
            <Box>
                <Box sx={{ display: 'grid', gridTemplateColumns: gridColumnsStr, alignItems: 'center' }}>
                    {bUpdateRadioBtn ? addRadioBtns(fieldArrays[0]) : null}
                    {
                        fieldArrays.map(fa => (
                            <Box key={fa.field}>{addFieldArray(fa)}</Box>
                        ))
                    }
                    {addInsertBtns(fieldArrays)}
                    {addRemoveBtns(fieldArrays, bUpdateRadioBtn)}
                </Box>
                {getFirstErrorInFieldArrays(fieldArrays)}
            </Box>
        );
    }

    function addRadioBtns(fieldArray) {
        return (
            <Box>
                <Box>
                    {fieldArray.placeholder ? <Box sx={{ height: '19.99px' }}> </Box> : null}
                </Box>
                {
                    formik.values[fieldArray.field].map((val, i) => (
                        <Radio
                            key={i}
                            name='default_item_idx'
                            sx={{ margin: '7.5px 5px 5.8px 0' }}
                            value={i}
                            checked={formik.values.default_item_idx === i}
                            onChange={(e, d) => formik.setFieldValue('default_item_idx', d.value)}
                        />
                    ))
                }
            </Box>
        );
    }

    function isErrorFieldArray(fieldArray) {
        return formik.errors[fieldArray.field] && formik.touched[fieldArray.field];
    }

    function isErrorFieldArrayVal(fieldArray, index) {
        return isErrorFieldArray(fieldArray) && formik.errors[fieldArray.field][index] && 
            formik.touched[fieldArray.field][index];
    }

    function addFieldArray(fieldArray) {
        return (
            <FormikProvider value={formik}>
                <FieldArray name={fieldArray.field}>
                    {({ insert, remove, push }) => {
                        fieldArray.insert = insert;
                        fieldArray.remove = remove;
                        fieldArray.push = push;

                        return (
                            <Box>
                                <Typography variant="body1" sx={{ paddingLeft: '15px', fontWeight: 'bold' }}>
                                    {fieldArray.placeholder ? fieldArray.placeholder : null}
                                </Typography>
                                {
                                    formik.values[fieldArray.field].map((val, i) => {
                                        return (
                                            <Box key={`${fieldArray.field}-${i}`}>
                                                <Input
                                                    name={`${fieldArray.field}.${i}`}
                                                    sx={{
                                                        width: '100%', height: '30px', marginBottom: '3px',
                                                        borderColor: isErrorFieldArrayVal(fieldArray, i) ? 'error.main' : 'grey.300',
                                                    }}
                                                    placeholder={fieldArray.placeholder}
                                                    value={formik.values[fieldArray.field][i]}
                                                    onChange={formik.handleChange} onBlur={formik.handleBlur}
                                                />
                                            </Box>
                                        );
                                    })
                                }
                            </Box>
                        );
                    }}
                </FieldArray>
            </FormikProvider>
        );
    }

    function addInsertBtns(fieldArrays) {
        return (
            <Box>
                <Box>
                    {fieldArrays[0].placeholder ? <Box sx={{ height: '19.99px' }}> </Box> : null}
                </Box>
                {
                    formik.values[fieldArrays[0].field].map((val, i) => (
                        <IconButton
                            key={i}
                            color="primary"
                            sx={{ margin: '4.5px 0 7.5px 0' }}
                            onClick={() => {
                                fieldArrays.forEach(fa => {
                                    fa.insert(i + 1, '');
                                });
                            }}
                        >
                            <AddCircleIcon />
                        </IconButton>
                    ))
                }
            </Box>
        );
    }

    function addRemoveBtns(fieldArrays, bUpdateRadioBtn) {
        return (
            <Box>
                <Box>
                    {fieldArrays[0].placeholder ? <Box sx={{ height: '19.99px' }}> </Box> : null}
                </Box>
                {
                    formik.values[fieldArrays[0].field].map((val, i) => (
                        <IconButton
                            key={i}
                            color="error"
                            disabled={i === 0}
                            sx={{ margin: '4.5px 0 7.5px 0' }}
                            onClick={() => {
                                fieldArrays.forEach(fa => {
                                    fa.remove(i);
                                });
    
                                if (bUpdateRadioBtn && formik.values.default_item_idx === i)
                                    formik.setFieldValue('default_item_idx', i - 1);
                            }}
                        >
                            <RemoveCircleIcon />
                        </IconButton>
                    ))
                }
            </Box>
        );
    }

    return (
        <Container sx={{ minWidth: '815px', padding: '15px' }}>
            <form onSubmit={formik.handleSubmit}>
                <Grid2 container spacing={4}>
                    <Grid2 item xs={12} md={6}>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', mt: 2 }}>
                            {imgFiles.map((imgFile, i) => (
                                <Box key={i} sx={{ margin: 'auto', position: 'relative' }}>
                                    <img
                                        src={typeof imgFile === 'string' ? imgFile : imgFile.preview}
                                        alt="product"
                                        style={{ width: '200px', height: '200px', objectFit: 'cover' }}
                                    />
                                    <IconButton
                                        color="error"
                                        sx={{ position: 'absolute', top: 0, right: 0 }}
                                        onClick={() => removeImgFile(imgFile)}
                                    >
                                        <DeleteIcon />
                                    </IconButton>
                                </Box>
                            ))}
                        </Box>
                        <ImgDropzone onDrop={handleImgDrop} />
                        {formik.errors.images && (
                            <Box sx={{ display: 'flex', alignItems: 'center', color: 'error.main', mt: 1 }}>
                                <WarningIcon />
                                <Typography variant="body2" sx={{ ml: 1 }}>
                                    {formik.errors.images}
                                </Typography>
                            </Box>
                        )}
                    </Grid2>
                    <Grid2 item xs={12} md={6}>
                        <Box sx={{ padding: '15px 0 10px 30px' }}>
                            <Typography variant="h5">Product Name:</Typography>
                            <TextField
                                id="name"
                                name="name"
                                multiline
                                rows={3}
                                fullWidth
                                sx={{ mt: 1 }}
                                value={formik.values.name}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                            />
                            {formik.errors.name && formik.touched.name && (
                                <Box sx={{ display: 'flex', alignItems: 'center', color: 'error.main', mt: 5 }}>
                                    <WarningIcon />
                                    <Typography variant="body2" sx={{ ml: 1 }}>
                                        {formik.errors.name}
                                    </Typography>
                                </Box>
                            )}
                            <Divider sx={{ my: 4 }} />
                            <Typography variant="h6" sx={{ mb: 1, fontWeight: 'bold' }}>Prices & Sizes:</Typography>
                                {addFieldArrays(priceSizeFAs, true)}
                            <Box sx={{ mt: 4 }}>
                                <Typography variant="h6" sx={{ mb: 1, fontWeight: 'bold' }}>Product Details:</Typography>
                                {addFieldArrays(details_1_FAs, false)}
                            </Box>
                            <Divider sx={{ my: 4 }} />
                            <Box sx={{ mt: 2 }}>
                                <Typography variant="h6" sx={{ mb: 1, fontWeight: 'bold' }}>Product Description:</Typography>
                                {addFieldArrays(aboutThisItemFAs, false)}
                            </Box>
                        </Box>
                    </Grid2>
                </Grid2>
                <Divider sx={{ my: 4 }} />
                <Grid2 item xs={12} md={6}>
                    <Box sx={{ padding: '15px 0 10px 30px' }}>
                        <Typography variant="h5" sx={{ mt: 2, mb: 1, fontWeight: 'bold' }}>Additional Details:</Typography>
                        {addFieldArrays(details_2_FAs, false)}
                    </Box>
                </Grid2>
                <Box sx={{ padding: '15px 0 10px 30px' }}>
                    <Button type="submit" variant="contained" color="warning" size="large" sx={{ color: 'black', borderRadius: '10px', width: '250px' }}>
                        Add this product
                    </Button>
                </Box>
            </form>
        </Container>
    );
}

export default AddItem;