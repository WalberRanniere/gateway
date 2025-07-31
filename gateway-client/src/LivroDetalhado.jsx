/* eslint-disable no-unused-vars */
import { useState } from 'react';
import {
  TextField,
  Button,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Box,
  createTheme,
  ThemeProvider
} from '@mui/material';
import axios from 'axios';

const theme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function LivroDetalhado() {
  const [isbn, setIsbn] = useState('');
  const [livro, setLivro] = useState(null);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState(null);

  const buscarLivro = async () => {
    setLoading(true);
    setErro(null);
    setLivro(null);
    try {
      const res = await axios.get(`http://localhost:8000/api/livro-detalhado-soap/${isbn}`);
      setLivro(res.data);
    } catch (err) {
      setErro('Livro não encontrado ou erro na consulta.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          bgcolor: '#121212',
          padding: 2,
        }}
      >
        <Box sx={{ maxWidth: 500, width: '100%' }}>
          <TextField
            label="ISBN"
            variant="outlined"
            fullWidth
            value={isbn}
            onChange={e => setIsbn(e.target.value)}
            margin="normal"
            InputProps={{
              style: { color: 'white' }
            }}
            InputLabelProps={{
              style: { color: 'white' }
            }}
          />
          <Button variant="contained" color="primary" onClick={buscarLivro} fullWidth>
            Buscar Livro
          </Button>

          {loading && <CircularProgress sx={{ mt: 2 }} />}
          {erro && <Typography color="error" sx={{ mt: 2 }}>{erro}</Typography>}

          {livro && (
            <Card sx={{ mt: 2 }}>
              <CardContent>
                <Typography variant="h6">{livro.titulo}</Typography>
                <Typography variant="body1">Autor: {livro.autor}</Typography>
                <Typography variant="body2">Ano: {livro.ano}</Typography>
                <Typography variant="body2">Preço: R$ {livro.preco} {livro.moeda}</Typography>
                <Typography variant="caption">ISBN: {livro.isbn}</Typography>
              </CardContent>
            </Card>
          )}
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default LivroDetalhado;
