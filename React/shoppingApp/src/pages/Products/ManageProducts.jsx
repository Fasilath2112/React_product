import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchProducts, addProduct } from '../../store/products';
import { Button, TextField, Box, Typography } from '@mui/material';
import ProductTable from '../../components/ProductTable';

const ManageProducts = () => {
  const dispatch = useDispatch();
  const products = useSelector((state) => state.products.products);
  const productStatus = useSelector((state) => state.products.status);

  const [category, setCategory] = useState('');
  const [productName, setProductName] = useState('');
  const [productImage, setProductImage] = useState('');

  useEffect(() => {
    if (productStatus === 'idle') {
      dispatch(fetchProducts());
    }
  }, [productStatus, dispatch]);

  const handleAddProduct = () => {
    const newProduct = {
      category,
      productName,
      productImage,
    };
    dispatch(addProduct(newProduct));
    setCategory('');
    setProductName('');
    setProductImage('');
  };

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Manage Products
      </Typography>
      <Box mb={3} display="flex" gap={2}>
        <TextField
          label="Category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        />
        <TextField
          label="Product Name"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
        />
        <TextField
          label="Product Image URL"
          value={productImage}
          onChange={(e) => setProductImage(e.target.value)}
        />
        <Button variant="contained" onClick={handleAddProduct}>
          Add Product
        </Button>
      </Box>
      <ProductTable products={products} />
    </Box>
  );
};

export default ManageProducts;
