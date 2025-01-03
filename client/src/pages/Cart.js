import { useState, useEffect } from 'react';
import { useOutletContext, useNavigate } from 'react-router-dom';
import { handleCItemDelete, handleCItemChange } from '../components/global';
import { Box, Button, Checkbox, Container, Divider, Grid2, IconButton, Input, MenuItem, Select, Typography } from '@mui/material';
import { Delete as DeleteIcon, Update as UpdateIcon } from '@mui/icons-material';

function Cart() {
    const { user, cartItems, onSetCartItems, orders, onSetOrders } = useOutletContext();
    const [selectStatus, setSelectStatus] = useState(2);
    const navigate = useNavigate();
    const [qInputs, setQInputs] = useState({});

    useEffect(() => {
        if (!user || !user.customer) {
            navigate('/signin');
            return;
        }

        const tmpDict = {};
        cartItems.forEach(cItem => tmpDict[cItem.id] = [cItem.quantity >= 10 ? true : false, cItem.quantity.toString()]);
        setQInputs(tmpDict);

        const selectNum = cartItems.reduce((accum, cItem) => cItem.checked ? accum + 1 : accum, 0);
        setSelectStatus(selectNum === cartItems.length ? 2 : selectNum === 0 ? 0 : 1);
    }, [cartItems]);

    const quantityOptions = Array.from({ length: 11 }, (_, i) => ({
        key: i,
        text: i === 10 ? '10+' : i.toString(),
        value: i,
    }));

    function handleNavigateItem(itemId) {
        navigate(`/items/${itemId}`);
    }

    function handleCItemMassQuantityChange(e, d, cItem) {
        if (/^([1-9]{1}[0-9]{0,2})|([0]{0,1})$/.test(d.value)) {
            const qInput = qInputs[cItem.id];
            qInput[1] = d.value;
            setQInputs({ ...qInputs, [cItem.id]: qInput });
        }
    }

    function handleCItemQuantityChange(e, d, cItem) {
        if (d.value === 10) {
            const qInput = qInputs[cItem.id];
            qInput[0] = true;
            setQInputs({ ...qInputs, [cItem.id]: qInput });
        } else {
            handleCItemChange({ ...cItem, quantity: d.value }, onSetCartItems, null);
        }
    }

    async function handleSelect() {
        for (const cartItem of cartItems) {
            if ((selectStatus === 2 && cartItem.checked) || (selectStatus !== 2 && !cartItem.checked)) {
                await handleCItemChange({ ...cartItem, checked: selectStatus === 2 ? 0 : 1 }, onSetCartItems, null);
            }
        }
    }

    function deleteCheckedCartItems() {
        cartItems.filter(cItem => cItem.checked).forEach(cItem => handleCItemDelete(cItem, onSetCartItems));
    }

    async function handlePlaceOrder() {
        const numCheckedItems = cartItems.reduce((acc, cItem) => cItem.checked ? acc + 1 : acc, 0);
        if (!numCheckedItems) {
            alert("At least one item must be checked.");
            return;
        }

        await fetch('/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                street_1: user.street_1,
                street_2: user.street_2,
                city: user.city,
                state: user.state,
                zip_code: user.zip_code,
                customer_id: user.customer.id,
            })
        })
        .then(async r => {
            await r.json().then(async data1 => {
                if (r.ok) {
                    const orderTmp = data1;
                    const checkedCartItems = cartItems.filter(cItem => cItem.checked);
                    for (const cItem of checkedCartItems) {
                        await fetch('/orderitems', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                quantity: cItem.quantity,
                                price: cItem.item.discount_prices[cItem.item_idx],
                                item_idx: cItem.item_idx,
                                item_id: cItem.item.id,
                                order_id: orderTmp.id,
                            })
                        })
                        .then(async r => {
                            await r.json().then(async data2 => {
                                if (r.ok) {
                                    const orderItemTmp = data2;
                                    orderItemTmp.item = cItem.item;
                                    orderTmp.order_items.push(orderItemTmp);
                                } else {
                                    if (r.status === 401 || r.status === 403) {
                                        console.log(data2);
                                        alert(data2.message);
                                    } else {
                                        console.log("Server Error - Can't add an order item: ", data2);
                                        alert(`Server Error - Can't add an order item: ${data2.message}`);
                                        await fetch(`/orders/${orderTmp.id}`, { method: 'DELETE' }).then(r => { return; });
                                    }
                                }
                            });
                        });
                    }
                    onSetOrders([...orders, orderTmp]);
                    deleteCheckedCartItems();
                    navigate('/orders');
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

    function dispSubTotal() {
        return (
            <>
                {selectStatus ? (
                    <>
                        <Typography variant="h6" component="span" sx={{ marginRight: '10px' }}>
                            Subtotal ({cartItems.length} {cartItems.length <= 1 ? 'item' : 'items'}):
                        </Typography>
                        <Typography variant="h6" component="span" sx={{ fontWeight: 'bold' }}>
                            ${(Math.round(subTotal * 100) / 100).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                        </Typography>
                    </>
                ) : (
                    <Typography variant="h6" component="span" sx={{ marginRight: '10px' }}>
                        No items selected
                    </Typography>
                )}
            </>
        );
    }

    let subTotal = 0, itemTotal = 0;
    const dispCartItems = cartItems.map(cItem => {
        itemTotal = Math.round(cItem.quantity * cItem.item.discount_prices[cItem.item_idx] * 100) / 100;
        subTotal += cItem.checked ? itemTotal : 0;

        return (
            <Box key={cItem.id} sx={{ display: 'grid', gridTemplateColumns: '100px 200px 1fr 180px', alignItems: 'center', padding: '10px 0' }}>
                <Checkbox checked={Boolean(cItem.checked)} sx={{ margin: 'auto' }} onChange={() => handleCItemChange({ ...cItem, checked: !cItem.checked }, onSetCartItems, null)} />
                <Box
                    sx={{
                        width: '100%',
                        height: '220px',
                        backgroundImage: `url(${cItem.item.images[0]})`,
                        backgroundSize: 'contain',
                        backgroundRepeat: 'no-repeat',
                        backgroundPosition: 'center',
                        cursor: 'pointer',
                    }}
                    onClick={() => handleNavigateItem(cItem.item.id)}
                />
                <Box sx={{ margin: '10px' }}>
                    <Typography variant="h6" component="p" sx={{ marginBottom: '1px', cursor: 'pointer' }} onClick={() => handleNavigateItem(cItem.item.id)}>
                        {cItem.item.name}
                    </Typography>
                    <Box>
                        <Typography variant="body1" component="span" sx={{ fontWeight: 'bold', marginRight: '5px' }}>
                            Size:
                        </Typography>
                        <Typography variant="body1" component="span">
                            {`${cItem.item.amounts[cItem.item_idx]} ${cItem.item.units[cItem.item_idx].charAt(0).toUpperCase() + cItem.item.units[cItem.item_idx].slice(1)} (Pack of ${cItem.item.packs[cItem.item_idx]})`}
                        </Typography>
                    </Box>
                    <Box sx={{ marginTop: '15px' }}>
                        {Object.keys(qInputs).length > 0 && qInputs[cItem.id][0] ? (
                            <Box sx={{ display: 'inline-block' }}>
                                <Input
                                    type="text"
                                    size="small"
                                    sx={{ width: '80px' }}
                                    value={qInputs[cItem.id][1]}
                                    onChange={(e, d) => handleCItemMassQuantityChange(e, d, cItem)}
                                />
                                {qInputs[cItem.id][1] !== '' && (
                                    <Button
                                        variant="contained"
                                        color="warning"
                                        size="small"
                                        sx={{ marginLeft: '5px', borderRadius: '10px', padding: '7px 10px' }}
                                        onClick={() => handleCItemChange({ ...cItem, quantity: parseInt(qInputs[cItem.id][1], 10) }, onSetCartItems, null)}
                                    >
                                        Update
                                    </Button>
                                )}
                            </Box>
                        ) : (
                            <Select
                                value={cItem.quantity}
                                onChange={(e, d) => handleCItemQuantityChange(e, d, cItem)}
                                sx={{ fontSize: '1.2em', padding: '7px 10px', margin: '10px 0 0 0', borderRadius: '10px', background: 'whitesmoke', border: '1px solid lightgray' }}
                            >
                                {quantityOptions.map(option => (
                                    <MenuItem key={option.value} value={option.value}>
                                        {option.text}
                                    </MenuItem>
                                ))}
                            </Select>
                        )}
                        <Typography variant="body1" component="span" sx={{ fontSize: '1.2em', color: 'lightgray', margin: '0 10px' }}>
                            |
                        </Typography>
                        <Typography variant="body1" component="span" sx={{ cursor: 'pointer', color: 'red' }} onClick={() => handleCItemDelete(cItem, onSetCartItems)}>
                            Delete
                        </Typography>
                    </Box>
                </Box>
                <Box sx={{ display: 'grid', gridTemplateColumns: '1fr max-content', alignItems: 'center', margin: '10px' }}>
                    <Box />
                    <Typography variant="h6" component="div" sx={{ fontWeight: 'bold', marginRight: '10px' }}>
                        ${itemTotal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </Typography>
                </Box>
            </Box>
        );
    });

    return (
        <Container sx={{ minWidth: '815px', border: '10px solid whitesmoke' }}>
            <Box sx={{ display: 'grid', gridTemplateColumns: '1fr max-content', alignItems: 'center', padding: '20px', border: '10px solid whitesmoke' }}>
                <Box>{dispSubTotal()}</Box>
                <Button variant="contained" color="warning" size="large" sx={{ borderRadius: '10px', width: '250px' }} onClick={handlePlaceOrder}>
                    Proceed to checkout
                </Button>
            </Box>
            <Box sx={{ border: '10px solid whitesmoke' }}>
                <Typography variant="h4" sx={{ padding: '30px 0 0 20px' }}>
                    Shopping Cart
                </Typography>
                <Typography variant="body1" sx={{ padding: '10px 0 0 20px' }}>
                    {selectStatus === 0 ? 'No items selected. ' : null}
                    <Typography component="span" sx={{ cursor: 'pointer', color: 'blue' }} onClick={handleSelect}>
                        {selectStatus === 2 ? 'Deselect all items' : 'Select all items'}
                    </Typography>
                </Typography>
                <Box sx={{ display: 'grid', gridTemplateColumns: '1fr max-content', padding: '10px 20px' }}>
                    <Box />
                    <Typography variant="body1" sx={{ marginRight: '20px' }}>
                        Price
                    </Typography>
                </Box>
                <Divider sx={{ margin: '0 20px' }} />
                <Box>{dispCartItems}</Box>
                <Divider sx={{ margin: '0 20px' }} />
                <Box sx={{ display: 'grid', gridTemplateColumns: '1fr max-content', alignItems: 'center', padding: '10px 20px' }}>
                    <Box />
                    <Box sx={{ margin: '10px 20px 40px' }}>{dispSubTotal()}</Box>
                </Box>
            </Box>
        </Container>
    );
}

export default Cart;