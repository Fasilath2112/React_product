import PropTypes from 'prop-types';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const ProductTable = ({ products }) => {
  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Category</TableCell>
            <TableCell>Product Name</TableCell>
            <TableCell>Product Image</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {products.map((product, index) => (
            <TableRow key={index}>
              <TableCell>{product.category}</TableCell>
              <TableCell>{product.productName}</TableCell>
              <TableCell>
                <img src={product.productImage} alt={product.productName} width="50" />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

ProductTable.propTypes = {
  products: PropTypes.arrayOf(
    PropTypes.shape({
      category: PropTypes.string.isRequired,
      productName: PropTypes.string.isRequired,
      productImage: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default ProductTable;
