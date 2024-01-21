import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { back } from '../features/pages';
import { fill } from '../features/content';
import { useNavigate } from 'react-router-dom';

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
      const response = await fetch('http://127.0.0.1:8000/api/ask/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(article)
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      console.log('成功发送：', data);
      dispatch(fill(data));
      navigate('/article');
    } catch (error) {
      console.error('Error sending data to backend', error);
      setErrorMessage('Error sending data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={'navigation'}>
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      <button className='btn1' onClick={() => dispatch(back())}>Go Back</button>
      <button className='btn2' onClick={GenerateClick} disabled={isLoading}>
        {isLoading ? 'Generating...' : 'Generate'}
      </button>
    </div>
  );
}

export default GenerateButton;
