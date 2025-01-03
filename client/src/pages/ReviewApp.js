import { useState, useEffect } from 'react';
import { useOutletContext, Outlet, useNavigate } from 'react-router-dom';
import { Box, Button, Container, IconButton, Input, Typography } from '@mui/material';
import { Edit as EditIcon, Save as SaveIcon, Cancel as CancelIcon, AccountCircle as AccountCircleIcon } from '@mui/icons-material';

function ReviewApp() {
    const { user, onSetUser, orders, reviews, onSetReviews } = useOutletContext();
    const [nickname, setNickname] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (!user || !user.customer) {
            navigate('/signin');
            return;
        }
    }, [user, navigate]);

    function handleNickNameChange() {
        fetch(`/customers/${user.customer.id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                nickname: nickname,
            }),
        })
        .then(r => {
            r.json().then(data => {
                if (r.ok) {
                    onSetUser({
                        ...user,
                        customer: {
                            ...user.customer,
                            nickname: nickname,
                        }
                    });
                    setNickname(null);
                } else {
                    if (r.status === 401 || r.status === 403) {
                        console.log(data);
                        alert(data.message);
                    } else {
                        console.log('Server Error - Updating customer nickname: ', data);
                        alert(`Server Error - Updating customer nickname: ${data.message}`);
                    }
                }
            });
        });
    }

    if (!user || !user.customer) return null;

    return (
        <Container>
            <Box sx={{ height: '60px', padding: '0 140px', backgroundColor: 'lightcyan', fontSize: '1.1em', display: 'flex', alignItems: 'center' }}>
                <AccountCircleIcon sx={{ fontSize: 40, color: 'lightgray' }} />
                {nickname !== null ? (
                    <>
                        <Input
                            type='text'
                            sx={{ width: '180px', height: '35px', border: '1px solid gray', borderRadius: '5px', marginLeft: 1 }}
                            value={nickname}
                            onChange={(e) => setNickname(e.target.value)}
                        />
                        <Button
                            variant="contained"
                            color="warning"
                            startIcon={<SaveIcon />}
                            sx={{ marginLeft: 1, borderRadius: '10px' }}
                            onClick={handleNickNameChange}
                        >
                            Save
                        </Button>
                        <Button
                            variant="outlined"
                            startIcon={<CancelIcon />}
                            sx={{ marginLeft: 1, borderRadius: '10px' }}
                            onClick={() => setNickname(null)}
                        >
                            Cancel
                        </Button>
                    </>
                ) : (
                    <>
                        <Typography variant="body1" sx={{ marginLeft: 1 }}>
                            {user.customer.nickname}
                        </Typography>
                        <IconButton
                            color="primary"
                            sx={{ marginLeft: 1 }}
                            onClick={() => setNickname(user.customer.nickname)}
                        >
                            <EditIcon />
                        </IconButton>
                    </>
                )}
            </Box>
            <Outlet context={{ user, orders, reviews, onSetReviews }} />
        </Container>
    );
}

export default ReviewApp;