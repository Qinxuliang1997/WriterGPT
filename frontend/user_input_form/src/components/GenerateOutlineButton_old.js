import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { back } from '../features/pages';
import { info } from '../features/description';
import { useNavigate } from 'react-router-dom';
import { next } from '../features/pages'

import axios from 'axios'; 

const GenerateOutlineButton = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const description = useSelector((e) => e.description.value);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const GenerateClick = async () => {
    setIsLoading(true);
    setErrorMessage('');

    try {
      // Use axios for the POST request
      // 127.0.0.1:8000
      const response = await axios.post('http://106.14.184.241/api/outline/', description, {
        headers: {
          'Content-Type': 'application/json',
        }
      });
      console.log('成功发送：', response.data);
      const outlineData = {
        outline:response.data.article.outline,
      };
      dispatch(info(outlineData));
      dispatch(next());
    } catch (error) {
      console.error('Error sending data to backend', error);
      setErrorMessage('出错啦！请稍后再试');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={'btnNavigation'}>
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      <button className='btn1' onClick={() => dispatch(back())}>上一步</button>
      <button className='btn2' onClick={GenerateClick} disabled={isLoading}>
        {isLoading ? '正在生成目录......' : '生成目录'}
      </button>
    </div>
  );
}

export default GenerateOutlineButton;
