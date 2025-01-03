import { useRouteError } from 'react-router-dom';
import { Box, Container, Typography } from '@mui/material';

function ErrorPage() {
    const error = useRouteError();
    console.error(error);

    return (
        <Container sx={{ textAlign: 'center', paddingTop: '100px' }}>
            <Box>
                <Typography variant="h1" component="div" sx={{ color: 'crimson', mb: 2 }}>
                    Invalid path! Please, check your path.
                </Typography>
                <Typography variant="h5" component="div">
                    {error.data}
                </Typography>
            </Box>
        </Container>
    );
}

export default ErrorPage;