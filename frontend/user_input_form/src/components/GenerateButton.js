import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { back } from '../features/pages';
import { fill } from '../features/content';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; // Import axios

const GenerateButton = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const article = useSelector((e) => e.article.value);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const GenerateClick = async () => {
    setIsLoading(true);
    setErrorMessage('');

    try {
      // Use axios for the POST request
      const response = await axios.post('http://127.0.0.1:8000/api/ask/', article, {
        headers: {
          'Content-Type': 'application/json',
        }
      });
      console.log('成功发送：', response.data);
      dispatch(fill({content: response.data.content}));
      navigate('/article');
    } catch (error) {
      console.error('Error sending data to backend', error);
      setErrorMessage('Error sending data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={'btnNavigation'}>
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      <button className='btn1' onClick={() => dispatch(back())}>Go Back</button>
      <button className='btn2' onClick={GenerateClick} disabled={isLoading}>
        {isLoading ? 'Generating...' : 'Generate'}
      </button>
    </div>
  );
}

export default GenerateButton;
